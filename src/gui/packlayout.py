import tkvis as tk

from src.config import cfg


class PackLayoutCanvas(tk.Canvas):
    def redraw(self, tkObj, rootTkObj):
        # grab necessary info
        side = tkObj.packArgs.side

        window = rootTkObj.obj
        sw = window.winfo_width()
        sh = window.winfo_height()

        # first, clear out the canvas with a recognisable colour
        self.delete(tk.ALL)

        self.create_rectangle(
                0, 0,
                sw, sh,
                fill='gray',
                outline='gray',
            )

        # draw the parent, if necessary
        if tkObj.parent is not None:
            self._drawWidget(tkObj.parent, rootTkObj, cfg.COLORS.PARENT_VIEW)

        # draw the packed space on this guy
        self._drawPackedSpace(tkObj, rootTkObj, cfg.COLORS.RESERVED_SPACE,
                side=side)

        # draw all of the filled space from views packed before this one
        # at the same level (in other words, the space from the parent)
        if tkObj.parent is not None:
            for child in tkObj.parent.children:
                if child is tkObj:
                    break

                childSide = child.packArgs.get('side', tk.TOP)
                self._drawPackedSpace(child, rootTkObj, cfg.COLORS.PARENT_VIEW,
                        side=childSide)

        # and finally we draw the object itself on top
        self._drawWidget(tkObj, rootTkObj, cfg.COLORS.ACTIVE_VIEW)

    def _drawWidget(self, tkObj, rootTkObj, color):
        sx = rootTkObj.obj.winfo_rootx()
        sy = rootTkObj.obj.winfo_rooty()

        x = tkObj.obj.winfo_rootx() - sx
        y = tkObj.obj.winfo_rooty() - sy
        w = tkObj.obj.winfo_width()
        h = tkObj.obj.winfo_height()

        self.create_rectangle(
                x, y,
                x + w, y + h,
                fill=color,
                outline=color,
            )

    def _drawPackedSpace(self, tkObj, rootTkObj, color, side=tk.TOP):
        sx = rootTkObj.obj.winfo_rootx()
        sy = rootTkObj.obj.winfo_rooty()

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
                self.create_rectangle(
                        vx, py,
                        vx + vw, py + ph,
                        fill=color,
                        outline=color,
                    )
            else:
                self.create_rectangle(
                        px, vy,
                        px + pw, vy + vh,
                        fill=color,
                        outline=color,
                    )
