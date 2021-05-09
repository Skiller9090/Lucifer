from js2py.pyjs import PyObjectWrapper

from ..Interface import LMI


class PyJsLucifer(PyObjectWrapper):
    INSTANCE = None

    @staticmethod
    def getInstance():
        if PyJsLucifer.INSTANCE is None:
            return PyJsLucifer()
        return PyJsLucifer.INSTANCE

    def __init__(self):
        super().__init__(self)
        PyJsLucifer.INSTANCE = self
        self.LMI = LMI

    def getLuciferManager(self):
        return self.LMI.luciferManager

    @property
    def luciferManager(self):
        return self.LMI.luciferManager

    def __repr__(self):
        return f"<PyJsLucifer|{self.__class__.__name__}>"
