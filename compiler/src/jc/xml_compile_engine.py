from jc.abstract_engine import AbstractEngine


class XmlCompileEngine(AbstractEngine):
    def compileClass(self):
        self._write_line("<class>")
        self._inc_indent_lvl()

        self._write_line("</class>")
        self._dec_indent_lvl()

    def compileClassVarDec(self):
        pass

    def compileSubroutine(self):
        pass

    def compileParameterList(self):
        pass

    def compileSubroutineBody(self):
        pass

    def compileVarDec(self):
        pass

    def compileStatements(self):
        pass

    def compileLet(self):
        pass

    def compileIf(self):
        pass

    def compileWhile(self):
        pass

    def compileDo(self):
        pass

    def compileReturn(self):
        pass

    def compileExpression(self):
        pass

    def compileTerm(self):
        pass

    def compileExpressionList(self) -> int:
        return 0
