import sys


def set_bit(value: int, bit_index: int) -> int:
    return value | (1 << bit_index)


def get_bit(value: int, bit_index: int) -> int:
    return value & (1 << bit_index)


def unset_bit(value: int, bit_index: int) -> int:
    return value & (0 << bit_index)


def print_binary(arg: int) -> str:
    return f"{''.join(format(byte, '03b') for byte in int.to_bytes(arg))}"


def dest(arg: str) -> str:
    value = 0b0

    if arg == "null":
        return print_binary(0)

    if arg.find("M") >= 0:
        value = set_bit(value, 0)

    if arg.find("D") >= 0:
        value = set_bit(value, 1)

    if arg.find("A") >= 0:
        value = set_bit(value, 2)

    return print_binary(value)


def comp(arg: str) -> str:
    if arg == "0":
        return print_binary(0b101010)
    if arg == "1":
        return print_binary(0b111111)
    return ""


def jump(arg: str) -> str:
    value = 0b0
    if arg == "null":
        return print_binary(0)
    if arg == "JMP":
        return print_binary(0b111)

    has_n = arg.find("N") >= 0

    if arg.find("G") >= 0 or has_n:
        value = set_bit(value, 0)

    if arg.find("L") >= 0 or has_n:
        value = set_bit(value, 2)

    if arg.find("E") >= 0 and not has_n:
        value = set_bit(value, 1)

    return print_binary(value)
