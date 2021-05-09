import ctypes
import os
import re

from lucifer.Errors import LuciferFailedToFind
from .ClangCompiler import ClangCompiler


class Clang:
    def __init__(self):
        self.compiler = ClangCompiler()
        self.cache = {}

    def getPossibleCompiles(self):
        return {"c": self.compiler.canCompileC,
                "cpp": self.compiler.canCompileCPP,
                "c++": self.compiler.canCompileCPP}

    def load(self, path: str):
        normPath = os.path.normpath(path)
        if not os.path.isabs(normPath):
            normPath = os.path.join(self.compiler.topSrcDirectory, normPath)
        normPath = os.path.abspath(normPath)
        pre, ext = os.path.splitext(normPath)
        if ext == "":
            pre, after = os.path.split(normPath)
            files = os.listdir(pre)
            rExp = re.compile(f"^{after}.({'|'.join(self.compiler.availableExtensions)})$")
            possible = list(filter(rExp.match, files))
            if len(possible) == 1:
                normPath = os.path.abspath(os.path.join(pre, possible[0]))
            else:
                raise LuciferFailedToFind(f"failed to find a single file what matches {after} in the c sources, " +
                                          "please make sure you haven't got two identical named files in the same" +
                                          " directory with different extensions, such as test.c and test.cpp!")
        if normPath in self.cache.keys():
            return self.cache[normPath]
        outfile = self.compiler.compileAuto(normPath, silent=False, verbose=False)
        if outfile is None:
            return None
        dynLib = ctypes.cdll.LoadLibrary(outfile)
        self.cache[normPath] = dynLib
        return dynLib
