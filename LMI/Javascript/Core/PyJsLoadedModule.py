from js2py.pyjs import to_python


class PyJsLoadedModule:
    def __init__(self, obj):
        from ..PyJsLucifer import PyJsLucifer
        self.obj = obj
        obj.__dict__["_obj"].register("lucifer")
        obj.__dict__["_obj"].put("lucifer", PyJsLucifer.getInstance())
        self.rawFunctionMap = obj.__dict__["_obj"].__dict__.get("own")
        self.functionMap = {}
        self._setupFunctionMap()

    def _setupFunctionMap(self):
        for k, v in zip(self.rawFunctionMap.keys(), self.rawFunctionMap.values()):
            self.functionMap[k] = v["value"]

    def __getattr__(self, item):
        if item in self.functionMap:
            return to_python(self.functionMap[item])
        if item in self.__dict__:
            return self.functionMap[item]
        raise AttributeError(f"No attribute: {item}")
