from ... import Gtk
from .. import Document, PseudoDocument

class FrameLabel(PseudoDocument):
    def __init__(self, app):
        super().__init__(app)

class Frame(Document):
    def __init__(self, app, **kwargs):
        super().__init__(app,**kwargs)
    def render_raw(self):
        return Gtk.Frame()
    def insert_child(self, w, d):
        if isinstance(d, FrameLabel):
            w.set_label_widget(d.render())
        else:
            w.set_child(d.render())
