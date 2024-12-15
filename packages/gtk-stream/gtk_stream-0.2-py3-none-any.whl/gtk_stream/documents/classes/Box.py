from ... import Gtk
from .. import Document

class Box(Document):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
    def render_raw(self):
        return Gtk.Box()
    def attach_child(self, w, d):
        w.append(d.render())
