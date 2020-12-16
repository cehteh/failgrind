import xxhash

print("failgrind v0.000000001")


seen = dict()    # id : state
bpoints = dict() # symbol : injection


class Intercept:
    "Symbol to intercept and inject"

    def __init__(self, name: str, injection):
        """
        register a breakpoint and faultinjection code
        type can be a function, a string, a string array, an array of string arrays.
        """
        self.name = name
        self.bp = gdb.Breakpoint(name)
        self.bp.silent = True
        self.injection = injection
        bpoints[name] = self



def bthash(bt):
    result = xxhash.xxh64()
    for frame in bt:
        result.update(bin(frame.pc()))

    return result.intdigest()


def backtrace():
    result = []
    frame = gdb.newest_frame()
    while frame:
        result.append(frame)
        frame = frame.older()
    return result


def bp_handler (bp):
    bt = backtrace()
    id = bthash(bt)

    if id not in seen:
        seen[id] = True
        print("Inject:")
    else:
        print("Pass:")

def include(filename: str):
    exec(compile(open(filename, "rb").read(), filename, 'exec'))

def main():
    mainbp = gdb.Breakpoint('main')
    mainbp.silent = True
    gdb.execute('run')
    mainbp.delete()
    include("intercept.py")
    gdb.events.stop.connect (bp_handler)
    gdb.execute('cont')



main()


#TODO: catch abort reasons SEGV ABRT SIGBUS SIGILL SIGSYS unhandled SIGFPE
#PLANNED: watchpoint: inferior can pass info to the debugger (ignore next bp etc)
#PLANNED: cpu cycle/time limit

