from lucifer.Errors import NoShellError


def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


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
