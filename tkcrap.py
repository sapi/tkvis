import tkvis as tk


ACTIVE_FRAME_COLOR = 'red'
INACTIVE_FRAME_COLOR = 'gray80'
OTHER_COLOR = 'gray60'
EXAMPLE_FRAME_SIZE = 20


class BorderedFrame(tk.Frame):
    def __init__(self, master, bd=0, col='black', **kwargs):
        tk.Frame.__init__(self, master, bd=bd, bg=col,
                **{k: v for k,v in kwargs.iteritems() if k not in ('bd', 'bg')}
            )

        self.inner = tk.Frame(self, **kwargs)
        self.inner.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)


class ArrowCanvas(tk.Canvas):
    X = 'X'
    Y = 'Y'

    def __init__(self, master, axis, flip=False, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)

        assert axis in (ArrowCanvas.X, ArrowCanvas.Y)
        self.axis = axis
        self.flip = flip

        self.bind("<Configure>", self.resize)

    def resize(self, evt):
        self.delete(tk.ALL)

        w = self.winfo_width()
        h = self.winfo_height()

        parallel = h if self.axis == ArrowCanvas.Y else w
        perpendicular = w if self.axis == ArrowCanvas.Y else h

        ARROW_HEIGHT = int(0.3*parallel)
        ARROW_WIDTH = int(0.2*perpendicular)
        LINE_WIDTH = int(0.05*perpendicular)
        TOP_MARGIN = 5

        points = [
                (perpendicular/2 - ARROW_WIDTH/2, ARROW_HEIGHT),
                (perpendicular/2, TOP_MARGIN),
                (perpendicular/2 + ARROW_WIDTH/2, ARROW_HEIGHT),
                (perpendicular/2 + LINE_WIDTH/2, ARROW_HEIGHT),
                (perpendicular/2 + LINE_WIDTH/2, h),
                (perpendicular/2 - LINE_WIDTH/2, h),
                (perpendicular/2 - LINE_WIDTH/2, ARROW_HEIGHT),
            ]

        if self.flip:
            points = [(par,parallel - perp) for par,perp in points]

        if self.axis == ArrowCanvas.X:
            points = [(y,x) for x,y in points]

        self.create_polygon(points)

        if self.axis == ArrowCanvas.X:
            self.create_line(0, h/2, 1, h/2)
        else:
            self.create_line(w/2, 0, w/2, 1)


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
