from ... import Gtk
from .. import Document, PseudoDocument

class Stack(Document):
    __g_class__ = Gtk.Stack
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
    def render_raw(self):
        return Gtk.Stack()
    def insert_child(self, w, d):
        w.add_child(d.render())
