import re
from dataclasses import dataclass
from jc.spec import TOKEN_REGEX, TokenType, KeywordType


@dataclass
class Token:
    token_type: TokenType
    value: str | int
    loc: tuple[int, int]


class Tokenizer:
    def __init__(self, filename: str, contents: str):
        self.filename = filename
        self.contents = contents

    def try_tokenize(self):
        line_no = 1
        line_start = 0
        for match in re.finditer(TOKEN_REGEX, self.contents):
            potential_type = match.lastgroup
            if potential_type is None:
                raise RuntimeError(f"Unreachable(?) None token found '{match}'!")

            token_type = TokenType[potential_type]
            value = match.group()
            column = match.start() - line_start

            if token_type == TokenType.NEWLINE:
                line_no += 1
                line_start = match.end()
                continue
            if token_type == TokenType.SKIP:
                continue
            if token_type == TokenType.INVALID:
                raise RuntimeError(f"Invalid token found '{match}'!")
            self.current_token = Token(
                token_type, value.replace('"', ""), (line_no, column + 1)
            )
            yield self.current_token

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
