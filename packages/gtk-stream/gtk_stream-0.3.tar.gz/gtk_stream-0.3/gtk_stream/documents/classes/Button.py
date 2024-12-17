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
    def insert_child(self, w, d):
        w.set_child(d.render())

class LinkButton(Button):
    def __init__(self, app, id, **kwargs):
        super().__init__(app, id=id, **kwargs)
    def render_raw(self):
        button = Gtk.LinkButton()
        button.connect('activate-link', printEvent('clicked', self.id, True))
        return button
    def insert_child(self, w, d):
        w.set_child(d.render())
