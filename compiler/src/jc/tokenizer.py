from io import TextIOWrapper
import re
from dataclasses import dataclass
from jc.spec import TOKEN_REGEX, TokenType, KeywordType
from jc.util import print_verbose


@dataclass
class Token:
    token_type: TokenType
    value: str | int
    loc: tuple[int, int]


class Tokenizer:
    def __init__(self, file: TextIOWrapper) -> None:
        self.file = file
        self.current_line_no = 1
        self.line_start = 0
        self.current_line = file.readline()
        self.current_iterator_i = 0

    def tokenize_line(self) -> None:
        self.iterator = re.finditer(TOKEN_REGEX, self.current_line)

    # def analyze_token(self, match: re.Match[str]) -> Token:

    def advance(self):
        match = next(self.iterator)
        potential_type = match.lastgroup
        if potential_type is None:
            raise RuntimeError(f"Unreachable(?) None token found '{match}'!")

        token_type = TokenType[potential_type]
        value = match.group()
        column = match.start() - self.line_start

        if token_type == TokenType.NEWLINE:
            print_verbose("hit new line")
            if self.has_more_tokens():
                self.current_line = self.file.readline()
                self.current_line_no += 1
                self.line_start = 0
                self.tokenize_line()
                self.advance()
                return
            else:
                raise RuntimeError("No more tokens left!")
        elif token_type == TokenType.SKIP:
            self.advance()
            return
        elif token_type == TokenType.INVALID:
            raise RuntimeError(f"Invalid token found '{match}'!")
        self.current_token = Token(
            token_type,
            value.lstrip('"').rstrip('"'),
            (self.current_line_no, column + 1),
        )
        print_verbose(f"Advance: {self.current_token}")

    def has_more_tokens(self) -> bool:
        # FIXME: This really only checks if there's another line but my approach
        # seems to not care?
        cur_pos = self.file.tell()
        has_more_lines = bool(self.file.readline())
        self.file.seek(cur_pos)
        return has_more_lines

    def token_type(self) -> TokenType:
        return self.current_token.token_type

    def key_word(self) -> KeywordType:
        assert self.token_type() == TokenType.KEYWORD, (
            f"Token '{self.current_token}' is not a valid keyword!"
        )
        assert type(self.current_token.value) is str, "Unreachable?"
        return KeywordType[self.current_token.value.upper()]

    def symbol(self) -> str:
        assert self.token_type() == TokenType.SYMBOL, (
            f"Token '{self.current_token}' is not a valid symbol!"
        )
        assert type(self.current_token.value) is str, "Unreachable?"
        return self.current_token.value

    def identifier(self) -> str:
        assert self.token_type() == TokenType.SYMBOL, (
            f"Token '{self.current_token}' is not a valid symbol!"
        )
        assert type(self.current_token.value) is str, "Unreachable?"
        return self.current_token.value

    def int_val(self) -> int:
        assert self.token_type() == TokenType.INT_CONST, (
            f"Token '{self.current_token}' is not an integer!"
        )

        assert type(self.current_token.value) is int, "Unreachable?"
        int_val = int(self.current_token.value)
        assert int_val >= 0 and int_val < 32767, (
            f"Integer '{int_val}' must be between 0-32767"
        )
        return int_val

    def string_val(self) -> str:
        assert self.token_type() == TokenType.STRING_CONST, (
            f"Token '{self.current_token}' is not a valid String!"
        )
        assert type(self.current_token.value) is str, "Unreachable?"
        return self.current_token.value
