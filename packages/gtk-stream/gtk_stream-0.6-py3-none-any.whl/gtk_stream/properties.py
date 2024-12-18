import sys

from . import Gtk

def _const(x):
    return lambda _: x
def _parse_orientation_property(val):
    return _const((Gtk.Orientation.HORIZONTAL) if val == "horizontal" else (Gtk.Orientation.VERTICAL))
def _parse_boolean_property(val):
    return _const(True if val == "true" else False)
def _parse_float_property(val):
    return _const(float(val))
def _parse_int_property(val):
    return _const(int(val))
def _parse_searchMode_property(val):
    match val:
        case 'exact':
            return _const(Gtk.StringFilterMatchMode.EXACT)
        case 'substring':
            return _const(Gtk.StringFilterMatchMode.SUBSTRING)
        case _:
            return _const(Gtk.StringFilterMatchMode.PREFIX)
def _parse_css_classes_property(val):
    return _const(val.split())
def _parse_widget_property(val):
    return lambda app: app.namedWidgets[val]
        
_PARSE_TYPE_PROPERTY = {
    'GStrv'                    : _parse_css_classes_property,
    'GtkOrientation'           : _parse_orientation_property,
    'gdouble'                  : _parse_float_property,
    'gfloat'                   : _parse_float_property,
    'gint'                     : _parse_int_property,
    'gboolean'                 : _parse_boolean_property,
    'GtkStringFilterMatchMode' : _parse_searchMode_property,
    'GtkWidget'                : _parse_widget_property,
    'gchararray'               : _const,
}

def parse_property(prop_type, val):
    # print(f"Parsing property '{val}' of type '{prop_type}'", file=sys.stderr)
    return _PARSE_TYPE_PROPERTY[prop_type](val)
def get_prop_type(klass, prop):
    return klass.find_property(prop).value_type.name
