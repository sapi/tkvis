from tkvis import *


class SampleApp(object):
    def __init__(self, master):
        self._master = master
        master.title("Hello!")
        master.minsize(430, 200)

        self._lbl = Label(master, text="Choose a button")
        self._lbl.pack(side=TOP, expand=1)

        frm = Frame(master)
        frm.pack(side=TOP)

        btn = Button(frm, text="Click Me!", command=self.say_hello)
        btn.pack(side=LEFT, anchor=N)

        btn = Button(frm, text="Click Me!", command=self.say_hello)
        btn.pack(side=LEFT)

    def say_hello(self):
        print 'Hello! Thanks for clicking!'


if __name__ == "__main__":
    root = Tk()
    app = SampleApp(root)
    root.mainloop()
