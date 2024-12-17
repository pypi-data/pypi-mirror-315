from ... import Gtk
from .. import Document, PseudoDocument

class Cell(PseudoDocument):
    def __init__(self, app, x, y, w="1", h="1"):
        super().__init__(app)
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)

class Grid(Document):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

    def render_raw(self):
        return Gtk.Grid()
    def insert_child(self, w, d):
        w.attach(d.render(), d.x, d.y, d.w, d.h)
