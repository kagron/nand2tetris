from jc.abstract_compile_engine import AbstractCompileEngine
from jc.spec import KeywordType, TokenType
from jc.util import print_verbose


class XmlCompileEngine(AbstractCompileEngine):
    def compile_token(self, expected_token: str | None = None):
        current_token = self.tokenizer.current_token
        current_val = current_token.value
        if expected_token is not None and expected_token != current_val:
            raise RuntimeError(
                f"Expecting token '{expected_token}' but found token '{current_val}'"
            )
        token_type = current_token.token_type.name.lower()

        match token_type:
            case "int_const":
                token_type = "integerConstant"
            case "string_const":
                token_type = "stringConstant"

        token_val = (
            (
                current_val.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
            )
            if type(current_val) is str
            else current_val
        )
        self._write_line(f"<{token_type}>{token_val}</{token_type}>")

    def process_token(self, expected_token: str | None = None):
        print_verbose("Processing token")
        self.compile_token(expected_token)
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
        else:
            print("PROCESSING TOKEN WHEN NO MORE TOKENS")
            if expected_token is not None:
                print(f"EXPECTED TOKEN: {expected_token}")

    def compile_class(self):
        self._write_line("<class>")
        self._inc_indent_lvl()

        self.process_token("class")
        self.process_token()  # class identifier
        self.process_token("{")

        token_type = self.tokenizer.token_type()

        while self.tokenizer.has_more_tokens() and not (
            token_type == TokenType.SYMBOL and self.tokenizer.symbol() == "}"
        ):
            print_verbose("beginning of compile_class() loop")
            match token_type:
                case TokenType.KEYWORD:
                    match self.tokenizer.key_word():
                        case KeywordType.STATIC | KeywordType.FIELD:
                            self.compile_class_var_dec()
                        case (
                            KeywordType.FUNCTION
                            | KeywordType.CONSTRUCTOR
                            | KeywordType.METHOD
                        ):
                            self.compile_subroutine()
                case TokenType.SYMBOL:
                    self.compile_token()

            token_type = self.tokenizer.token_type()

        print("Last curly")
        self.process_token("}")
        self._dec_indent_lvl()
        self._write_line("</class>")

    def compile_class_var_dec(self):
        self._write_line("<classVarDec>")
        self._inc_indent_lvl()
        self.process_token()  # static/field
        self.process_token()  # class var type keyword or type
        self.process_token()  # class var identifier
        self.process_token(";")
        self._dec_indent_lvl()
        self._write_line("</classVarDec>")

    def compile_subroutine(self):
        print_verbose("compile_subroutine()")
        self._write_line("<subroutineDec>")
        self._inc_indent_lvl()

        self.process_token()  # constructor/function/method
        self.process_token()  # subroutine type
        self.process_token()  # subroutine identifier
        self.process_token("(")  # (
        if not (
            self.tokenizer.token_type() == TokenType.SYMBOL
            and self.tokenizer.symbol() == ")"
        ):
            self.compile_parameter_list()
        self.process_token(")")  # )
        self.process_token("{")  # {
        self.compile_subroutine_body()
        self.process_token("}")  # }

        self._dec_indent_lvl()
        self._write_line("</subroutineDec>")

    def compile_parameter_list(self):
        print_verbose("compile_parameter_list()")
        self._write_line("<parameterList>")
        self._inc_indent_lvl()

        self.process_token()  # param type
        self.process_token()  # param identifier

        token_type = self.tokenizer.token_type()
        while self.tokenizer.has_more_tokens() and not (
            token_type == TokenType.SYMBOL and self.tokenizer.symbol() == ")"
        ):
            self.process_token(",")
            self.process_token()  # param type
            self.process_token()  # param identifier
        self._dec_indent_lvl()
        self._write_line("</parameterList>")

    def compile_subroutine_body(self):
        print_verbose("compile_subroutine_body()")
        self._write_line("<subroutineBody>")
        self._inc_indent_lvl()

        token_type = self.tokenizer.token_type()

        while self.tokenizer.has_more_tokens() and not (
            token_type == TokenType.SYMBOL and self.tokenizer.symbol() == "}"
        ):
            print_verbose("Beginning of compile_subroutine_body() loop")
            match token_type:
                case TokenType.KEYWORD:
                    # Spec says Vars have to come before statements so meh
                    if self.tokenizer.key_word() == KeywordType.VAR:
                        self.compile_var_dec()
                    else:
                        self.compile_statements()

                case TokenType.SYMBOL:
                    self.process_token()

            token_type = self.tokenizer.token_type()

        self._dec_indent_lvl()
        self._write_line("</subroutineBody>")

    def compile_var_dec(self):
        print_verbose("compile_var_dec()")
        self._write_line("<varDec>")
        self._inc_indent_lvl()

        self.process_token("var")
        self.process_token()  # var type
        self.process_token()  # var identifier

        token_type = self.tokenizer.token_type()
        while self.tokenizer.has_more_tokens() and not (
            token_type == TokenType.SYMBOL and self.tokenizer.symbol() == ";"
        ):
            self.process_token(",")
            self.process_token()  # var identifier
        self._dec_indent_lvl()
        self._write_line("</varDec>")

    def compile_statements(self):
        print_verbose("compile_statements()")
        self._write_line("<statements>")
        self._inc_indent_lvl()
        token_type = self.tokenizer.token_type()

        while self.tokenizer.has_more_tokens() and not (
            token_type == TokenType.SYMBOL and self.tokenizer.symbol() == "}"
        ):
            print_verbose("Beginning of compile_statements() loop")
            match token_type:
                case TokenType.KEYWORD:
                    match self.tokenizer.key_word():
                        case KeywordType.LET:
                            self.compile_let()
                        case KeywordType.IF:
                            self.compile_if()
                        case KeywordType.WHILE:
                            self.compile_while()
                        case KeywordType.DO:
                            self.compile_do()
                        case KeywordType.RETURN:
                            self.compile_return()
                case TokenType.SYMBOL:
                    self.process_token()
            token_type = self.tokenizer.token_type()

        self._dec_indent_lvl()
        self._write_line("</statements>")

    def compile_let(self):
        print_verbose("compile_let")
        self._write_line("<letStatement>")
        self._inc_indent_lvl()
        self.process_token("let")
        self.process_token()
        self.process_token(";")
        self._dec_indent_lvl()
        self._write_line("</letStatement>")

    def compile_if(self):
        pass

    def compile_while(self):
        pass

    def compile_do(self):
        print_verbose("compile_do")
        self._write_line("<doStatement>")
        self._inc_indent_lvl()
        self.process_token("do")
        self.process_token()
        self.process_token("(")
        expressions_created = self.compile_expression_list()
        self.process_token(")")
        self.process_token(";")
        self._dec_indent_lvl()
        self._write_line("</doStatement>")

    def compile_return(self):
        print_verbose("compile_return")
        self._write_line("<returnStatement>")
        self._inc_indent_lvl()
        self.process_token("return")
        # TODO: Add expression handling here
        self.process_token(";")
        self._dec_indent_lvl()
        self._write_line("</returnStatement>")

    def compile_expression(self):
        # 10
        # 1 > 0
        # my_var
        # my_var & this_var
        # my_var & this_var & that_var -> term op term op term
        # my_var | (this_var + that_var) -> term op term
        self._write_line("<expression>")
        self._inc_indent_lvl()
        self.compile_term()

        token_type = self.tokenizer.token_type()
        if token_type == TokenType.SYMBOL:
            # Found op or term
            self.process_token()
            if token_type == TokenType.SYMBOL:
                pass

        self._dec_indent_lvl()
        self._write_line("</expression>")

    def compile_term(self):
        pass

    def compile_expression_list(self) -> int:
        return 0
