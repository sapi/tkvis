import Tkinter

import src.monkey.replacement as _replacement


# set up to log all creation and pack calls
for name in dir(Tkinter):
    obj = getattr(Tkinter, name)

    if hasattr(obj, 'pack'):
        # intercept all calls to pack
        pack = getattr(obj, 'pack')
        setattr(obj, 'pack', _replacement.replace_pack(pack))

        # also intercept creation calls for all packable objects
        setattr(Tkinter, name, _replacement.replace_creation(obj))


# also log the Tk object itself, which is where the root app is created
# we need to do the same thing with the toplevel as well
_Tk = getattr(Tkinter, 'Tk')
_Tk = _replacement.replace_creation(_Tk, isRootObj=True)
setattr(Tkinter, 'Tk', _Tk)

_Toplevel = getattr(Tkinter, 'Toplevel')
_Toplevel = _replacement.replace_creation(_Toplevel, isRootObj=False)
setattr(Tkinter, 'Toplevel', _Toplevel)


# set the attributes on this module so it can be used as a drop-in replacement
for name in dir(Tkinter):
    obj = getattr(Tkinter, name)
    globals()[name] = obj


# import monitor into global scope so this can be called after importing tkvis
# hopefully this never conflicts with anything in Tk...
from src.monkey.callbacks import monitor
