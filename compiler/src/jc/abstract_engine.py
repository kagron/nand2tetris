from abc import ABC, abstractmethod

from jc.util import append_verbose

INDENT = "  "


class AbstractEngine(ABC):
    def __init__(self, buffer: list[str]):
        self.buffer = buffer
        self.indent_lvl = 1

    @abstractmethod
    def compileClass(self):
        """Compiles a complete `class`"""
        pass

    @abstractmethod
    def compileClassVarDec(self):
        """Compiles a static variable declaration, or a field declaration"""
        pass

    @abstractmethod
    def compileSubroutine(self):
        """Compiles a complete `method`, `function`, or `constructor`"""
        pass

    @abstractmethod
    def compileParameterList(self):
        """
        Compiles a (possibly empty) parameter list.  Does not handle the
        enclosing parentheses tokens `(` and `)`.
        """
        pass

    @abstractmethod
    def compileSubroutineBody(self):
        """Compiles a subroutine's body"""
        pass

    @abstractmethod
    def compileVarDec(self):
        """Compiles a `var` declaration"""
        pass

    @abstractmethod
    def compileStatements(self):
        """
        Compiles a sequence of statements.  Does not handle the enclosing
        curly bracket tokens `{` and `}`.
        """
        pass

    @abstractmethod
    def compileLet(self):
        """Compiles a `let` statement"""
        pass

    @abstractmethod
    def compileIf(self):
        """Compiles a `if` statement, possibly with a trailing `else` statement"""
        pass

    @abstractmethod
    def compileWhile(self):
        """Compiles a `while` statement"""
        pass

    @abstractmethod
    def compileDo(self):
        """Compiles a `do` statement"""
        pass

    @abstractmethod
    def compileReturn(self):
        """Compiles a `return` statement"""
        pass

    @abstractmethod
    def compileExpression(self):
        """Compiles an expression"""
        pass

    @abstractmethod
    def compileTerm(self):
        """
        Compiles a `term`.  If the current token is an `identifier`, the
        routine must resolve it into a `variable`, an `array element`
        or a `subroutine call`.  A single lookahead token, which may be
        `[`, `(`, or `,`, suffices to distinguish between the possibilities.
        Any other token is not part of this term and should not be advanced
        over
        """
        pass

    @abstractmethod
    def compileExpressionList(self) -> int:
        """
        Compiles a (possibly empty) comma-separated list of expressions.
        Returns the number of expressions in the list
        """
        pass

    def _inc_indent_lvl(self):
        self.indent_lvl += 1

    def _dec_indent_lvl(self):
        self.indent_lvl = max(0, self.indent_lvl - 1)

    def _write_verbose(self, line: str):
        append_verbose(self.buffer, line)

    def _write_line(self, line: str):
        self.buffer.append(f"{self.indent_lvl * INDENT}{line}\n")
