from PIL import Image, ImageTk
import os
import tkvis as tk

from widgets import clear_highlight, highlight, \
        HIGHLIGHT_COLOR, PARENT_HIGHLIGHT_COLOR
from tkcrap import AnchorFrame, ExpandFrame, FillFrame, SideFrame


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

        # add the colour coding in the listbox itself
        self._updateLbxColors(tkObj)

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

    def _updateLbxColors(self, tkObj):
        for idx,elem in enumerate(self._widgets):
            # text color, set to match highlight colours
            if elem == tkObj:
                self.lbxWidgets.itemconfig(idx,
                        selectforeground=HIGHLIGHT_COLOR)
            elif elem == tkObj.parent:
                self.lbxWidgets.itemconfig(idx, fg=PARENT_HIGHLIGHT_COLOR)
            else:
                self.lbxWidgets.itemconfig(idx, fg='black')

            # background color, if not packed
            if elem.needsPacking and not elem.packArgs:
                self.lbxWidgets.itemconfig(idx, bg='red')

    def setPackArgs(self, tkObj):
        side = tkObj.packArgs.get('side', tk.TOP)
        anchor = tkObj.packArgs.get('anchor', tk.CENTER)
        fill = tkObj.packArgs.get('fill', tk.NONE)
        expand = tkObj.packArgs.get('expand', False)

        # generate pack thingy
        for frm in self.dynamicFrames:
            frm.destroy()

        # side, anchor, fill, expand
        frmLeft = tk.Frame(self.frmDynamic)
        frmLeft.pack(side=tk.LEFT)
        self.dynamicFrames.append(frmLeft)

        frmSide = SideFrame(frmLeft, side)
        frmSide.pack(side=tk.TOP)
        self.dynamicFrames.append(frmSide)

        frmAnchor = AnchorFrame(frmLeft, side, anchor)
        frmAnchor.pack(side=tk.TOP)
        self.dynamicFrames.append(frmAnchor)

        frmFill = FillFrame(frmLeft, side, fill)
        frmFill.pack(side=tk.TOP)
        self.dynamicFrames.append(frmFill)

        frmExpand = ExpandFrame(frmLeft, side, expand)
        frmExpand.pack(side=tk.TOP)
        self.dynamicFrames.append(frmExpand)

        # space in window
        window = self._objsRoot.obj
        sw = window.winfo_width()
        sh = window.winfo_height()

        cvsRight = tk.Canvas(self.frmDynamic, width=sw, height=sh)
        cvsRight.pack(side=tk.LEFT)
        self.dynamicFrames.append(cvsRight)

        # first, clear out the canvas with a recognisable colour
        cvsRight.create_rectangle(0, 0, sw, sh, fill='gray', outline='gray')

        # draw the parent, if necessary
        if tkObj.parent is not None:
            self._drawWidget(cvsRight, tkObj.parent, PARENT_HIGHLIGHT_COLOR)

        # draw the packed space on this guy
        self._drawPackedSpace(cvsRight, tkObj, 'red4', side=side)

        # draw all of the filled space from views packed before this one
        # at the same level (in other words, the space from the parent)
        if tkObj.parent is not None:
            for child in tkObj.parent.children:
                if child is tkObj:
                    break

                childSide = child.packArgs.get('side', tk.TOP)
                self._drawPackedSpace(cvsRight, child, PARENT_HIGHLIGHT_COLOR,
                        side=childSide)

        # and finally we draw the object itself on top
        self._drawWidget(cvsRight, tkObj, HIGHLIGHT_COLOR)

    def _drawWidget(self, canvas, tkObj, color):
        sx = self._objsRoot.obj.winfo_rootx()
        sy = self._objsRoot.obj.winfo_rooty()

        x = tkObj.obj.winfo_rootx() - sx
        y = tkObj.obj.winfo_rooty() - sy
        w = tkObj.obj.winfo_width()
        h = tkObj.obj.winfo_height()

        canvas.create_rectangle(
                x, y,
                x + w, y + h,
                fill=color,
                outline=color,
            )

    def _drawPackedSpace(self, canvas, tkObj, color, side=tk.TOP):
        sx = self._objsRoot.obj.winfo_rootx()
        sy = self._objsRoot.obj.winfo_rooty()

        vx = tkObj.obj.winfo_rootx() - sx
        vy = tkObj.obj.winfo_rooty() - sy
        vw = tkObj.obj.winfo_width()
        vh = tkObj.obj.winfo_height()

        # we want to extend over the entirety of the other axis (so if we
        # packed on to the left or right hand side, extend vertically)
        if tkObj.parent is not None:
            px = tkObj.parent.obj.winfo_rootx() - sx
            py = tkObj.parent.obj.winfo_rooty() - sy
            pw = tkObj.parent.obj.winfo_width()
            ph = tkObj.parent.obj.winfo_height()

            if side in (tk.LEFT, tk.RIGHT):
                canvas.create_rectangle(
                        vx, py,
                        vx + vw, py + ph,
                        fill=color,
                        outline=color,
                    )
            else:
                canvas.create_rectangle(
                        px, vy,
                        px + pw, vy + vh,
                        fill=color,
                        outline=color,
                    )


def create_gui(root):
    window = TkVisualiser(root)

    return window
