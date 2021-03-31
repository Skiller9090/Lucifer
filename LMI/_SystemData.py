import os
import sys


class _SystemData:
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            _SystemData()
        return cls.instance

    def __init__(self):
        if _SystemData.instance is not None:
            return
        _SystemData.instance = self
        self._IS_WINDOWS = os.name == "nt"
        self._IS_DARWIN = sys.platform == "darwin"
        self._OS = "windows" if self._IS_WINDOWS else "mac" if self._IS_DARWIN else sys.platform
        self._ARCH = "x64" if sys.maxsize > 2 ** 32 else "x32"

    @property
    def IS_WINDOWS(self):
        return self._IS_WINDOWS

    @property
    def IS_DARWIN(self):
        return self._IS_DARWIN

    @property
    def OS(self):
        return self._OS

    @property
    def ARCH(self):
        return self._ARCH
