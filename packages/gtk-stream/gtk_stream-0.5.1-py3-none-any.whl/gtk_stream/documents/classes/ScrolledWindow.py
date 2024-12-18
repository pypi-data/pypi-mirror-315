from ... import Gtk
from .. import Document

class ScrolledWindow(Document):
    __g_class__ = Gtk.ScrolledWindow
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
    def render_raw(self):
        return Gtk.ScrolledWindow()
    def insert_child(self, w, d):
        w.set_child(d.render())
