import Tkinter as tk

from widgets import describe


class TkObject(object):
    def __init__(self, obj, parent=None):
        self.obj = obj
        self.parent = parent

        self._repr = describe(obj)

        self._children = []
        self._packArgs = None

    def __str__(self, level=0):
        ret = '{indent}{value}\n'.format(indent='\t'*level, value=self._repr)

        for child in self.children:
            ret += child.__str__(level+1)

        return ret

    def __iter__(self):
        yield self

        for child in self.children:
            for elem in child:
                yield elem

    @property
    def children(self):
        return self._children

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
    def packArgs(self, val):
        self._packArgs = val

    @property
    def isPacked(self):
        return self._packArgs is not None

    @property
    def needsPacking(self):
        return not isinstance(self.obj, (tk.Tk, tk.Toplevel, tk.Menu))

    @property
    def hasError(self):
        # TODO: not finished
        return self.needsPacking and not self.isPacked

    @property
    def hasWarning(self):
        # TODO: not finished
        return False
