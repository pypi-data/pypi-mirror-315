import sys
from ... import Gtk
from .. import Document

class Picture(Document):
    __g_class__ = Gtk.Picture
    def __init__(self, app, src, **kwargs):
        super().__init__(app, **kwargs)
        self.src = src
    def render_raw(self):
        return Gtk.Picture.new_for_filename(self.src)
