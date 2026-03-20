from jc.abstract_engine import AbstractCompileEngine
from jc.spec import KeywordType, TokenType


class XmlCompileEngine(AbstractCompileEngine):
    def compile_token(self):
        token_type = self.token.token_type.name.lower()

        match self.token.token_type.name.lower():
            case "int_const":
                token_type = "integerConstant"
            case "string_const":
                token_type = "stringConstant"

        token_val = (
            (
                self.token.value.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
            )
            if type(self.token.value) is str
            else self.token.value
        )
        self._write_line(f"<{token_type}>{token_val}</{token_type}>")

    def compile_class(self):
        self._write_line("<class>")
        self._inc_indent_lvl()
        self.compile_token()  # Class Keyword
        self.set_current_token(next(self.token_generator))
        self.compile_token()  # Class Name Identifier
        self.set_current_token(next(self.token_generator))
        self.compile_token()  # {

        for token in self.token_generator:
            print(token)
            self.set_current_token(token)
            token_type = self.token.token_type
            value = self.token.value
            if token_type == TokenType.KEYWORD:
                if (
                    value == KeywordType.STATIC.name.lower()
                    or value == KeywordType.FIELD.name.lower()
                ):
                    self.compile_class_var_dec()
                elif (
                    value == KeywordType.FUNCTION.name.lower()
                    or value == KeywordType.CONSTRUCTOR.name.lower()
                    or value == KeywordType.METHOD.name.lower()
                ):
                    self.compile_subroutine()
                    print("function")
            elif token_type == TokenType.SYMBOL:
                self.compile_token()

        self._dec_indent_lvl()
        self._write_line("</class>")

    def compile_class_var_dec(self):
        pass

    def compile_subroutine(self):
        self._write_line("<subroutineDec>")
        self._inc_indent_lvl()
        self.compile_token()  # constructor/function/method
        self.set_current_token(next(self.token_generator))
        self.compile_token()  # subroutine type
        self.set_current_token(next(self.token_generator))
        self.compile_token()  # subroutine identifier
        self.set_current_token(next(self.token_generator))
        self.compile_token()  # (
        self.compile_parameter_list()
        self.set_current_token(next(self.token_generator))
        self.compile_token()  # )
        self.set_current_token(next(self.token_generator))
        self.compile_token()  # {
        self.compile_subroutine_body()
        self._dec_indent_lvl()
        self._write_line("</subroutineDec>")

    def compile_parameter_list(self):
        pass

    def compile_subroutine_body(self):
        pass

    def compile_var_dec(self):
        pass

    def compile_statements(self):
        pass

    def compile_let(self):
        pass

    def compile_if(self):
        pass

    def compile_while(self):
        pass

    def compile_do(self):
        pass

    def compile_return(self):
        pass

    def compile_expression(self):
        pass

    def compile_term(self):
        pass

    def compile_expression_list(self) -> int:
        return 0
