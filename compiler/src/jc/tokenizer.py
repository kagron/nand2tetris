import re
from jc.spec import TOKEN_REGEX, TokenType, KeywordType
from .util import print_verbose


class Tokenizer:
    def __init__(self, filename: str, contents: str):
        self.filename = filename
        # self.contents = contents.splitlines()
        # self.line_no = -1
        self.tokens = contents.split()
        self.current_token = ""
        self.current_token_i = -1

    def has_more_tokens(self) -> bool:
        return self.current_token_i + 1 < len(self.tokens)

    def advance(self):
        self.current_token_i += 1
        self.current_token = self.tokens[self.current_token_i].rstrip(";")

    def token_type(self) -> TokenType:
        match = re.match(TOKEN_REGEX, self.current_token)
        if match is None or match.lastgroup is None:
            return TokenType.INVALID

        return TokenType[match.lastgroup]

    def key_word(self) -> KeywordType:
        assert self.token_type() == TokenType.KEYWORD, (
            f"Token '{self.current_token}' is not a valid keyword!"
        )
        return KeywordType[self.current_token.upper()]

    def symbol(self) -> str:
        assert self.token_type() == TokenType.SYMBOL, (
            f"Token '{self.current_token}' is not a valid symbol!"
        )
        return self.current_token

    def identifier(self) -> str:
        assert self.token_type() == TokenType.SYMBOL, (
            f"Token '{self.current_token}' is not a valid symbol!"
        )
        return self.current_token

    def int_val(self) -> int:
        assert self.token_type() == TokenType.INT_CONST, (
            f"Token '{self.current_token}' is not an integer!"
        )
        int_val = int(self.current_token)
        assert int_val >= 0 and int_val < 32767, (
            f"Integer '{int_val}' must be between 0-32767"
        )
        return int_val

    def string_val(self) -> str:
        assert self.token_type() == TokenType.STRING_CONST, (
            f"Token '{self.current_token}' is not a valid String!"
        )
        return self.current_token
