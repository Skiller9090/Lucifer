import collections
import os

from .._SystemData import _SystemData


class _JavaInstallsData:
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            _JavaInstallsData()
        return cls.instance

    def __init__(self):
        if _JavaInstallsData.instance is not None:
            return
        _JavaInstallsData.instance = self
        self._systemData = _SystemData.getInstance()
        self.LUCIFER_RELATIVE_JDK_DIR = ".lucifer-jdk"
        self.LUCIFER_JDK_DIR = os.path.abspath(self.LUCIFER_RELATIVE_JDK_DIR)
        self.UNPACK200 = "unpack200.exe" if self._systemData.IS_WINDOWS else "unpack200"
        self.UNPACK200_ARGS = '-r -v -l ""' if self._systemData.IS_WINDOWS else ""
        self.Path = collections.namedtuple("_Path", "dir base name ext")
        self.impl = "hotspot"

    @property
    def IS_WINDOWS(self):
        return self._systemData.IS_WINDOWS

    @property
    def IS_DARWIN(self):
        return self._systemData.IS_DARWIN

    @property
    def OS(self):
        return self._systemData.OS

    @property
    def ARCH(self):
        return self._systemData.ARCH
