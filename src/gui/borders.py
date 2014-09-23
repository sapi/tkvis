import tkvis as tk


class BorderedFrame(tk.Frame):
    '''
    A tk.Frame with a border.

    '''
    def __init__(self, master, bd=0, col='black', **kwargs):
        '''
        Create a new instance of the BorderedFrame class.

        @param tk.Widget $master
          The tk widget to create the BorderedFrame in.

        @param int $bd [optional]
          The border width.  Defaults to 0.
        @param str $col [optional]
          The border color.  Defaults to black.

        '''
        tk.Frame.__init__(self, master, bd=bd, bg=col,
                **{k: v for k,v in kwargs.iteritems() if k not in ('bd', 'bg')}
            )

        self.inner = tk.Frame(self, **kwargs)
        self.inner.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
