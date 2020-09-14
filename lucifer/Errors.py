from subprocess import CalledProcessError
import pybrake

notifier = pybrake.Notifier(project_id=297340,
                            project_key='bc600da5fe7ba7a73119a2d84519793d',
                            environment='production')


class BaseLuciferError(Exception):
    def __init__(self, message):
        """Store Error Details"""
        self.message = message


class IncompatibleSystemError(BaseLuciferError):
    def __str__(self):
        """Error Output"""
        return "Incompatible System Error: " + str(self.message)


class NoShellError(BaseLuciferError):
    def __str__(self):
        """Error Output"""
        return "No Shell Error Error: " + str(self.message)


class ArgumentUndefinedError(BaseLuciferError):
    def __str__(self):
        """Error Output"""
        return "Argument Undefined: " + str(self.message)


class LuciferFileNotFound(BaseLuciferError):
    def __str__(self):
        """Error Output"""
        return "File Does Not Exist: " + str(self.message)


class LuciferSettingNotFound(BaseLuciferError):
    def __str__(self):
        """Error Output"""
        return "Lucifer Setting Not Found: " + str(self.message)


def checkErrors(e, ModuleError=False):
    try:
        raise e
    except IncompatibleSystemError:
        print(e)
    except NoShellError:
        print(e)
    except CalledProcessError:
        pass
    except ArgumentUndefinedError:
        print(e)
    except LuciferFileNotFound:
        print(e)
        raise e
    # except LuciferSettingNotFound:
    #     print(e)
    #     print("If Error Continues Try Removing 'settings.yml'")
    except Exception as err:
        if not ModuleError:
            notifier.notify(err)
            print("The following error has occurred" +
                  " and has been reported to the devs: ")
            raise err
        else:
            notifier.notify(err)
            print("The Following Error Occurred In Current Module, Reported To Devs...\n"+str(err))


