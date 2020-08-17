class IncompatibleSystemError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "Incompatible System Error: " + str(self.message)