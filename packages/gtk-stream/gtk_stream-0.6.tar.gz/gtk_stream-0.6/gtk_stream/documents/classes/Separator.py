from ... import Gtk
from .. import Document

class Separator(Document):
    __g_class__ = Gtk.Separator
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
    def render_raw(self):
        return Gtk.Separator()
