from ... import Gtk
from .. import Document

class Paned(Document):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
    def render(self):
        if len(self.children) == 1:
            return self.children[0].render()
        
        l = self.children[0].render()
        for (r,rem_size) in zip(self.children[1:], range(len(self.children),1,-1)):
            j = Gtk.Paned()
            j.set_shrink_start_child(False)
            j.set_shrink_end_child(False)
            j.props.start_child = l
            j.props.end_child = r.render()
            self.set_properties(j)
            l = j
        return l
