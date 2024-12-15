import sys
from ...properties import parse_property

class Document:
    def __init__(self, app, id = None, **attrs):
        self.id = id
        self.app = app
        self.props = { attr: parse_property(attr, val) for (attr, val) in attrs.items() }
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        
    def render_raw(self):
        """Method to render the document to a widet"""
        raise Exception("Method 'render' not implemented")
    def set_properties(self, w):
        self.app.nameWidget(self.id, w)
        for (p,v) in self.props.items():
            w.set_property(p, v)
        w.attach_child = lambda d: self.attach_child(w, d)
    def render(self):
        w = self.render_raw()
        self.set_properties(w)
        for child in self.children:
            self.attach_child(w, child)
        return w
    
    def attach_child(self, w, child):
        raise Exception("Unimplemented method 'attach_child'")
