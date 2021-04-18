from .Parser import MakeCLParser
from .Lexer import MakeCLLexer
import os


class MakeCLFile:
    def __init__(self, filePath):
        self.filePath = os.path.abspath(filePath)

    def getRawFileDirectives(self):
        makeCLLexer = MakeCLLexer()
        makeCLParser = MakeCLParser()

        makeCLLexer.openFile(self.filePath)
        while not makeCLLexer.finished:
            makeCLLexer.next()
            makeCLLexer.consume()

        data = makeCLLexer.retrieveContext()
        makeCLParser.loadFromContext(data)

        while not makeCLParser.finished:
            makeCLParser.next()
            makeCLParser.consume()
        return makeCLParser.compressedTokens

    def getFileDirectives(self):
        rawFileDirectives = self.getRawFileDirectives()
        fileDirectives = {}
        for fd in rawFileDirectives:
            fileDirectives[fd.value['file']] = {
                'links': {x.value["file"]: x.value["path"] for x in fd.value["links"]},
                'args': fd.value["args"]
            }
        return fileDirectives
