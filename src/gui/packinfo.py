import tkvis as tk

from arrows import ArrowCanvas
from borders import BorderedFrame


ACTIVE_FRAME_COLOR = 'red'
INACTIVE_FRAME_COLOR = 'gray80'
OTHER_COLOR = 'gray60'
EXAMPLE_FRAME_SIZE = 20


class PackInfoFrame(tk.Frame):
    def __init__(self, master, width=100, height=100, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.lbl = tk.Label(self)
        self.lbl.pack(side=tk.TOP)

        frm = BorderedFrame(self, bd=2, width=width, height=height)
        frm.pack(side=tk.TOP)
        frm.pack_propagate(0)

        self.frm = frm.inner

        self.width = width
        self.height = height

        self._framesToRemove = []

    def update(self, **kwargs):
        for frm in self._framesToRemove:
            frm.destroy()

        self._framesToRemove = []


class SideFrame(PackInfoFrame):
    def update(self, side=tk.TOP):
        PackInfoFrame.update(self, side=side)

        self.lbl.config(text='side={}'.format(side.upper()))

        if side in (tk.TOP, tk.BOTTOM):
            innerSize = {
                    'height': EXAMPLE_FRAME_SIZE,
                    'width': self.width/4,
                }
            size = {'height': EXAMPLE_FRAME_SIZE}

            fill = tk.X
            axis = ArrowCanvas.Y
        else:
            innerSize = {
                    'width': EXAMPLE_FRAME_SIZE,
                    'height': self.height/4,
                }
            size = {'width': EXAMPLE_FRAME_SIZE}

            fill = tk.Y
            axis = ArrowCanvas.X

        flip = side in (tk.BOTTOM, tk.RIGHT)

        frmBefore = tk.Frame(self.frm, bg=OTHER_COLOR, **size)
        frmBefore.pack(side=side, fill=fill)
        self._framesToRemove.append(frmBefore)

        frmPacked = tk.Frame(self.frm, bg=ACTIVE_FRAME_COLOR, **innerSize)
        frmPacked.pack(side=side)
        self._framesToRemove.append(frmPacked)

        cvsArrow = ArrowCanvas(self.frm, axis, flip=flip)
        cvsArrow.pack(side=side)
        self._framesToRemove.append(cvsArrow)


class AnchorFrame(PackInfoFrame):
    def update(self, side=tk.TOP, anchor=tk.CENTER):
        PackInfoFrame.update(self, side=side, anchor=anchor)

        self.lbl.config(text='anchor={}'.format(side.upper()))

        if side in (tk.TOP, tk.BOTTOM):
            key = 'height'
            fill = tk.X
            innerFrameArgs = {
                    'width': self.width/4,
                    'height': EXAMPLE_FRAME_SIZE
                }
        else:
            key = 'width'
            fill = tk.Y
            innerFrameArgs = {
                    'width': EXAMPLE_FRAME_SIZE,
                    'height': self.height/4
                }

        size = {key: EXAMPLE_FRAME_SIZE}

        frmBefore = tk.Frame(self.frm, bg=OTHER_COLOR, **size)
        frmBefore.pack(side=side, fill=fill)
        self._framesToRemove.append(frmBefore)

        frmPacked = tk.Frame(self.frm, bg=INACTIVE_FRAME_COLOR, **size)
        frmPacked.pack(side=side, fill=fill)
        frmPacked.pack_propagate(0)
        self._framesToRemove.append(frmPacked)

        frmAnchored = tk.Frame(frmPacked, bg=ACTIVE_FRAME_COLOR,
                **innerFrameArgs)
        frmAnchored.pack(side=side, anchor=anchor)
        self._framesToRemove.append(frmAnchored)


class FillFrame(PackInfoFrame):
    def update(self, side=tk.TOP, fill=tk.NONE):
        PackInfoFrame.update(self, side=side, fill=fill)

        self.lbl.config(text='fill={}'.format(fill.upper()))

        if side in (tk.TOP, tk.BOTTOM):
            key = 'height'
            innerFrameArgs = {
                    'width': self.width/4,
                    'height': EXAMPLE_FRAME_SIZE
                }
        else:
            key = 'width'
            innerFrameArgs = {
                    'width': EXAMPLE_FRAME_SIZE,
                    'height': self.height/4
                }

        size = {key: EXAMPLE_FRAME_SIZE}

        frmBefore = tk.Frame(self.frm, bg=OTHER_COLOR, **size)
        frmBefore.pack(side=side, fill=tk.BOTH)
        self._framesToRemove.append(frmBefore)

        frmPacked = tk.Frame(self.frm, bg=INACTIVE_FRAME_COLOR, **size)
        frmPacked.pack(side=side, fill=tk.BOTH)
        frmPacked.pack_propagate(0)
        self._framesToRemove.append(frmPacked)

        frmFilled = tk.Frame(frmPacked, bg=ACTIVE_FRAME_COLOR,
                **innerFrameArgs)
        frmFilled.pack(side=side, fill=fill)
        self._framesToRemove.append(frmFilled)


class ExpandFrame(PackInfoFrame):
    def update(self, side=tk.TOP, expand=tk.FALSE):
        PackInfoFrame.update(self, side=side, expand=expand)

        self.lbl.config(text='expand={}'.format(str(expand)))

        if side in (tk.TOP, tk.BOTTOM):
            key = 'height'
            fill = tk.X
            innerFrameArgs = {
                    'width': self.width/4,
                    'height': EXAMPLE_FRAME_SIZE
                }
        else:
            key = 'width'
            fill = tk.Y
            innerFrameArgs = {
                    'width': EXAMPLE_FRAME_SIZE,
                    'height': self.height/4
                }

        size = {key: EXAMPLE_FRAME_SIZE}

        frmBefore = tk.Frame(self.frm, bg=OTHER_COLOR, **size)
        frmBefore.pack(side=side, fill=fill)
        self._framesToRemove.append(frmBefore)

        frmPacked = tk.Frame(self.frm, bg=INACTIVE_FRAME_COLOR, **size)
        frmPacked.pack(side=side, fill=tk.BOTH, expand=expand)
        frmPacked.pack_propagate(0)
        self._framesToRemove.append(frmPacked)

        frmExpanded = tk.Frame(frmPacked, bg=ACTIVE_FRAME_COLOR,
                **innerFrameArgs)
        frmExpanded.pack(side=side, expand=expand)
        self._framesToRemove.append(frmExpanded)
