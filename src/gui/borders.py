import tkvis as tk


class BorderedFrame(tk.Frame):
    def __init__(self, master, bd=0, col='black', **kwargs):
        tk.Frame.__init__(self, master, bd=bd, bg=col,
                **{k: v for k,v in kwargs.iteritems() if k not in ('bd', 'bg')}
            )

        self.inner = tk.Frame(self, **kwargs)
        self.inner.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
