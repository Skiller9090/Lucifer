class LFTError(Exception):
    def __init__(self, message):
        self.message = message
        self.__class__.__module__ = "LTF"

    def raiseError(self):
        raise self

    def __str__(self):
        return f"{self.message}"

    def __repr__(self):
        return f"<{self.__class__.__name__}, message='{self.message}'>"
