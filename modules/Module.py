from lucifer.Utils import RetrieveShell


class BaseModule(RetrieveShell):   # All Modules should inherit from BaseModule (this class)
    def __init__(self, luciferManager, ShellRun=False):  # Module setup, DO NOT EDIT, hook onto the 'setup' instead
        self.luciferManager = luciferManager
        self.actions = []
        self.isShellRun = ShellRun
        self.get_shell()
        self.setup()
        self.desc = ""
        self.default_vars = {}

    def setup(self):  # This is a setup hook which will be run on module load
        pass

    def run(self):  # This is a run hook and will be run on the module 'run'
        for action in self.actions:
            action()

    def set_vars(self):  # This is set_vars hook and will return the vars to set when the command 'set_vars' is run
        self.default_vars = {
        }
        return self.default_vars

    def get_description(self):   # This is the description hook, returns a description on command 'description'
        self.desc = """This Module Has No Description!"""
        return self.desc
