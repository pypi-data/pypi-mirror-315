import sys

from . import Gtk, GLib, Gdk
from .common import printEvent
from .properties import parse_property

class GtkStreamApp(Gtk.Application):
    def __init__(self, name = None, **kwargs):
        super().__init__(**kwargs)
        if name != None:
            GLib.set_application_name(name)
        self.namedWidgets = { }
        self.namedWindows = { }
        
        self.callback_queue = []

        def run_when_idle_before_startup(cb):
            self.callback_queue.append(cb)
        self.run_when_idle = run_when_idle_before_startup
        
        def on_startup(_):
            for cb in self.callback_queue:
                GLib.idle_add(cb)
            self.run_when_idle = GLib.idle_add
        self.connect('startup', on_startup)
        
    def nameWidget(self, id, w):
        if id is not None:
            self.namedWidgets[id] = w

    def openFileDialog(self, id, parent):
        def cb():
            dialog = Gtk.FileDialog()
            dialog.props.modal = True
            def on_choose(_, b):
                try:
                    file = dialog.open_finish(b)
                    print(f"{id}:selected:{file.get_path()}")
                    sys.stdout.flush()
                except GLib.GError as e:
                    print(f"{id}:none-selected")
                    sys.stdout.flush()
                    
            dialog.open(parent = self.namedWindows[parent], callback = on_choose)
        self.run_when_idle(cb)
    def newWindow(self, document, id, title = "Window", width = None, height = None):
        def cb():
            win = Gtk.Window(application=self)
            win.set_title(title)
            if width != None and height != None:
                win.set_default_size(int(width), int(height))
            self.namedWindows[id] = win
            win.set_child(document.render())
            win.connect('close-request', printEvent('close-request', id))
            win.present()
            return False
        self.run_when_idle(cb)
    def addStyle(self, style):
        def cb():
            provider = Gtk.CssProvider()
            provider.load_from_data(style)
            Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.run_when_idle(cb)
    def closeWindow(self, id):
        def cb():
            self.namedWindows[id].close()
        self.run_when_idle(cb)
    def removeWidget(self, id):
        def cb():
            w = self.namedWidgets[id]
            w.get_parent().remove(w)
        self.run_when_idle(cb)
    def insertWidget(self, to, document):
        def cb():
            if to in self.namedWidgets:
                w = self.namedWidgets[to]
                w.insert_child(document)
            else:
                raise Exception(f"Error: unknown widget id '{to}'")
        self.run_when_idle(cb)
    def setProp(self, id, name, value):
        def cb():
            w = self.namedWidgets[id]
            w.set_property(name, parse_property(name, value))
        self.run_when_idle(cb)
