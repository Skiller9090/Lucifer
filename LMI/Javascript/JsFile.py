import importlib
import os

import js2py

from lucifer.Errors import LuciferFileNotFound
from .Core import PyJsLoadedModule
from .Interpreter import JsInterpreter


class JsFile:
    def __init__(self, fileName):
        self.fileName = fileName
        self.file = None
        self.content = None

    def readFile(self):
        if not os.path.exists(self.fileName):
            raise LuciferFileNotFound(f"JS file not found: {self.fileName}")
        with open(self.fileName, "r") as self.file:
            self.content = self.file.read()

    def runFile(self):
        self.readFile()
        jsInterpreter = JsInterpreter()
        jsInterpreter.exec(self.content, self.fileName)

    def translateFile(self):
        directory, file = os.path.split(self.fileName)
        name, _ = os.path.splitext(file)
        directory = directory.replace("external-modules/javascript/sources", "external-modules/javascript/builds")
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        pyPath = os.path.normpath(f"{directory}{os.sep}{name}.py")
        js2py.translate_file(self.fileName, pyPath)
        return pyPath

    def importFile(self):
        path = self.translateFile()
        directory, file = os.path.split(path)
        name, _ = os.path.splitext(file)
        module = importlib.import_module(directory.replace(os.sep, ".") + "." + name)
        return PyJsLoadedModule(module.__dict__[name])
