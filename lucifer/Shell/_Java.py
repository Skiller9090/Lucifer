import LMI.Java.Installs


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