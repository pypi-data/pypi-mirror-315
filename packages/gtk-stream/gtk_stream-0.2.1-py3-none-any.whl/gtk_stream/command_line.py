import io
import xml.sax as sax
import signal

from .parser import GtkStreamXMLHandler

def main():
    handler = GtkStreamXMLHandler()
    parser = sax.make_parser()
    parser.setContentHandler(handler)
    try:
        parser.parse(io.FileIO(0, 'r', closefd=False))
    finally:
        handler.app.release()
