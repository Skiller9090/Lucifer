import os

from .Error import MakeCLInvalidTooManyArgsError, MakeCLInvalidStateError
from .ParserStates import States
from .Tokens import TokenEnum


class MakeCLParser:
    def __init__(self):
        self.tokens = []
        self.compressedTokens = []
        self.counter = 0
        self.pointer = 0
        self.lexedFile = ("", "")
        self.stack = []
        self.currentToken = None
        self.finished = False
        self.state = States.Root
        self.stateMap = {
            States.Root: self.handleRoot,
            States.InFileDirectiveInitializer: self.handleFDI,
            States.InFileDirective: self.handleFD,
            States.InFileDirectiveAndLink: self.handleFDAL,
            States.InFileDirectiveAndArg: self.handleFDAA
        }

    def loadFromContext(self, context):
        self.tokens = context["tokens"]
        self.lexedFile = os.path.split(context["filePath"])
        self.pointer = 0
        self.compressedTokens.clear()
        self.stack.clear()
        self.currentToken = None
        self.state = States.Root
        self.finished = False

    def next(self):
        self.currentToken = self.tokens[self.pointer]
        self.pointer += 1

    def consume(self):
        function = self.stateMap.get(self.state, None)
        if function is not None:
            return function()
        raise MakeCLInvalidStateError(str(self.state) + " is an invalid state for the parser!")

    def handleRoot(self):
        if self.currentToken.type == TokenEnum.FileDirective:
            self.state = States.InFileDirectiveInitializer
            self.stack.append(self.currentToken)
        elif self.currentToken.type == TokenEnum.EOF:
            self.finished = True
            return True

    def handleFDI(self):
        if self.currentToken.type == TokenEnum.String:
            absFilePath = os.path.abspath(
                os.path.normpath(os.path.join(self.lexedFile[0], self.currentToken.value))
            )
            self.stack[-1].setFile(absFilePath)
        elif self.currentToken.type == TokenEnum.LBrace:
            self.state = States.InFileDirective

    def handleFD(self):
        if self.currentToken.type == TokenEnum.Link:
            self.state = States.InFileDirectiveAndLink
            self.stack.append(self.currentToken)
        elif self.currentToken.type == TokenEnum.Arg:
            self.state = States.InFileDirectiveAndArg
            self.stack.append(self.currentToken)
        elif self.currentToken.type == TokenEnum.RBrace:
            self.state = States.Root
            self.emitToken()

    def handleFDAL(self):
        if self.currentToken.type == TokenEnum.LBracket:
            self.counter = 0
        elif self.currentToken.type == TokenEnum.String:
            if self.counter == 0:
                self.stack[-1].setPath(
                    os.path.abspath(os.path.normpath(os.path.join(
                        self.lexedFile[0], self.currentToken.value)))
                )
            elif self.counter == 1:
                self.stack[-1].setFile(self.currentToken.value)
            else:
                raise MakeCLInvalidTooManyArgsError("Too many arguments in a link statement!")
        elif self.currentToken.type == TokenEnum.ArgSep:
            self.counter += 1
        elif self.currentToken.type == TokenEnum.SemiColon:
            LToken = self.stack.pop(-1)
            FDToken = self.stack[-1]
            FDToken.addLink(LToken)
            self.state = States.InFileDirective

    def handleFDAA(self):
        if self.currentToken.type == TokenEnum.String:
            self.stack[-1].addArg(self.currentToken.value)
        elif self.currentToken.type == TokenEnum.SemiColon:
            ArgToken = self.stack.pop(-1)
            FDToken = self.stack[-1]
            for link in ArgToken.value:
                FDToken.addArg(link)
            self.state = States.InFileDirective

    def emitToken(self):
        self.compressedTokens.append(self.stack.pop(-1))
