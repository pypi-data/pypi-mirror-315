import sys

def _data_str_default(*args):
    return ''
def _data_str_by(get_data):
    def ret(*args):
        return ":"+get_data(*args)
    return ret

def printEvent(event, id, retval = None, get_data = None):
    data_str = _data_str_default if get_data == None else _data_str_by(get_data)
    def ret(*args):
        try:
            print("{}:{}{}".format(id,event,data_str(*args)), file=sys.stdout)
            sys.stdout.flush()
        except Exception as e:
            print("Exception when writing an event: {}".format(e), file=sys.stderr)
        return retval
    return ret
