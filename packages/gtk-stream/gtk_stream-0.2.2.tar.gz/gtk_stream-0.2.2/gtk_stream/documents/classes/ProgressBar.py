from ... import Gtk
from .. import Document

class ProgressBar(Document):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
    def render_raw(self):
        return Gtk.ProgressBar()
