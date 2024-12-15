from . import Gtk

def _parse_orientation_property(val):
    return (Gtk.Orientation.HORIZONTAL) if val == "horizontal" else (Gtk.Orientation.VERTICAL)
def _parse_boolean_property(val):
    return True if val == "true" else False
def _parse_float_property(val):
    return float(val)
def _parse_int_property(val):
    return int(val)
def _parse_searchMode_property(val):
    match val:
        case 'exact':
            return Gtk.StringFilterMatchMode.EXACT
        case 'substring':
            return Gtk.StringFilterMatchMode.SUBSTRING
        case _:
            return Gtk.StringFilterMatchMode.PREFIX
def _parse_css_classes_property(val):
    return val.split()
        
_PARSE_PROPERTY = {
    'css-classes':       _parse_css_classes_property, 
    'orientation':       _parse_orientation_property,
    'fraction':          _parse_float_property,
    'show-text':         _parse_boolean_property,
    'enable-search':     _parse_boolean_property,
    'search-match-mode': _parse_searchMode_property,
    'visited':           _parse_boolean_property,
    'hexpand':           _parse_boolean_property,
    'hexpand-set':       _parse_boolean_property,
    'vexpand':           _parse_boolean_property,
    'vexpand-set':       _parse_boolean_property,
    'xalign':            _parse_float_property,
    'yalign':            _parse_float_property,
    'state':             _parse_boolean_property,
    'managed':           _parse_boolean_property
}

def parse_property(prop, val):
    return _PARSE_PROPERTY.get(prop, lambda x: x)(val)
