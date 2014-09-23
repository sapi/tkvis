import Tkinter as tk


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
