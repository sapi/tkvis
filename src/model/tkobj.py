# We need a Tkinter import here (cf tkvis) because this module is imported
# from tkvis.
# Should limit the usage here as much as possible, as, eg, instantiating a
# tk object from here will cause serious problems.
import Tkinter as tk

from src.config import cfg
from namespaces import Namespace
from widgets import describe


class TkObject(object):
    DEFAULT_PACK_ARGS = {
            'side': tk.TOP,
            'anchor': tk.CENTER,
            'fill': tk.NONE,
            'expand': tk.FALSE,
        }

    def __init__(self, obj, parent=None):
        self.obj = obj
        self.parent = parent

        self._repr = describe(obj)

        self._children = []
        self._isPacked = False

        # NB: must NOT use the seter
        self._packArgs = Namespace(**TkObject.DEFAULT_PACK_ARGS)

    def __str__(self, level=0):
        ret = '{indent}{value}\n'.format(indent=' '*4*level, value=self._repr)

        for child in self.children:
            ret += child.__str__(level+1)

        return ret

    def __iter__(self):
        yield self

        for child in self.children:
            for elem in child:
                yield elem

    def rearrangeChildren(self):
        # We want to order all packed children before all unpacked children
        # This is to account for people creating widgets in a different order
        # than they are packed
        # Our end result should have all unpacked widgets at the bottom
        packed = []
        unpacked = []

        for child in self.children:
            if child.isPacked:
                packed.append(child)
            else:
                unpacked.append(child)

        self.children = packed + unpacked

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, val):
        self._children = val

    def addChild(self, child):
        self._children.append(child)
        child.parent = self

    def removeChild(self, child):
        assert child in self._children, \
                'Cannot remove non-existent child: %s'%child
        self._children.remove(child)

    @property
    def packArgs(self):
        return self._packArgs

    @packArgs.setter
    def packArgs(self, kwargs):
        keys = set(kwargs.keys()).union(set(TkObject.DEFAULT_PACK_ARGS.keys()))
        d = {k: kwargs.get(k, TkObject.DEFAULT_PACK_ARGS.get(k)) for k in keys}

        self._packArgs = Namespace(**d)
        self._isPacked = True

        # layout our parent
        if self.parent is not None:
            self.parent.rearrangeChildren()

    @property
    def isPacked(self):
        return self._isPacked

    @property
    def needsPacking(self):
        return not isinstance(self.obj, (tk.Tk, tk.Toplevel, tk.Menu))

    @property
    def errors(self):
        errors = []

        if self.needsPacking and not self.isPacked:
            errors.append(cfg.MESSAGES.NOT_PACKED)

        return errors

    @property
    def warnings(self):
        # All our checking atm requires that the widget be packed
        if not self.isPacked:
            return []

        warnings = []

        # First check: does this have an anchor argument that doesn't seem to
        # make sense (eg, N or S when packed to TOP or BOTTOM)
        side = self.packArgs.side
        anchor = self.packArgs.anchor

        if (side in (tk.TOP, tk.BOTTOM) and anchor in (tk.N, tk.S)) \
                or (side in (tk.LEFT, tk.RIGHT) and anchor in (tk.E, tk.W)):
            warnings.append(cfg.MESSAGES.BAD_ANCHOR)

        # Second check: has there been inconsistent packing in child widgets
        childSides = [child.packArgs.side for child in self.children]

        if childSides and len(set(childSides)) != 1:
            warnings.append(cfg.MESSAGES.INCONSISTENT_CHILD_PACKING)

        return warnings
