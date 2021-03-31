from subprocess import CalledProcessError

import pybrake

notifier = pybrake.Notifier(project_id=297340,
                            project_key='bc600da5fe7ba7a73119a2d84519793d',
                            environment='production')


class PrintableError(Exception):
    pass


class BaseLuciferError(Exception):
    def __init__(self, message):
        """Store Error Details"""
        self.message = message


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


class LuciferCCompilerNotFound(BaseLuciferError, PrintableError):
    def __str__(self):
        """Error Output"""
        return f"Could not find a c compiler: {str(self.message)}"


class LuciferCPPCompilerNotFound(BaseLuciferError, PrintableError):
    def __str__(self):
        """Error Output"""
        return f"Could not find a c++ compiler: {str(self.message)}"


class LuciferFailedToCompile(BaseLuciferError, PrintableError):
    def __str__(self):
        """Error Output"""
        return f"Failed to compile: {str(self.message)}"


class LuciferFailedToFind(BaseLuciferError, PrintableError):
    def __str__(self):
        """Error Output"""
        return f"Failed to find: {str(self.message)}"


def checkErrors(e, ModuleError=False):
    try:
        raise e
    except PrintableError:
        print(e)
    except CalledProcessError:
        pass
    except LuciferSettingNotFound:
        print(e)
        print("If Error Continues Try Removing 'settings.yml'")
    except Exception as err:
        notifier.notify(err)
        if not ModuleError:
            print("The following error has occurred" +
                  " and has been reported to the devs: ")
            raise err
        print("The Following Error Occurred In Current Module, Reported To Devs...\n" + str(err))
