import collections
import os
import sys


class _JavaInstallsData:
    instance = None

    def __init__(self):
        if _JavaInstallsData.instance is None:
            _JavaInstallsData.instance = self
            self.IS_WINDOWS = os.name == "nt"
            self.IS_DARWIN = sys.platform == "darwin"
            self.LUCIFER_RELATIVE_JDK_DIR = ".lucifer-jdk"
            self.LUCIFER_JDK_DIR = os.path.abspath(self.LUCIFER_RELATIVE_JDK_DIR)
            self.UNPACK200 = "unpack200.exe" if self.IS_WINDOWS else "unpack200"
            self.UNPACK200_ARGS = '-r -v -l ""' if self.IS_WINDOWS else ""
            self.Path = collections.namedtuple("_Path", "dir base name ext")
            self.OS = "windows" if self.IS_WINDOWS else "mac" if self.IS_DARWIN else sys.platform
            self.ARCH = "x64" if sys.maxsize > 2 ** 32 else "x32"
            self.impl = "hotspot"


_JavaInstallsData()
_JavaInstallsData = _JavaInstallsData.instance
