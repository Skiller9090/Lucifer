import LMI
from LMI import Utils
from LMI.Java.Installs.List import get_lucifer_java_versions


def _getVerbose(com_args):
    verbose = True
    vv = False
    if "-vv" in com_args:
        vv = True
    if "-s" in com_args or "--silent" in com_args:
        verbose = False
    return verbose, vv


def installJava(self, com_args):
    if len(com_args) < 2:
        print("Please add a java version to install!")
        return
    verbose, vv = _getVerbose(com_args)
    LMI.Java.Installs.install(com_args[1], verbose=verbose, vv=vv)


def reinstallJava(self, com_args):
    if len(com_args) < 2:
        print("Please add a java version to reinstall!")
        return
    verbose, vv = _getVerbose(com_args)
    LMI.Java.Installs.reinstall(com_args[1], verbose=verbose, vv=vv)


def uninstallJava(self, com_args):
    if len(com_args) < 2:
        print("Please add a java version to uninstall!")
        return
    if com_args[1] == "*":
        com_args[1] = ""
        print("Uninstalling ALL lucifer java installations!")
    verbose, vv = _getVerbose(com_args)
    LMI.Java.Installs.uninstall(com_args[1], verbose=verbose, vv=vv)


def getJavaInstalls(self, com_args):
    print(LMI.Java.Installs.getVersions())


def setJavaJDK(self, com_args):
    if len(com_args) < 2:
        print("Please add a Java JDK ID to use, to get IDs run 'get_installs_java' command!")
        return
    if LMI.Java.Run.luciferJVM.isJVMRunning:
        print("Can not set Java JDK for lucifer when JVM is already running!\nPlease restart lucifer to start a "
              "different version of Java JDK")
        return
    if not Utils.check_int(com_args[1]):
        print("The Java JDK ID needs to be an integer!")
        return
    javaVersions = get_lucifer_java_versions()
    javaIndex = abs(int(com_args[1]))
    if len(javaVersions) - 1 < javaIndex:
        print("Invalid Java ID!")
        return
    javaVersion = javaVersions[list(javaVersions.keys())[javaIndex]]
    LMI.Java.Run.luciferJVM.setJavaPath(
        javaVersion["folderPath"]
    )
    print(f"JDK set to: {javaVersion['folderName']}")


def startJavaJVM(self, com_args):
    if LMI.Java.Run.luciferJVM.isJVMRunning:
        print("Java JVM already running, to change java version restart lucifer!")
        return
    LMI.Java.Run.luciferJVM.startJVM()


def buildJar(self, com_args):
    LMI.Java.Run.compiler.createLuciferModuleJar()
    print("Lucifer Module Jar Build Complete!")


def loadLuciferJar(self, com_args):
    if not LMI.Java.Run.luciferJVM.isJVMRunning:
        print("Please start jvm first then run command!")
        return
    LMI.Java.Run.luciferJVM.addLuciferJar()
    LMI.Java.Run.luciferJVM.setSTDOUT()
    print("Loaded Lucifer Module Jar!")
