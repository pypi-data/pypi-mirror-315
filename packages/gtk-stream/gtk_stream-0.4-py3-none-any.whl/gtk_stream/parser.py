import threading
import signal
import sys
import xml.sax as sax

from . import GLib
from . import documents as docs

from .application import GtkStreamApp

class _Object:
    pass
   
WIDGET_DOCUMENTS = {
    'progress-bar' : docs.ProgressBar,
    'label'        : docs.Label,
    'box'          : docs.Box,
    'box-prepend'  : docs.BoxPrepend,
    'button'       : docs.Button,
    'dropdown'     : docs.Dropdown,
    'item'         : docs.Item,
    'paned'        : docs.Paned,
    'grid'         : docs.Grid,
    'cell'         : docs.Cell,
    'frame'        : docs.Frame,
    'frame-label'  : docs.FrameLabel,
    'link'         : docs.LinkButton,
    'switch'       : docs.Switch,
    'picture'      : docs.Picture
}

class GtkStreamXMLHandler(sax.ContentHandler):
    def __init__(self):
        self.transition_enter = self.transE_conn
        self.transition_leave = self.transL_final
        self.transition_chars = self.ignore_chars
        self.namedWidgets = { }
        self.windows = { }

    def setNamed(self, attrs, ):
        if 'id' in attrs:
            self.namedWidgets[attrs['id']] = widget
    def ignore_chars(self, s):
        pass
        
    def transE_final(self, name, attrs):
        raise Exception(f"Unexpected tag '{name}'")
    def transL_final(self, name):
        raise Exception(f"Unexpected end tag '{name}'")
    def transL_tag(self, tag, enter, leave_parent, leave = None):
        def ret(name):
            if name == tag:
                if leave != None:
                    leave()
                self.transition_enter = enter
                self.transition_leave = leave_parent
            else:
                raise Exception(f"Error: expected end tag '{tag}', got '{name}'")
        return ret
                               
    def transE_conn(self, name, attrs):
        match name:
            case 'application':
                self.app = GtkStreamApp(**attrs)
                def on_activate(a):
                    a.hold()
                self.app.connect('activate', on_activate)
                def appMain():
                    self.app.run([])
                threading.Thread(target = appMain).start()
                def on_sigint(a,b):
                    def cb():
                        self.app.quit()
                        sys.exit(0)
                    GLib.idle_add(cb)
                signal.signal(signal.SIGINT, on_sigint)
                self.transition_enter = self.transE_message
                self.transition_leave = self.transL_tag('application', self.transE_final, self.transL_final)
            case _:
                raise Exception("Error: expected 'application' tag")
    def transE_message(self, name, attrs):
        leave_parent = self.transition_leave
        match name:
            case 'style':
                style = _Object()
                style.chars = []
                def onchars(s):
                    style.chars.append(s)
                def leave():
                    self.transition_chars = self.ignore_chars
                    self.app.addStyle(" ".join(style.chars))
                self.transition_chars = onchars
                self.transition_enter = self.transE_final
                self.transition_leave = self.transL_tag('style', self.transE_message, leave_parent, leave)
                
            case 'window':
                if 'id' in attrs:
                    store = _Object()
                    def leave():
                        self.app.newWindow(store.child, **attrs)
                    def setChild(c):
                        store.child = c
                    self.transition_enter = self.transE_addChild(setChild)
                    self.transition_leave = self.transL_tag('window', self.transE_message, leave_parent, leave)
                else:
                    raise Exception("Error: expected attribute 'id' in 'window' tag")
                
            case 'file-dialog':
                id = attrs.get('id')
                parent = attrs.get('parent')
                if id != None and parent != None:
                    self.app.openFileDialog(id, parent)
                    self.transition_enter = self.transE_final
                    self.transition_leave = self.transL_tag('file-dialog', self.transE_message, leave_parent)
                else:
                    raise Exception("Error: expected 'id' and 'parent' attributes on 'file-chooser'")

            case 'close-window':
                if 'id' in attrs:
                    def leave():
                        self.app.closeWindow(attrs['id'])
                    self.transition_enter = self.transE_final
                    self.transition_leave = self.transL_tag('close-window', self.transE_message, leave_parent, leave)
                else:
                    raise Exception("Error: expected 'id' attribute in 'close-window' tag")

            case 'set-prop':
                self.app.setProp(**attrs)
                self.transition_enter = self.transE_final
                self.transition_leave = self.transL_tag('set-prop', self.transE_message, leave_parent)
                
            case 'insert':
                if 'into' in attrs:
                    children = []
                    def leave():
                        for child in children:
                            self.app.insertWidget(attrs['into'], child)
                    self.transition_enter = self.transE_addChild(lambda child: children.append(child))
                    self.transition_leave = self.transL_tag('insert', self.transE_message, leave_parent, leave)
                else:
                    raise Exception("Expected 'to' attribute of 'append' message")

            case 'remove':
                if 'id' in attrs:
                    def leave():
                        self.app.removeWidget(attrs['id'])
                    self.transition_enter = self.transE_final
                    self.transition_leave = self.transL_tag('remove', self.transE_message, leave_parent, leave)
                else:
                    raise Exception("Expected 'id' attribute of 'remove' message")

            case _:
                raise Exception(f"Error: unknown message '{name}'")

    def transE_addChild(self, addChild):
        def ret(name, attrs):
            leave_parent = self.transition_leave
            doc_class = WIDGET_DOCUMENTS.get(name)
            if doc_class != None:
                doc = doc_class(self.app, **attrs)
                addChild(doc)
                self.transition_enter = self.transE_addChild(lambda child: doc.add_child(child))
                self.transition_leave = self.transL_tag(name, self.transE_addChild(addChild), leave_parent)
            else:
                raise Exception(f"Error: Unknown widget {name}")
        return ret

    def characters(self, s):
        self.transition_chars(s)
    def startElement(self, name, attrs):
        self.transition_enter(name, attrs)
    def endElement(self, name):
        self.transition_leave(name)
