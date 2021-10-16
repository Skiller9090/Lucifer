from LMI.Javascript import JsFile
from modules.Module import BaseModule


class Module(BaseModule):
    def run(self):
        jsFile = JsFile("external-modules/javascript/sources/lucifer/tests/testConsole.js")
        jsFile.runFile()
        return True

    def set_vars(self):
        default_vars = {
        }
        return default_vars

    def get_description(self):
        desc = """This module test to see if lucifer's javascript engine is working."""
        return desc
