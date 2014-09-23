import tkvis as tk

from src.config import cfg
from arrows import ArrowCanvas
from borders import BorderedFrame


class PackInfoFrame(tk.Frame):
    '''
    A frame for displaying information about a specific pack argument.

    Contains a descriptive label, and a bordered frame for drawing in.

    Subclasses must override .update with appropriate keyword arguments.

    '''
    def __init__(self, master, width=cfg.PACKINFO.WIDTH,
            height=cfg.PACKINFO.HEIGHT, **kwargs):
        '''
        Create a new instance of the PackInfoFrame class.

        @param tk.Widget $master
          The tk widget to create the PackInfoFrame in.

        @param int $width [optional]
          The width of the frame.  This defaults to the value given in the
          config file.
        @param int $height [optional]
          The height of the frame.  This defaults to the value given in the
          config file.

        '''
        tk.Frame.__init__(self, master, **kwargs)

        self.lbl = tk.Label(self)
        self.lbl.pack(side=tk.TOP)

        frm = BorderedFrame(self, bd=2, width=width, height=height)
        frm.pack(side=tk.TOP)
        frm.pack_propagate(0)

        self.frm = frm.inner

        self.width = width
        self.height = height

        self._viewsToRemove = []

    def update(self, **kwargs):
        '''
        Update the pack info.

        Subclasses will override with appropiate arguments and will create
        all necessary subviews.

        The default implementation simply destroys all views marked for
        removal.  It is assumed that subclasses will call this implementation.

        '''
        for frm in self._viewsToRemove:
            frm.destroy()

        self._viewsToRemove = []


class SideFrame(PackInfoFrame):
    def update(self, side=tk.TOP):
        PackInfoFrame.update(self, side=side)

        self.lbl.config(text='side={}'.format(side.upper()))

        if side in (tk.TOP, tk.BOTTOM):
            innerSize = {
                    'height': cfg.PACKINFO.DUMMY_SIZE,
                    'width': self.width/4,
                }
            size = {'height': cfg.PACKINFO.DUMMY_SIZE}

            fill = tk.X
            axis = ArrowCanvas.Y
        else:
            innerSize = {
                    'width': cfg.PACKINFO.DUMMY_SIZE,
                    'height': self.height/4,
                }
            size = {'width': cfg.PACKINFO.DUMMY_SIZE}

            fill = tk.Y
            axis = ArrowCanvas.X

        flip = side in (tk.BOTTOM, tk.RIGHT)

        frmBefore = tk.Frame(self.frm, bg=cfg.COLORS.DUMMY_FRAME, **size)
        frmBefore.pack(side=side, fill=fill)
        self._viewsToRemove.append(frmBefore)

        frmPacked = tk.Frame(self.frm, bg=cfg.COLORS.ACTIVE_VIEW, **innerSize)
        frmPacked.pack(side=side)
        self._viewsToRemove.append(frmPacked)

        cvsArrow = ArrowCanvas(self.frm, axis, flip=flip)
        cvsArrow.pack(side=side)
        self._viewsToRemove.append(cvsArrow)


class AnchorFrame(PackInfoFrame):
    def update(self, side=tk.TOP, anchor=tk.CENTER):
        PackInfoFrame.update(self, side=side, anchor=anchor)

        self.lbl.config(text='anchor={}'.format(anchor.upper()))

        if side in (tk.TOP, tk.BOTTOM):
            key = 'height'
            fill = tk.X
            innerFrameArgs = {
                    'width': self.width/4,
                    'height': cfg.PACKINFO.DUMMY_SIZE
                }
        else:
            key = 'width'
            fill = tk.Y
            innerFrameArgs = {
                    'width': cfg.PACKINFO.DUMMY_SIZE,
                    'height': self.height/4
                }

        size = {key: cfg.PACKINFO.DUMMY_SIZE}

        frmBefore = tk.Frame(self.frm, bg=cfg.COLORS.DUMMY_FRAME, **size)
        frmBefore.pack(side=side, fill=fill)
        self._viewsToRemove.append(frmBefore)

        frmPacked = tk.Frame(self.frm, bg=cfg.COLORS.DUMMY_BACKGROUND, **size)
        frmPacked.pack(side=side, fill=fill)
        frmPacked.pack_propagate(0)
        self._viewsToRemove.append(frmPacked)

        frmAnchored = tk.Frame(frmPacked, bg=cfg.COLORS.ACTIVE_VIEW,
                **innerFrameArgs)
        frmAnchored.pack(side=side, anchor=anchor)
        self._viewsToRemove.append(frmAnchored)


class FillFrame(PackInfoFrame):
    def update(self, side=tk.TOP, fill=tk.NONE):
        PackInfoFrame.update(self, side=side, fill=fill)

        self.lbl.config(text='fill={}'.format(fill.upper()))

        if side in (tk.TOP, tk.BOTTOM):
            key = 'height'
            innerFrameArgs = {
                    'width': self.width/4,
                    'height': cfg.PACKINFO.DUMMY_SIZE
                }
        else:
            key = 'width'
            innerFrameArgs = {
                    'width': cfg.PACKINFO.DUMMY_SIZE,
                    'height': self.height/4
                }

        size = {key: cfg.PACKINFO.DUMMY_SIZE}

        frmBefore = tk.Frame(self.frm, bg=cfg.COLORS.DUMMY_FRAME, **size)
        frmBefore.pack(side=side, fill=tk.BOTH)
        self._viewsToRemove.append(frmBefore)

        frmPacked = tk.Frame(self.frm, bg=cfg.COLORS.DUMMY_BACKGROUND, **size)
        frmPacked.pack(side=side, fill=tk.BOTH)
        frmPacked.pack_propagate(0)
        self._viewsToRemove.append(frmPacked)

        frmFilled = tk.Frame(frmPacked, bg=cfg.COLORS.ACTIVE_VIEW,
                **innerFrameArgs)
        frmFilled.pack(side=side, fill=fill)
        self._viewsToRemove.append(frmFilled)


class ExpandFrame(PackInfoFrame):
    def update(self, side=tk.TOP, expand=tk.FALSE):
        PackInfoFrame.update(self, side=side, expand=expand)

        self.lbl.config(text='expand={}'.format(str(expand)))

        if side in (tk.TOP, tk.BOTTOM):
            key = 'height'
            fill = tk.X
            innerFrameArgs = {
                    'width': self.width/4,
                    'height': cfg.PACKINFO.DUMMY_SIZE
                }
        else:
            key = 'width'
            fill = tk.Y
            innerFrameArgs = {
                    'width': cfg.PACKINFO.DUMMY_SIZE,
                    'height': self.height/4
                }

        size = {key: cfg.PACKINFO.DUMMY_SIZE}

        frmBefore = tk.Frame(self.frm, bg=cfg.COLORS.DUMMY_FRAME, **size)
        frmBefore.pack(side=side, fill=fill)
        self._viewsToRemove.append(frmBefore)

        frmPacked = tk.Frame(self.frm, bg=cfg.COLORS.DUMMY_BACKGROUND, **size)
        frmPacked.pack(side=side, fill=tk.BOTH, expand=expand)
        frmPacked.pack_propagate(0)
        self._viewsToRemove.append(frmPacked)

        frmExpanded = tk.Frame(frmPacked, bg=cfg.COLORS.ACTIVE_VIEW,
                **innerFrameArgs)
        frmExpanded.pack(side=side, expand=expand)
        self._viewsToRemove.append(frmExpanded)
