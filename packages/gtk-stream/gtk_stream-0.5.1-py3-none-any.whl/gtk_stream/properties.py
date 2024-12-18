import sys

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
        
_PARSE_TYPE_PROPERTY = {
    'GStrv'                    : _parse_css_classes_property,
    'GtkOrientation'           : _parse_orientation_property,
    'gdouble'                  : _parse_float_property,
    'gfloat'                   : _parse_float_property,
    'gint'                     : _parse_int_property,
    'gboolean'                 : _parse_boolean_property,
    'GtkStringFilterMatchMode' : _parse_searchMode_property
}

def parse_property(prop_type, val):
    # print(f"Parsing property '{val}' of type '{prop_type}'", file=sys.stderr)
    return _PARSE_TYPE_PROPERTY.get(prop_type, lambda x: x)(val)
def get_prop_type(klass, prop):
    return klass.find_property(prop).value_type.name
