def set_bit(value: int, bit_index: int) -> int:
    return value | (1 << bit_index)


def get_bit(value: int, bit_index: int) -> int:
    return value & (1 << bit_index)


def unset_bit(value: int, bit_index: int) -> int:
    return value & (0 << bit_index)


def print_binary(arg: int, str_format: str = "03b") -> str:
    return format(arg, str_format)


comps = {
    "0": 0b0101010,
    "1": 0b0111111,
    "-1": 0b0111010,
    "D": 0b0001100,
    "A": 0b0110000,
    "M": 0b1110000,
    "!D": 0b0001101,
    "!A": 0b0110001,
    "!M": 0b1110001,
    "-D": 0b0001111,
    "-A": 0b0110011,
    "-M": 0b1110011,
    "D+1": 0b0011111,
    "A+1": 0b0110111,
    "M+1": 0b1110111,
    "D-1": 0b0001110,
    "A-1": 0b0110010,
    "M-1": 0b1110010,
    "D+A": 0b0000010,
    "D+M": 0b1000010,
    "D-A": 0b0010011,
    "D-M": 0b1010011,
    "A-D": 0b0000111,
    "M-D": 0b1000111,
    "D&A": 0b0000000,
    "D&M": 0b1000000,
    "D|A": 0b0010101,
    "D|M": 0b1010101,
}


def dest(arg: str) -> str:
    value = 0b0

    if arg == "null" or len(arg) == 0:
        return print_binary(0)

    if arg.find("M") >= 0:
        value = set_bit(value, 0)

    if arg.find("D") >= 0:
        value = set_bit(value, 1)

    if arg.find("A") >= 0:
        value = set_bit(value, 2)

    return print_binary(value)


def comp(arg: str) -> str:
    comp_val = comps.get(arg)
    if comp_val is None:
        raise ValueError(f"Instruction has an invalid comp '{arg}'")
    return print_binary(comp_val, "07b")


def jump(arg: str) -> str:
    value = 0b0
    # Kinda doubt null will ever be in the assembly
    if arg == "null" or len(arg) == 0:
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
