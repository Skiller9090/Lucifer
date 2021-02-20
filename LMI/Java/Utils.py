from . import Run


def checkJavaRequirements():
    if not Run.isJPypeInstalled:
        print(
            "You do not have 'jpype1' installed so you can not use lucifer java extensions!"
        )
        return False
    if not Run.luciferJVM.isJVMRunning:
        print(
            "You have not started your java JVM please start it before running this module!"
        )
        return False
    return True
