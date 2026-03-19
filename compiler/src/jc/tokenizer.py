from enum import Enum, auto
from .util import print_verbose


class TokenType(Enum):
    KEYWORD = auto()
    SYMBOL = auto()
    IDENIFIER = auto()
    INT_CONST = auto()
    STRING_CONST = auto()
    INVALID = auto()


class KeywordType(Enum):
    CLASS = auto()
    METHOD = auto()
    FUNCTION = auto()
    CONSTRUCTOR = auto()
    INT = auto()
    BOOLEAN = auto()
    CHAR = auto()
    VOID = auto()
    VAR = auto()
    STATIC = auto()
    FIELD = auto()
    LET = auto()
    DO = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()
    THIS = auto()
    INVALID = auto()


SYMBOLS = [
    "{",
    "}",
    "(",
    ")",
    r"\[",
    r"\]",
    ".",
    ",",
    ";",
    "+",
    r"\-",
    "*",
    "/",
    "&",
    "|",
    "<",
    ">",
    "=",
    "~",
]

KEYWORD_NAMES = "|".join(
    [
        ktype.name.lower()
        for ktype in list(KeywordType)
        if ktype is not KeywordType.INVALID
    ]
)
SYMBOL_STRS = "".join(SYMBOLS)
TOKEN_SPEC = [
    (TokenType.KEYWORD, rf"({KEYWORD_NAMES})"),
    (TokenType.SYMBOL, rf"[{SYMBOL_STRS}]"),
]


class Tokenizer:
    def __init__(self, filename: str, contents: str):
        self.filename = filename
        self.contents = contents.splitlines()
        print_verbose(f"Number of lines: {len(self.contents)}")
        print_verbose(f"Contents: {self.contents}")
        # self.line_no = -1
        self.current_token = ""

    def has_more_tokens(self) -> bool:
        return True

    def advance(self):
        pass

    def token_type(self) -> TokenType:
        return TokenType.INVALID

    def key_word(self) -> KeywordType:
        return KeywordType.INVALID

    def symbol(self) -> str:
        return ""

    def identifier(self) -> str:
        return ""

    def int_val(self) -> int:
        return 0

    def string_val(self) -> str:
        return ""
