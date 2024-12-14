from ... import Gtk
from ...common import printEvent
from .. import Document

class Button(Document):
    def __init__(self, app, id, **kwargs):
        super().__init__(app, id = id, **kwargs)
    def render_raw(self):
        button = Gtk.Button()
        button.connect('clicked', printEvent('clicked', self.id))
        return button
    def attach_child(self, w, d):
        w.set_child(d.render())
