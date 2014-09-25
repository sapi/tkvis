import inspect
import sys


class EventManager(object):
    def __init__(self):
        self._topLevelEvents = []  # at top of call stack; child of nothing

        self._enabled = True

    def _findParent(self, frames, obj=None):
        events = obj.children if obj is not None else self._topLevelEvents

        for evt in events:
            if evt.frame in frames:
                parent = self._findParent(frames, evt)

                return parent if parent is not None else evt

    def disable(self):
        self._enabled = False

    def enable(self):
        self._enabled = True

    def addEvent(self, event):
        if not self._enabled:
            return

        frames = [frame for frame,_,_,_,_,_ in inspect.stack()]
        parent = self._findParent(frames)

        if parent:
            parent.addChild(event)
        else:
            self._topLevelEvents.append(event)


# Mimic a singleton with a module var
# NB: This is not threadsafe (but neither is Tkinter)
EVENT_MANAGER = EventManager()


class Event(object):
    def __init__(self, obj, fn, args, kwargs):
        self.obj = obj
        self.fn = fn

        self.args = args
        self.kwargs = kwargs

        self.result = None
        self.frame = None

        self._children = []

    def __str__(self):
        if self.obj is None:
            return '{}(...) -> {}'.format(self.fn.__name__, self.result)

        return '{!r}.{}(...) -> {}'.format(self.obj, self.fn.__name__,
                self.result)

    @property
    def children(self):
        return self._children

    def addChild(self, child):
        self._children.append(child)

    def __iter__(self):
        for child in self._children:
            yield child


def log(fn, isMethod=True):
    def f(*args, **kwargs):
        if isMethod:
            evt = Event(args[0], fn, args[1:], kwargs)
        else:
            evt = Event(None, fn, args, kwargs)

        # set the current frame as the event's frame
        # this isn't entirely accurate (as the event represents the function
        # we're about to call), but will work for our purposes
        # TODO this WILL cause a memory leak: need to delete frame later
        evt.frame = inspect.currentframe()

        EVENT_MANAGER.addEvent(evt)

        result = fn(*args, **kwargs)

        evt.result = result

        return result

    return f


def monitor(moduleName):
    module = sys.modules[moduleName]

    functions = inspect.getmembers(module, inspect.isfunction)

    for name,fn in functions:
        setattr(module, name, log(fn, isMethod=False))

    classes = inspect.getmembers(module, inspect.isclass)

    for _,cls in classes:
        methods = inspect.getmembers(cls, inspect.ismethod)

        for name,method in methods:
            setattr(cls, name, log(method, isMethod=True))
