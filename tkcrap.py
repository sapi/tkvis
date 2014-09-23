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
            innerSize = {
                    'height': EXAMPLE_FRAME_SIZE,
                    'width': width/4,
                }
            size = {'height': EXAMPLE_FRAME_SIZE}

            fill = tk.X
            axis = ArrowCanvas.Y
        else:
            innerSize = {
                    'width': EXAMPLE_FRAME_SIZE,
                    'height': height/4,
                }
            size = {'width': EXAMPLE_FRAME_SIZE}

            fill = tk.Y
            axis = ArrowCanvas.X

        frmBefore = tk.Frame(frmSide.inner, bg=OTHER_COLOR, **size)
        frmBefore.pack(side=side, fill=fill)

        frmPacked = tk.Frame(frmSide.inner, bg=ACTIVE_FRAME_COLOR, **innerSize)
        frmPacked.pack(side=side)

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


class FillFrame(tk.Frame):
    def __init__(self, master, side, fill, width=100, height=100, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        lbl = tk.Label(self, text='fill={}'.format(fill.upper()))
        lbl.pack(side=tk.TOP)

        frmFill = BorderedFrame(self, bd=2, width=width, height=height)
        frmFill.pack(side=tk.TOP)
        frmFill.pack_propagate(0)

        if side in (tk.TOP, tk.BOTTOM):
            key = 'height'
            innerFrameArgs = {'width': width/4, 'height': EXAMPLE_FRAME_SIZE}
        else:
            key = 'width'
            innerFrameArgs = {'width': EXAMPLE_FRAME_SIZE, 'height': height/4}

        size = {key: EXAMPLE_FRAME_SIZE}

        frmBefore = tk.Frame(frmFill.inner, bg=OTHER_COLOR, **size)
        frmBefore.pack(side=side, fill=tk.BOTH)

        frmPacked = tk.Frame(frmFill.inner, bg=INACTIVE_FRAME_COLOR, **size)
        frmPacked.pack(side=side, fill=tk.BOTH)
        frmPacked.pack_propagate(0)

        frmFilled = tk.Frame(frmPacked, bg=ACTIVE_FRAME_COLOR,
                **innerFrameArgs)
        frmFilled.pack(side=side, fill=fill)


class ExpandFrame(tk.Frame):
    def __init__(self, master, side, expand, width=100, height=100, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        lbl = tk.Label(self, text='expand={}'.format(str(expand)))
        lbl.pack(side=tk.TOP)

        frmExpand = BorderedFrame(self, bd=2, width=width, height=height)
        frmExpand.pack(side=tk.TOP)
        frmExpand.pack_propagate(0)

        if side in (tk.TOP, tk.BOTTOM):
            key = 'height'
            fill = tk.X
            innerFrameArgs = {'width': width/4, 'height': EXAMPLE_FRAME_SIZE}
        else:
            key = 'width'
            fill = tk.Y
            innerFrameArgs = {'width': EXAMPLE_FRAME_SIZE, 'height': height/4}

        size = {key: EXAMPLE_FRAME_SIZE}

        frmBefore = tk.Frame(frmExpand.inner, bg=OTHER_COLOR, **size)
        frmBefore.pack(side=side, fill=fill)

        frmPacked = tk.Frame(frmExpand.inner, bg=INACTIVE_FRAME_COLOR, **size)
        frmPacked.pack(side=side, fill=tk.BOTH, expand=expand)
        frmPacked.pack_propagate(0)

        frmExpanded = tk.Frame(frmPacked, bg=ACTIVE_FRAME_COLOR,
                **innerFrameArgs)
        frmExpanded.pack(side=side, expand=expand)
