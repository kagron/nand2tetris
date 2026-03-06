from io import TextIOWrapper

from jv.parser import CommandType


class CodeWriter:
    def __init__(self, file_name: str, commands: dict[str, CommandType]) -> None:
        self.file_name = file_name
        self.commands = commands

    def write(self) -> None:
        try:
            with open(self.file_name, "w") as f:
                self.f = f
                self.write_commands()
        except Exception as e:
            print("Exception:")
            print(e)

    def write_commands(self):
        for command, command_type in self.commands:
            if command_type == CommandType.C_ARITHMETIC:
                self.write_arithmetic(command)
            else:
                self.write_push_pop(command)

    def write_arithmetic(self, command: str):
        return

    def write_push_pop(self, command: str, segment: str, index: int):
        return
