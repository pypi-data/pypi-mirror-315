from ... import Gtk
from ...common import printEvent
from .. import Document
from ...properties import parse_property

class Switch(Document):
    __g_class__ = Gtk.Switch
    def __init__(self, app, id, managed = "false", **kwargs):
        super().__init__(app, id=id, **kwargs)
        self.managed = parse_property('gboolean', managed)(app)
    def render_raw(self):
        ret = Gtk.Switch()
        ret.connect('state-set', printEvent('switch', self.id,
                                            retval = self.managed,
                                            get_data = lambda _,state: "on" if state else "off"))
        return ret
