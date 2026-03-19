VERBOSE = False


def append_verbose(buffer: list[str], line: str):
    if VERBOSE and len(line) > 0:
        buffer.append(f"{line}\n")


def print_verbose(arg):
    if VERBOSE and arg is not None:
        print(arg)


def set_verbose(val: bool):
    global VERBOSE
    VERBOSE = val
