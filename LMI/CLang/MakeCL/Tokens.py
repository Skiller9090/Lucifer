from enum import Enum


class TokenEnum(Enum):
    FileDirective = 0
    Link = 1
    String = 2
    ArgSep = 3
    LBracket = 4
    RBracket = 5
    LBrace = 6
    RBrace = 7
    SemiColon = 8
    Keyword = 9
    EOF = 10
    Unknown = 99


class Token:
    def __init__(self, tokenType):
        self.type = tokenType

    def __str__(self):
        return f"{self.__class__.__name__}"

    def __repr__(self):
        return self.__str__()


class KeywordToken(Token):
    def __init__(self):
        super(KeywordToken, self).__init__(TokenEnum.Keyword)
        self.value = ""

    def add(self, char):
        self.value += char


class UnknownToken(Token):
    def __init__(self):
        super(UnknownToken, self).__init__(TokenEnum.Unknown)
        self.value = None


class SemiColonToken(Token):
    def __init__(self):
        super(SemiColonToken, self).__init__(TokenEnum.SemiColon)
        self.value = ";"


class RBraceToken(Token):
    def __init__(self):
        super(RBraceToken, self).__init__(TokenEnum.RBrace)
        self.value = "}"


class LBraceToken(Token):
    def __init__(self):
        super(LBraceToken, self).__init__(TokenEnum.LBrace)
        self.value = "{"


class RBracketToken(Token):
    def __init__(self):
        super(RBracketToken, self).__init__(TokenEnum.RBracket)
        self.value = ")"


class LBracketToken(Token):
    def __init__(self):
        super(LBracketToken, self).__init__(TokenEnum.LBracket)
        self.value = "("


class ArgSepToken(Token):
    def __init__(self):
        super(ArgSepToken, self).__init__(TokenEnum.ArgSep)
        self.value = "|"


class StringToken(Token):
    def __init__(self, openingChar):
        super(StringToken, self).__init__(TokenEnum.String)
        self.openingChar = openingChar
        self.value = ""

    def add(self, char: str):
        self.value += char


class LinkToken(Token):
    def __init__(self):
        super(LinkToken, self).__init__(TokenEnum.Link)
        self.value = {"path": "", "file": ""}

    def setFile(self, file: str):
        self.value["file"] = file

    def setPath(self, path: str):
        self.value["path"] = path


class FileDirectiveToken(Token):
    def __init__(self):
        super(FileDirectiveToken, self).__init__(TokenEnum.FileDirective)
        self.value = {"file": "", "links": []}

    def setFile(self, file: str):
        self.value["file"] = file

    def addLink(self, linkToken: LinkToken):
        self.value["links"].append(linkToken)


class EOFToken(Token):
    def __init__(self):
        super(EOFToken, self).__init__(TokenEnum.EOF)
        self.value = None


keywordMap = {
    "FD": FileDirectiveToken,
    "FileDirective": FileDirectiveToken,
    "L": LinkToken,
    "Link": LinkToken
}
