from ... import Gtk
from .. import Document

class Cell(Document):
    def __init__(self, app, x, y, w="1", h="1"):
        super().__init__(app)
        self.child = None
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
    def render(self):
        return self.child.render()
    def add_child(self, child):
        self.child = child

class Grid(Document):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

    def render_raw(self):
        return Gtk.Grid()
    def attach_child(self, w, d):
        w.attach(d.render(), d.x, d.y, d.w, d.h)
