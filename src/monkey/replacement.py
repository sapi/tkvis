from functools import wraps

from src.model.tkobj import TkObject


# We keep track of the root object, as well as all encountered objects, in a
# pair of global variables.
# This does not pose a huge problem, as by design this module should be a
# singleton for the life of the app.
#
# NB: There are potential thread-safety issues with this approach.
#     Here be dragons!
#
OBJS_ROOT = None
OBJS = {}


def replace_creation(cls, isRootObj=False):
    # we don't want to touch anything which isn't a class
    # a quick and dirty way to do this, which ties in nicely with our purposes,
    # is to check if it has an __init__ method
    if not hasattr(cls, '__init__'):
        return cls

    oldinit = cls.__init__

    @wraps(cls.__init__)
    def f(self, *args, **kwargs):
        # NB: must call oldinit *BEFORE* logging
        oldinit(self, *args, **kwargs)

        if isRootObj:
            log_root_creation(cls, self, *args, **kwargs)
        else:
            log_creation(cls, self, *args, **kwargs)

    cls.__init__ = f

    return cls


def replace_pack(fn):
    @wraps(fn)
    def f(*args, **kwargs):
        fn(*args, **kwargs)
        log_pack(*args, **kwargs)
    return f


def add_object(obj, parent=None):
    # it's possible that this method will be caled more than once (notably,
    # from both the subclass and the superclass)
    # it doesn't matter to us which one we take, so we just ignore the second
    # call to this function
    objID = id(obj)

    if objID in OBJS:
        return None

    tkObj = TkObject(obj)
    OBJS[objID] = tkObj

    if parent is not None:
        pID = id(parent)
        assert pID in OBJS, 'Unknown parent of Tk object: %r'%parent

        parentTkObj = OBJS[pID]
        parentTkObj.addChild(tkObj)

    return OBJS[objID]


def log_creation(cls, obj, *args, **kwargs):
    assert len(args) > 0, 'Expected at least 1 arg to Tk __init__ method'
    parent = args[0]

    add_object(obj, parent)


def log_root_creation(cls, obj, *args, **kwargs):
    global OBJS_ROOT
    OBJS_ROOT = add_object(obj)

    # override the main loop to do what we want
    if OBJS_ROOT is not None:
        assert hasattr(obj, 'mainloop'), 'Expected mainloop on root Tk object'
        setattr(obj, 'mainloop', run(obj))


def log_pack(obj, *args, **kwargs):
    objID = id(obj)
    assert objID in OBJS, \
            'Attempt to pack widget which was not detected at creation'

    assert not args, 'Expected no position arguments to pack'

    tkObj = OBJS[objID]
    tkObj.packArgs = kwargs


def run(root):
    mainloop = root.mainloop

    def f():
        from src.gui.main import create_gui
        from callbacks import EVENT_MANAGER

        EVENT_MANAGER.disable()

        window = create_gui(root)

        window.setEventManager(EVENT_MANAGER)

        OBJS_ROOT.removeChild(OBJS[id(window)])
        window.setObjectTree(OBJS_ROOT, OBJS)

        EVENT_MANAGER.enable()

        mainloop()
    return f
