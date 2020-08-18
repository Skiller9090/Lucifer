from lucifer.Errors import NoShellError


class BaseModule:
    def __init__(self, luciferManager, ShellRun=False):
        self.luciferManager = luciferManager
        self.actions = []
        self.isShellRun = ShellRun
        self.shell = self.luciferManager.main_shell if self.luciferManager.current_shell_id == 0 else None
        if self.shell is None:
            for shell in self.luciferManager.alternative_shells:
                if shell.id == self.luciferManager.current_shell_id:
                    self.shell = shell
                    break
            else:
                raise NoShellError("Couldn't Find Shell With ID: "+str(self.luciferManager.current_shell_id))

    def run(self):
        for action in self.actions:
            action()

    def set_vars(self):
        new_vars = {
        }
        return new_vars

    def get_description(self):
        desc = """This Module Has No Description!"""
        return desc