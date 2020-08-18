from subprocess import CalledProcessError


class IncompatibleSystemError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "Incompatible System Error: " + str(self.message)


class NoShellError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "No Shell Error Error: " + str(self.message)


def checkErrors(e):
    try:
        raise e
    except IncompatibleSystemError:
        print(e)
    except NoShellError:
        print(e)
    except CalledProcessError:
        pass
