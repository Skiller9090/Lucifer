import js2py
import js2py.pyjs
from js2py import PyJsException

from .API import Console
from .PyJsLucifer import PyJsLucifer


class JsInterpreter:
    def __init__(self):
        self.pyJsLucifer = PyJsLucifer()
        self.code = ""
        self.updateAPI()
        self.lastJsContext = None

    @staticmethod
    def updateAPI():
        js2py.pyjs.JS_BUILTINS["console"] = Console()

    def exec(self, code, filename=None, enable_require=False):
        self.code = code
        self.lastJsContext = js2py.EvalJs({"lucifer": self.pyJsLucifer}, enable_require=enable_require)
        try:
            self.lastJsContext.execute(self.code)
        except PyJsException as e:
            self.handle_error(e, filename=filename)

    @staticmethod
    def handle_error(e, filename=None):
        if hasattr(e, "typ") and hasattr(e, "message") and hasattr(e, "throw"):
            raise e
        if e.mes.Class == 'Error':
            print(e.mes.callprop('toString').value, end="")
        else:
            print(e.mes.to_string().value, end="")
        print(f" in file: {filename}" if filename is not None else "")
