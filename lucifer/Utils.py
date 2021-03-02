"""
Utils contains a few utility function and classes.

Classes:
    RetrieveShell -  A class to inherit from if you want the child class to be able to get and store the current
                     lucifer shell in the self.shell variable, NOTE: needs to have access to self.luciferManager!
"""
from lucifer.Errors import NoShellError


class RetrieveShell:
    def __init__(self):
        self.shell = None

    def get_shell(self):
        self.shell = self.luciferManager.main_shell \
            if self.luciferManager.current_shell_id == 0 else None
        if self.shell is None:
            for shell in self.luciferManager.alternative_shells:
                if shell.id == self.luciferManager.current_shell_id:
                    self.shell = shell
                    break
            else:
                raise NoShellError("Couldn't Find Shell With ID: " + str(self.luciferManager.current_shell_id))
