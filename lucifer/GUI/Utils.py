import re
from tkinter import messagebox

from lucifer.Errors import NoShellError

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


class Closer:
    def on_close(self):
        if messagebox.askokcancel("Quit Lucifer", "Are you sure you want to quit Lucifer?"):
            self.luciferManager.end()


class RetrieveShell:
    def get_shell(self):
        self.shell = self.luciferManager.main_shell if self.luciferManager.current_shell_id == 0 else None
        if self.shell is None:
            for shell in self.luciferManager.alternative_shells:
                if shell.id == self.luciferManager.current_shell_id:
                    self.shell = shell
                    break
            else:
                raise NoShellError("Couldn't Find Shell With ID: " + str(self.luciferManager.current_shell_id))
