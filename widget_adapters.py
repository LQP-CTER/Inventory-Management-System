import ttkbootstrap as tb

class MyButton(tb.Button):
    def __init__(self, master=None, **kw):
        kw.pop('bg', None)
        kw.pop('fg', None)
        kw.pop('activebackground', None)
        kw.pop('activeforeground', None)
        kw.pop('font', None)
        kw.pop('bd', None)
        kw.pop('relief', None)
        kw.pop('highlightthickness', None)
        super().__init__(master, **kw)

class MyLabel(tb.Label):
    def __init__(self, master=None, **kw):
        kw.pop('bg', None)
        kw.pop('fg', None)
        kw.pop('bd', None)
        kw.pop('relief', None)
        kw.pop('highlightthickness', None)
        super().__init__(master, **kw)

class MyFrame(tb.Frame):
    def __init__(self, master=None, **kw):
        kw.pop('bg', None)
        kw.pop('bd', None)
        kw.pop('relief', None)
        kw.pop('highlightthickness', None)
        kw.pop('padx', None)
        kw.pop('pady', None)
        super().__init__(master, **kw)

class MyEntry(tb.Entry):
    def __init__(self, master=None, **kw):
        kw.pop('bg', None)
        kw.pop('fg', None)
        kw.pop('font', None)
        kw.pop('bd', None)
        kw.pop('relief', None)
        kw.pop('highlightthickness', None)
        super().__init__(master, **kw)

class MyToplevel(tb.Toplevel):
    def __init__(self, master=None, **kw):
        kw.pop('bg', None)
        super().__init__(master, **kw)

class MyLabelFrame(tb.Labelframe):
    def __init__(self, master=None, **kw):
        kw.pop('bg', None)
        kw.pop('fg', None)
        kw.pop('font', None)
        kw.pop('bd', None)
        kw.pop('relief', None)
        super().__init__(master, **kw)

class MyCanvas(tb.Canvas):
    def __init__(self, master=None, **kw):
        kw.pop('bg', None)
        kw.pop('bd', None)
        kw.pop('relief', None)
        super().__init__(master, **kw)
