from ... import Gtk
from .. import Document

class Frame(Document):
    def __init__(self, app, label=None, **kwargs):
        super().__init__(app,**kwargs)
        self.label = label
    def render_raw(self):
        ret = Gtk.Frame()
        if self.label != None:
            ret.set_label(self.label)
        return ret
    def attach_child(self, w, d):
        w.set_child(d.render())
