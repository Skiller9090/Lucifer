from lucifer.Errors import MakeCLError


class MakeCLInvalidFileError(MakeCLError):
    def __init__(self, message):
        super().__init__(message)


class MakeCLInvalidKeywordError(MakeCLError):
    def __init__(self, message):
        super().__init__(message)


class MakeCLInvalidCharacterError(MakeCLError):
    def __init__(self, message):
        super().__init__(message)


class MakeCLInvalidStateError(MakeCLError):
    def __init__(self, message):
        super().__init__(message)


class MakeCLInvalidTooManyArgsError(MakeCLError):
    def __init__(self, message):
        super().__init__(message)
