from ... import Gtk
from .. import Document, PseudoDocument

class BoxPrepend(PseudoDocument):
    def __init__(self, app, after = None):
        super().__init__(app)
        self.after = after

class Box(Document):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
    def render_raw(self):
        return Gtk.Box()
    def insert_child(self, w, d):
        if isinstance(d, BoxPrepend):
            if d.after != None:
                w.insert_child_after(d.render(), self.app.namedWidgets[d.after])
            else:
                w.prepend(d.render())
        else:
            w.append(d.render())
