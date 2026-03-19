from enum import Enum, auto


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

TOKEN_SPEC = [
    (TokenType.KEYWORD, rf"({KEYWORD_NAMES})"),
    (TokenType.SYMBOL, rf"[{''.join(SYMBOLS)}]"),
    (TokenType.STRING_CONST, r'"[^"\n]+"'),
    (TokenType.IDENIFIER, r"[a-zA-Z]+\w+"),
    (TokenType.INT_CONST, r"\d+"),
]

TOKEN_REGEX = "|".join("(?P<%s>%s)" % (pair[0].name, pair[1]) for pair in TOKEN_SPEC)
