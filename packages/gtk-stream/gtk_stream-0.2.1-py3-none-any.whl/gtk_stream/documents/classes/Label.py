from ... import Gtk
from .. import Document

class Label(Document):
    def __init__(self, app, text, **kwargs):
        super().__init__(app, **kwargs)
        self.text = text
    def render_raw(self):
        l = Gtk.Label()
        l.set_text(self.text)
        return l
