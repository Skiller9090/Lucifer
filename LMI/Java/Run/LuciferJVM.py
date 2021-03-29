import os
import re
import sys

import jpype

from lucifer.Errors import LuciferJavaBinaryNotFound, LuciferJVMPathNotFound, LuciferJavaBinPathNotFound


class LuciferJVM:
    def __init__(self):
        self.JVMPath = None
        self.JavaRootPath = None
        self.JavaBinPath = None
        self.JavaJavacPath = None
        self.JavaJarPath = None
        self.luciferJarName = "luciferJavaModules.jar"
        self.luciferJavaModulesPath = "external-modules/java/"
        self.luciferJavaBuildPath = os.path.abspath(os.path.join(self.luciferJavaModulesPath, "builds/"))
        self.luciferJavaSrcPath = os.path.abspath(os.path.join(self.luciferJavaModulesPath, "java/"))
        self.isLuciferJarLoaded = False

    def setJavaPath(self, path):
        if self.isJVMRunning:
            return
        self.JavaRootPath = os.path.abspath(path)
        foundJVM = self.findJVM()
        if not foundJVM:
            raise LuciferJVMPathNotFound(path)
        foundBinPath = self.findBinPath()
        if not foundBinPath:
            raise LuciferJavaBinPathNotFound(path)
        self.findBinaries()

    def getJavaMajorVersion(self):
        if self.JavaRootPath is None:
            return None
        if self.isJVMRunning:
            return self.getRunningJavaMajorVersion()
        dirName = os.path.abspath(self.JavaRootPath).split(os.sep)[-1]
        dirName = dirName.replace("jdk", "")
        dirName = dirName.replace("u", ".")
        if "-" == dirName[0]:
            dirName = dirName[1:]
        if dirName.startswith("1."):
            return int(dirName.split(".")[1])
        return int(dirName.split(".")[0])

    def findJVM(self):
        found = None
        for dirPath, _, files in os.walk(self.JavaRootPath):
            for filename in files:
                fName = os.path.join(dirPath, filename)
                if re.match('.*jvm.*(dll|so|dylib)', fName):
                    found = fName
                    break
            else:
                continue
            break
        self.JVMPath = found
        if found is not None:
            return True
        return False

    def findBinPath(self):
        found = None
        for dirPath, dirs, files in os.walk(self.JavaRootPath):
            for dirName in dirs:
                dName = os.path.join(dirPath, dirName)
                if re.match('.*bin$', dName):
                    found = dName
                    break
            else:
                continue
            break
        self.JavaBinPath = found
        if found is not None:
            return True
        return False

    def findBinaries(self):
        javacName = "javac.exe" if os.name == "nt" else "javac"
        jarName = "jar.exe" if os.name == "nt" else "jar"

        if os.path.exists(os.path.join(self.JavaBinPath, javacName)):
            self.JavaJavacPath = os.path.join(self.JavaBinPath, javacName)
        else:
            raise LuciferJavaBinaryNotFound(f"{javacName} In {self.JavaBinPath}")

        if os.path.exists(os.path.join(self.JavaBinPath, jarName)):
            self.JavaJarPath = os.path.join(self.JavaBinPath, jarName)
        else:
            raise LuciferJavaBinaryNotFound(f"{jarName} In {self.JavaBinPath}")

    def startJVM(self, javaPath=None):
        if self.isJVMRunning:
            return
        if javaPath is not None:
            self.setJavaPath(javaPath)
        jpype.startJVM(self.JVMPath, "-ea", convertStrings=False)
        print("Started JVM!")

    def setSTDOUT(self):
        if self.JavaRootPath is None or not self.isJVMRunning:
            return None
        # updated to @JImplements
        stdoutPipe = jpype.JProxy("com.github.skiller9090.stdredirect.PythonPipe", inst=sys.stdout)
        # stderrPipe = jpype.JProxy("com.github.skiller9090.stdredirect.PythonPipe", inst=sys.stderr)
        out_stream = jpype.JClass("com.github.skiller9090.stdredirect.PythonPrintStream")()
        out_stream.setPythonStdout(stdoutPipe)
        # err_stream = jpype.JClass("com.github.skiller9090.stdredirect.PythonOutputStream")()
        # err_stream.setPythonStdout(stderrPipe)
        ps = jpype.JClass("java.io.PrintStream")
        jpype.java.lang.System.setOut(ps(out_stream))
        # jpype.java.lang.System.setErr(ps(err_stream))

    def getRunningJavaMajorVersion(self):
        if self.JavaRootPath is None or not self.isJVMRunning:
            return None
        System = jpype.java.lang.System
        version = str(System.getProperty("java.version"))
        index = 1 if version.startswith("1.") else 0
        version = version.split(".")[index]
        return int(version)

    @property
    def isJVMRunning(self):
        return jpype.isJVMStarted()

    @staticmethod
    def addJarToClassPath(path, verbose=False):
        if verbose:
            print(f"Adding {path} to class Path")
        jpype.addClassPath(
            os.path.abspath(path)
        )
        if verbose:
            print(f"Added {path} to class Path")

    def addLuciferJar(self, verbose=False):
        if self.isLuciferJarLoaded:
            if verbose:
                print("Already Loaded Lucifer Jar!")
            return
        jarLocation = os.path.abspath(os.path.join(
            self.luciferJavaBuildPath,
            f"java-{luciferJVM.getJavaMajorVersion()}/{self.luciferJarName}"
        ))
        if not os.path.exists(jarLocation):
            print("Jar has not been build, please build jar first")
            return
        self.addJarToClassPath(jarLocation, verbose=verbose)
        print(jpype.getClassPath())
        self.isLuciferJarLoaded = True

    @staticmethod
    def getPackage(package):
        return jpype.JPackage(package)

    @staticmethod
    def getClass(classPath):
        return jpype.JClass(classPath)


luciferJVM = LuciferJVM()
