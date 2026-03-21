from abc import ABC, abstractmethod
from typing import Generator

from jc.util import append_verbose
from jc.tokenizer import Token, Tokenizer

INDENT = "  "


class AbstractCompileEngine(ABC):
    def __init__(self, buffer: list[str], tokenizer: Tokenizer):
        self.buffer = buffer
        self.tokenizer = tokenizer
        self.indent_lvl = 0

    @abstractmethod
    def compile_class(self):
        """Compiles a complete `class`"""
        pass

    @abstractmethod
    def compile_class_var_dec(self):
        """Compiles a static variable declaration, or a field declaration"""
        pass

    @abstractmethod
    def compile_subroutine(self):
        """Compiles a complete `method`, `function`, or `constructor`"""
        pass

    @abstractmethod
    def compile_parameter_list(self):
        """
        Compiles a (possibly empty) parameter list.  Does not handle the
        enclosing parentheses tokens `(` and `)`.
        """
        pass

    @abstractmethod
    def compile_subroutine_body(self):
        """Compiles a subroutine's body"""
        pass

    @abstractmethod
    def compile_var_dec(self):
        """Compiles a `var` declaration"""
        pass

    @abstractmethod
    def compile_statements(self):
        """
        Compiles a sequence of statements.  Does not handle the enclosing
        curly bracket tokens `{` and `}`.
        """
        pass

    @abstractmethod
    def compile_let(self):
        """Compiles a `let` statement"""
        pass

    @abstractmethod
    def compile_if(self):
        """Compiles a `if` statement, possibly with a trailing `else` statement"""
        pass

    @abstractmethod
    def compile_while(self):
        """Compiles a `while` statement"""
        pass

    @abstractmethod
    def compile_do(self):
        """Compiles a `do` statement"""
        pass

    @abstractmethod
    def compile_return(self):
        """Compiles a `return` statement"""
        pass

    @abstractmethod
    def compile_expression(self):
        """Compiles an expression"""
        pass

    @abstractmethod
    def compile_term(self):
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
    def compile_expression_list(self) -> int:
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
