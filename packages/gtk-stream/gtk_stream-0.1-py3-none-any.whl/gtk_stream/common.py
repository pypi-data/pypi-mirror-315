import sys

def printEvent(event, id):
    def ret(w):
        try:
            print(f"{id}:{event}", file=sys.stdout)
            sys.stdout.flush()
        except:
            print("Broken pipe, right ?", file=sys.stderr)
    return ret
