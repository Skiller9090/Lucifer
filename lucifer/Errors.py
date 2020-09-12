from subprocess import CalledProcessError


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


def checkErrors(e):
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
