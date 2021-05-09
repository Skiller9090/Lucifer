import pkg_resources

isJs2PyInstalled = True if pkg_resources.working_set.by_key.get("js2py") is not None else False

__all__ = ["API", "Interpreter", "PyJsLucifer", "Core", "isJs2PyInstalled"]

if isJs2PyInstalled:
    print("Js2Py is installed enabling LMI.Javascript extension!")
    from .Interpreter import JsInterpreter
    from .JsFile import JsFile

    __all__.extend(["JsInterpreter", "JsFile"])
    print("Enabled LMI.Javascript extension.")
