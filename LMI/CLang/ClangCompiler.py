from ..Command import autoSilenceCommand, checkCommandExists
from .._SystemData import _SystemData
from lucifer.Errors import LuciferFailedToCompile
import os
import errno


class ClangCompiler:
    def __init__(self):
        self._systemData = _SystemData.getInstance()
        self.compiledExtension = self.fetchExtension()
        self._CC = None
        self._CPP = None
        self._CPPLink = "-lstdc++"
        self.topDirectory = os.path.abspath("external-modules/c/")
        self.topSrcDirectory = os.path.abspath("external-modules/c/sources/")
        self.availableExtensions = ["c", "cc", "cpp"]
        self.findCompiler()

    @property
    def canCompileC(self):
        return self._CC is not None

    @property
    def canCompileCPP(self):
        return self._CPP is not None

    def findCompiler(self):
        cc_names = ["cc", "CC", "gcc"]
        cpp_names = ["g++"]
        for ccTest in cc_names:
            if checkCommandExists(ccTest):
                self._CC = ccTest
                break
        for cppTest in cpp_names:
            if checkCommandExists(cppTest):
                self._CPP = f"{cppTest} {self._CPPLink}"
                break
        if self._CPP is None and self._CC is not None:
            self._CPP = f"{self._CC} {self._CPPLink}"

    def cToShared(self, mainFile, extern_files=None, out="builds/", verbose=False, silent=False, useCPP=False):
        if extern_files is None:
            extern_files = []
        for file in [mainFile, *extern_files]:
            if not silent:
                print(f"{'CC++' if useCPP else 'CC'}: {str(os.path.relpath(os.path.abspath(file), self.topDirectory))}")
        filesString = " ".join(list(map(os.path.abspath, [mainFile, *extern_files])))
        outfile = os.path.abspath(os.path.abspath(mainFile).replace(
            self.topSrcDirectory, self.topDirectory + os.sep + out))
        pre, _ = os.path.splitext(outfile)
        outfile = pre + self.compiledExtension
        if not os.path.exists(os.path.dirname(outfile)):
            try:
                os.makedirs(os.path.dirname(outfile))
            except OSError as error:
                if error.errno != errno.EEXIST:
                    raise LuciferFailedToCompile(f"Failed to compile {mainFile} with c"
                                                 f" due to not enough permissions")
        command = f"{self._CC if not useCPP else self._CPP} -o {outfile} -shared -fPIC {filesString}"
        if verbose:
            command += " -v"
        if verbose and not silent:
            print(f"Command: {command}")
        autoSilenceCommand(command, silent=silent, verbose=verbose)
        if not silent:
            print("Compiling Complete!")
        return outfile

    def cppToShared(self, mainFile, extern_files=None, out="builds/", verbose=False, silent=False):
        outfile = self.cToShared(
            mainFile, extern_files=extern_files, out=out, verbose=verbose, silent=silent, useCPP=True
        )
        return outfile

    def fetchExtension(self):
        if self._systemData.IS_WINDOWS:
            return ".dll"
        if self._systemData.IS_DARWIN:
            return ".dylib"
        return ".so"

    def compileAuto(self, mainFile, extern_files=None, out="builds/", verbose=False, silent=False):
        _, ext = os.path.splitext(mainFile)
        if ext.lower() in [".c", ".cc", "c", "cc"]:
            return self.cToShared(mainFile, extern_files=extern_files, out=out, verbose=verbose, silent=silent)
        if ext.lower() in [".cpp", "cpp"]:
            return self.cppToShared(mainFile, extern_files=extern_files, out=out, verbose=verbose, silent=silent)
        return None
