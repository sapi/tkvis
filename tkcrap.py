import tkvis as tk


ACTIVE_FRAME_COLOR = 'red'
INACTIVE_FRAME_COLOR = 'green'
OTHER_COLOR = 'gray'
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

    def __init__(self, master, axis, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)

        assert axis in (ArrowCanvas.X, ArrowCanvas.Y)
        self.axis = axis

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

        points = [
                (perpendicular/2 - ARROW_WIDTH/2, ARROW_HEIGHT),
                (perpendicular/2, 0),
                (perpendicular/2 + ARROW_WIDTH/2, ARROW_HEIGHT),
                (perpendicular/2 + LINE_WIDTH/2, ARROW_HEIGHT),
                (perpendicular/2 + LINE_WIDTH/2, h),
                (perpendicular/2 - LINE_WIDTH/2, h),
                (perpendicular/2 - LINE_WIDTH/2, ARROW_HEIGHT),
            ]

        if self.axis == ArrowCanvas.X:
            points = [(y,x) for x,y in points]

        self.create_polygon(points)

        if self.axis == ArrowCanvas.X:
            self.create_line(0, h/2, 1, h/2)
        else:
            self.create_line(w/2, 0, w/2, 1)


class SideFrame(tk.Frame):
    def __init__(self, master, side, width=100, height=100, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        lbl = tk.Label(self, text='side={}'.format(side.upper()))
        lbl.pack(side=tk.TOP)

        frmSide = BorderedFrame(self, bd=2, width=width, height=height)
        frmSide.pack(side=tk.TOP)
        frmSide.pack_propagate(0)

        if side in (tk.TOP, tk.BOTTOM):
            key = 'height'
            fill = tk.X
            axis = ArrowCanvas.Y
        else:
            key = 'width'
            fill = tk.Y
            axis = ArrowCanvas.X

        size = {key: EXAMPLE_FRAME_SIZE}

        frmBefore = tk.Frame(frmSide.inner, bg=OTHER_COLOR, **size)
        frmBefore.pack(side=side, fill=fill)

        frmPacked = tk.Frame(frmSide.inner, bg=ACTIVE_FRAME_COLOR, **size)
        frmPacked.pack(side=side, fill=fill)

        cvsArrow = ArrowCanvas(frmSide.inner, axis)
        cvsArrow.pack(side=side)


class AnchorFrame(tk.Frame):
    def __init__(self, master, side, anchor, width=100, height=100, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        lbl = tk.Label(self, text='anchor={}'.format(anchor.upper()))
        lbl.pack(side=tk.TOP)

        frmAnchor = BorderedFrame(self, bd=2, width=width, height=height)
        frmAnchor.pack(side=tk.TOP)
        frmAnchor.pack_propagate(0)

        if side in (tk.TOP, tk.BOTTOM):
            key = 'height'
            fill = tk.X
            innerFrameArgs = {'width': width/4, 'height': EXAMPLE_FRAME_SIZE}
        else:
            key = 'width'
            fill = tk.Y
            innerFrameArgs = {'width': EXAMPLE_FRAME_SIZE, 'height': height/4}

        size = {key: EXAMPLE_FRAME_SIZE}

        frmBefore = tk.Frame(frmAnchor.inner, bg=OTHER_COLOR, **size)
        frmBefore.pack(side=side, fill=fill)

        frmPacked = tk.Frame(frmAnchor.inner, bg=INACTIVE_FRAME_COLOR, **size)
        frmPacked.pack(side=side, fill=fill)
        frmPacked.pack_propagate(0)

        frmAnchored = tk.Frame(frmPacked, bg=ACTIVE_FRAME_COLOR,
                **innerFrameArgs)
        frmAnchored.pack(side=side, anchor=anchor)
