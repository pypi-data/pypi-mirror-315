import sys

from ... import Gtk
from ...common import printEvent
from .. import Document
from ...properties import parse_property

class Switch(Document):
    def __init__(self, app, id, managed = "false", **kwargs):
        super().__init__(app, id=id, **kwargs)
        self.managed = parse_property('managed', managed)
    def render_raw(self):
        ret = Gtk.Switch()
        def on_state_set(_x,new_state):
            state = "on" if new_state else "off"
            print(f"{self.id}:switch:{state}")
            sys.stdout.flush()
            return self.managed
        ret.connect('state-set', on_state_set)
        return ret
