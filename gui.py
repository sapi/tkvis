from PIL import Image, ImageTk
import os
import tkvis as tk

from widgets import clear_highlight, highlight
from tkcrap import AnchorFrame, SideFrame


class TkVisualiser(tk.Toplevel):
    HIGHLIGHT_COLOR = 'red'

    def __init__(self, master, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs)

        # change window settings
        self.title('TK Visualiser')

        # set up the window
        frm = tk.Frame(self)
        frm.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)

        self.lbxWidgets = tk.Listbox(frm)
        self.lbxWidgets.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.BOTH)
        self.lbxWidgets.bind('<<ListboxSelect>>',
                self.lbxWidgetsSelectionChanged)

        self.frmDynamic = tk.Frame(frm)
        self.frmDynamic.pack(side=tk.LEFT)

        self.dynamicFrames = []

        # set up local vars
        self._selection = None, None  # widget, bg
        self._selectionParent = None, None

    def lbxWidgetsSelectionChanged(self, evt):
        # get selection
        idx = self.lbxWidgets.curselection()[0]
        tkObj = self._widgets[idx]

        # reset the old value
        oldWidget, oldValue = self._selection

        if oldWidget is not None:
            clear_highlight(oldWidget, oldValue)

        oldParent, oldParentValue = self._selectionParent

        if oldParent is not None:
            clear_highlight(oldParent, oldParentValue)

        # apply the highlight and save the old value
        self._selection = tkObj.obj, highlight(tkObj.obj)

        if tkObj.parent is not None:
            self._selectionParent = (
                    tkObj.parent.obj,
                    highlight(tkObj.parent.obj, asParent=True)
                )
        else:
            self._selectionParent = None, None

        # update the pack args
        self.setPackArgs(tkObj)

    def setObjectTree(self, root, objs):
        self._objsRoot = root
        self._objs = objs

        self._updateLbxWidgets()

    def _updateLbxWidgets(self):
        self.lbxWidgets.delete(0, tk.END)

        self._widgets = list(self._objsRoot)

        # doing this the lazy way for now: __str__ on a tree object is defined
        # to print out a nice pretty tree :)
        for line in str(self._objsRoot).splitlines():
            self.lbxWidgets.insert(tk.END, line)

    def setPackArgs(self, tkObj):
        side = tkObj.packArgs.get('side', tk.TOP)
        anchor = tkObj.packArgs.get('anchor', tk.CENTER)

        # generate pack thingy
        for frm in self.dynamicFrames:
            frm.destroy()

        frmSide = SideFrame(self.frmDynamic, side)
        frmSide.pack(side=tk.TOP)
        self.dynamicFrames.append(frmSide)

        frmAnchor = AnchorFrame(self.frmDynamic, side, anchor)
        frmAnchor.pack(side=tk.TOP)
        self.dynamicFrames.append(frmAnchor)


def create_gui(root):
    window = TkVisualiser(root)

    return window
