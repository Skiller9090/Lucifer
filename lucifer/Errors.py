from subprocess import CalledProcessError

import pybrake
from termcolor import colored

notifier = pybrake.Notifier(project_id=297340,
                            project_key='bc600da5fe7ba7a73119a2d84519793d',
                            environment='production')


class PrintableError(Exception):
    pass


class BaseLuciferError(Exception):
    def __init__(self, message):
        """Store Error Details"""
        self.message = message


class MakeCLError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.__class__.__name__ + ": " + str(self.message)

    def raiseError(self):
        raise self


class CompilerError(Exception):
    def __init__(self, compiler, message):
        self.message = message
        self.compiler = compiler

    def __str__(self):
        return self.__class__.__name__ + ": " + str(self.message) + " with the " + self.compiler + " compiler"


class IncompatibleSystemError(BaseLuciferError, PrintableError):
    def __str__(self):
        """Error Output"""
        return "Incompatible System Error: " + str(self.message)


class NoShellError(BaseLuciferError, PrintableError):
    def __str__(self):
        """Error Output"""
        return "No Shell Error Error: " + str(self.message)


class ArgumentUndefinedError(BaseLuciferError, PrintableError):
    def __str__(self):
        """Error Output"""
        return "Argument Undefined: " + str(self.message)


class LuciferFileNotFound(BaseLuciferError, PrintableError):
    def __str__(self):
        """Error Output"""
        return "File Does Not Exist: " + str(self.message)


class LuciferSettingNotFound(BaseLuciferError):
    def __str__(self):
        """Error Output"""
        return "Lucifer Setting Not Found: " + str(self.message)


class LuciferAddressInUseError(BaseLuciferError, PrintableError):
    def __str__(self):
        """Error Output"""
        return "Address already in use, so cannot bind to ip and port"


class LuciferJVMPathNotFound(BaseLuciferError, PrintableError):
    def __str__(self):
        """Error Output"""
        return f"Could not find find JVM in: {str(self.message)}"


class LuciferJavaBinPathNotFound(BaseLuciferError, PrintableError):
    def __str__(self):
        """Error Output"""
        return f"Could not find find Bin Directory in: {str(self.message)}"


class LuciferJavaBinaryNotFound(BaseLuciferError, PrintableError):
    def __str__(self):
        """Error Output"""
        return f"Could not find find Binary: {str(self.message)}"


class CCompilerNotFound(CompilerError):
    pass


class CPPCompilerNotFound(CompilerError):
    pass


class FailedToCompileError(CompilerError):
    pass


class LuciferFailedToFind(BaseLuciferError, PrintableError):
    def __str__(self):
        """Error Output"""
        return f"Failed to find: {str(self.message)}"


def checkErrors(e, ModuleError=False):
    try:
        raise e
    except PrintableError:
        print(colored(e, "red"))
    except MakeCLError:
        print(colored(e, "red"))
    except CompilerError:
        print(colored(e, "red"))
    except CalledProcessError:
        pass
    except LuciferSettingNotFound:
        print(colored(e, "red"))
        print("If Error Continues Try Removing 'settings.yml'")
    except Exception as err:
        notifier.notify(err)
        if not ModuleError:
            print("The following error has occurred" +
                  " and has been reported to the devs: ")
            raise err
        print("The Following Error Occurred In Current Module, Reported To Devs...\n" + str(err))
