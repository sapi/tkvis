import tkvis as tk

from src.config import cfg
from src.model.widgets import clear_highlight, highlight
from packinfo import AnchorFrame, ExpandFrame, FillFrame, SideFrame
from packlayout import PackLayoutCanvas


class TkVisualiser(tk.Toplevel):
    '''
    The top-level Tk Visualiser object.

    '''
    def __init__(self, master, *args, **kwargs):
        '''
        Create a new instance of the TkVisualiser class.

        @param tk.Widget $master
          The tk widget to create the TkVisualiser in.

        '''
        tk.Toplevel.__init__(self, master, *args, **kwargs)

        #### Change window settings
        self.title('TK Visualiser')
        self.protocol('WM_DELETE_WINDOW', self.exit)

        #### Set up the window
        ##      Left            Right
        ##
        ##    [listbox]
        ##    [listbox]        [labels]
        ## [side] [anchor]  [pack details]
        ## [fill] [expand]
        ##

        #### Left
        frmLeft = tk.Frame(self)
        frmLeft.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.BOTH)

        ## Widget Listbox
        self.lbxWidgets = tk.Listbox(frmLeft, font=cfg.LISTBOX_FONT)
        self.lbxWidgets.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)
        self.lbxWidgets.bind('<<ListboxSelect>>',
                self.lbxWidgetsSelectionChanged)

        ## Problems Listbox
        tk.Label(frmLeft, text='Errors/Warnings for Selected Widget:')\
                .pack(side=tk.TOP, pady=(10, 0))

        self.lbxProblems = tk.Listbox(frmLeft, height=5)
        self.lbxProblems.pack(side=tk.TOP, fill=tk.X)

        ## Pack Args
        frmPackArgs = tk.Frame(frmLeft)
        frmPackArgs.pack(side=tk.TOP)

        # Side and Anchor
        frmTop = tk.Frame(frmPackArgs)
        frmTop.pack(side=tk.TOP)

        self.frmSide = SideFrame(frmTop)
        self.frmSide.pack(side=tk.LEFT, padx=10, pady=10)

        self.frmAnchor = AnchorFrame(frmTop)
        self.frmAnchor.pack(side=tk.LEFT, padx=10, pady=10)

        # Fill and Expand
        frmBottom = tk.Frame(frmPackArgs)
        frmBottom.pack(side=tk.TOP)

        self.frmFill = FillFrame(frmBottom)
        self.frmFill.pack(side=tk.LEFT, padx=10, pady=10)

        self.frmExpand = ExpandFrame(frmBottom)
        self.frmExpand.pack(side=tk.LEFT, padx=10, pady=10)

        #### Right
        frmRight = tk.Frame(self)
        frmRight.pack(side=tk.LEFT)

        ## Labels
        tk.Label(frmRight,
                text='Selected Widget: {}'.format(cfg.COLORS.ACTIVE_VIEW)
            ).pack(side=tk.TOP)

        tk.Label(frmRight,
                text='Parent Widget: {}'.format(cfg.COLORS.PARENT_VIEW)
            ).pack(side=tk.TOP)

        tk.Label(frmRight,
                text='Reserved Space: {}'.format(cfg.COLORS.RESERVED_SPACE)
            ).pack(side=tk.TOP)

        ## Canvas
        self.cvsPackLayout = PackLayoutCanvas(frmRight)
        self.cvsPackLayout.pack(side=tk.TOP)

        #### Set up local vars
        self._selection = None, None  # widget, bg
        self._selectionParent = None, None

    def exit(self):
        # bring down the hosted app when we're closed
        self._objsRoot.obj.destroy()

    def lbxWidgetsSelectionChanged(self, evt):
        # get selection
        idx = self.lbxWidgets.curselection()[0]
        tkObj = self._widgets[idx]

        self._selectWidget(tkObj)

    def _selectWidget(self, tkObj):
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
        self._updateLbxWidgetsColors(tkObj)

        # update the problems listbox
        self._updateLbxProblems(tkObj)

        # update the pack args
        self.setPackArgs(tkObj)

    def setObjectTree(self, root, objs):
        self._objsRoot = root
        self._objs = objs

        self._updateLbxWidgets()
        self.lbxWidgets.selection_set(0)

        self._selectWidget(self._objsRoot)

        # Bind to the root window's configuration method
        fSelectRoot = lambda evt: self._selectWidget(self._objsRoot)
        self._objsRoot.obj.bind('<Configure>', fSelectRoot)

    def _updateLbxWidgets(self):
        self.lbxWidgets.delete(0, tk.END)

        self._widgets = list(self._objsRoot)

        # doing this the lazy way for now: __str__ on a tree object is defined
        # to print out a nice pretty tree :)
        for line in str(self._objsRoot).splitlines():
            self.lbxWidgets.insert(tk.END, line)

    def _updateLbxWidgetsColors(self, tkObj):
        for idx,elem in enumerate(self._widgets):
            # text color, set to match highlight colours
            if elem == tkObj:
                self.lbxWidgets.itemconfig(idx,
                        selectforeground=cfg.COLORS.ACTIVE_VIEW)
            elif elem == tkObj.parent:
                self.lbxWidgets.itemconfig(idx, fg=cfg.COLORS.PARENT_VIEW)
            else:
                self.lbxWidgets.itemconfig(idx, fg='black')

            # background color, if not packed
            if elem.errors:
                self.lbxWidgets.itemconfig(idx, bg=cfg.COLORS.ERROR)
            elif elem.warnings:
                self.lbxWidgets.itemconfig(idx, bg=cfg.COLORS.WARNING)

    def _updateLbxProblems(self, tkObj):
        self.lbxProblems.delete(0, tk.END)

        for desc in tkObj.errors:
            self.lbxProblems.insert(tk.END, desc)
            self.lbxProblems.itemconfig(tk.END, fg=cfg.COLORS.ERROR)

        for desc in tkObj.warnings:
            self.lbxProblems.insert(tk.END, desc)
            self.lbxProblems.itemconfig(tk.END, fg=cfg.COLORS.WARNING)

    def setPackArgs(self, tkObj):
        # Update our pack argument visualisations
        side = tkObj.packArgs.side
        anchor = tkObj.packArgs.anchor
        fill = tkObj.packArgs.fill
        expand = tkObj.packArgs.expand

        self.frmSide.update(side)
        self.frmAnchor.update(side, anchor)
        self.frmFill.update(side, fill)
        self.frmExpand.update(side, expand)

        # Now update our canvas, which shows the actual location of things in
        # the attached program
        window = self._objsRoot.obj
        sw = window.winfo_width()
        sh = window.winfo_height()

        self.cvsPackLayout.config(width=sw, height=sh)
        self.cvsPackLayout.redraw(tkObj, self._objsRoot)


def create_gui(root):
    '''
    Create and configure the GUI.

    @param tk.Widget $root
      The root Tk object.

    @retval TkVisualiser
      The configured TkVisualiser instance.

    '''
    window = TkVisualiser(root)

    return window
