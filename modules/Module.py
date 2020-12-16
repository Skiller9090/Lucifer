from lucifer.Utils import RetrieveShell


class BaseModule(RetrieveShell):
    """All Modules should inherit from BaseModule (this class)"""
    def __init__(self, luciferManager, ShellRun=False):
        """Module setup, DO NOT EDIT, hook onto the 'setup' instead"""
        self.pre_setup()
        self.luciferManager = luciferManager
        self.actions = []
        self.isShellRun = ShellRun
        self.get_shell()
        self.setup()
        self.desc = ""
        self.default_vars = {}
        self.post_setup()

    def pre_setup(self):
        """This is a setup hook which runs on module load, this happens first on load"""
        pass

    def setup(self):
        """This is a setup hook which will be run on module load, this happens after getting
        luciferManager and getting shell"""
        pass

    def post_setup(self):
        """This is the final setup hook which will run last on module setup, after setting desc and vars"""
        pass

    def run(self):
        """This is a run hook and will be run on the module 'run'"""
        for action in self.actions:
            action()

    def set_vars(self):
        """This is set_vars hook and will return the vars to set when the command 'set_vars' is run"""
        return self.default_vars

    def get_description(self):
        """This is the description hook, returns a description on command 'description'"""
        self.desc = """This Module Has No Description!"""
        return self.desc
