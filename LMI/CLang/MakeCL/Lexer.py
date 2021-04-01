from .Error import MakeCLInvalidFileError, MakeCLInvalidKeywordError, MakeCLInvalidCharacterError
from .LexerStates import States
from .Tokens import KeywordToken, LBracketToken, RBracketToken, LBraceToken, \
    RBraceToken, StringToken, ArgSepToken, SemiColonToken, EOFToken, keywordMap
import string
import os


class MakeCLLexer:
    def __init__(self):
        self.tokens = []
        self.file = None
        self.path = None
        self.finished = False
        self.state = States.Root
        self.currentToken = None
        self.current = ""
        self.stateMap = {
            States.Root: self.consumeRoot,
            States.String: self.consumeString,
            States.Keyword: self.consumeKeyword,
            States.Comment: self.consumeComment
        }

    def retrieveContext(self):
        return {
            "tokens": self.tokens,
            "filePath": self.path
        }

    def openFile(self, path: str, ignoreFileName=False):
        absPath = os.path.abspath(path)
        _, ext = os.path.splitext(absPath)
        if ext not in [".clucifer", "clucifer"]:
            error = MakeCLInvalidFileError("Invalid extension for MakeCL file: " + ext)
            if not ignoreFileName:
                error.raiseError()
        pre, fileName = os.path.split(absPath)
        if fileName != "make.clucifer":
            error = MakeCLInvalidFileError("Invalid file name for MakeCL file")
            if not ignoreFileName:
                error.raiseError()
        self.state = States.Root
        self.tokens.clear()
        self.file = open(absPath, "r")
        self.path = absPath
        self.finished = False

    def next(self):
        self.current = self.file.read(1)

    def consume(self):
        function = self.stateMap.get(self.state, None)
        if function is not None:
            return function()
        print("Error")

    def consumeBracket(self):
        if self.current == "(":
            self.currentToken = LBracketToken()
            self.emit_token()
        elif self.current == ")":
            self.currentToken = RBracketToken()
            self.emit_token()
        elif self.current == "{":
            self.currentToken = LBraceToken()
            self.emit_token()
        elif self.current == "}":
            self.currentToken = RBraceToken()
            self.emit_token()

    def consumeRoot(self):
        if self.current == "":
            self.currentToken = EOFToken()
            self.emit_token()
            self.finished = True
            self.file.close()
            return True
        elif self.current in string.ascii_letters:
            self.state = States.Keyword
            self.currentToken = KeywordToken()
            self.currentToken.add(self.current)
        elif self.current in "(){}":
            self.consumeBracket()
        elif self.current in ["'", '"']:
            self.state = States.String
            self.currentToken = StringToken(self.current)
        elif self.current == "|":
            self.currentToken = ArgSepToken()
            self.emit_token()
        elif self.current == "#":
            self.state = States.Comment
        elif self.current == ";":
            self.currentToken = SemiColonToken()
            self.emit_token()

    def consumeString(self):
        if self.current == self.currentToken.openingChar:
            self.state = States.Root
            self.emit_token()
        elif self.current == "\n":
            raise MakeCLInvalidCharacterError("Newline character in string input!")
        else:
            self.currentToken.add(self.current)

    def consumeKeyword(self):
        if self.current in string.ascii_letters + string.digits:
            self.currentToken.add(self.current)
        else:
            self.state = States.Root
            if self.currentToken.value in keywordMap.keys():
                self.currentToken = keywordMap[self.currentToken.value]()
                self.emit_token()
            else:
                raise MakeCLInvalidKeywordError(self.currentToken.value)
            self.consumeRoot()

    def consumeComment(self):
        if self.current == "\n":
            self.state = States.Root

    def emit_token(self):
        self.tokens.append(self.currentToken)
        self.currentToken = None
