VERBOSE = False


def print_verbose(arg):
    if VERBOSE and arg is not None:
        print(arg)


def set_verbose(val: bool):
    global VERBOSE
    VERBOSE = val
