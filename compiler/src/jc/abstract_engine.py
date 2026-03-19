from abc import ABC, abstractmethod


class AbstractEngine(ABC):
    @abstractmethod
    def compileClass(self):
        pass

    @abstractmethod
    def compileClassVarDec(self):
        pass

    @abstractmethod
    def compileSubroutine(self):
        pass

    @abstractmethod
    def compileParameterList(self):
        pass

    @abstractmethod
    def compileSubroutineBody(self):
        pass

    @abstractmethod
    def compileVarDec(self):
        pass

    @abstractmethod
    def compileStatements(self):
        pass

    @abstractmethod
    def compileLet(self):
        pass

    @abstractmethod
    def compileIf(self):
        pass

    @abstractmethod
    def compileWhile(self):
        pass

    @abstractmethod
    def compileDo(self):
        pass

    @abstractmethod
    def compileReturn(self):
        pass

    @abstractmethod
    def compileExpression(self):
        pass

    @abstractmethod
    def compileTerm(self):
        pass

    @abstractmethod
    def compileExpressionList(self) -> int:
        pass
