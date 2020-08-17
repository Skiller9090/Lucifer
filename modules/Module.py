class BaseModule:
    def __init__(self, luciferManager, ShellRun=False):
        self.luciferManager = luciferManager
        self.actions = []
        self.isShellRun = ShellRun

    def run(self):
        for action in self.actions:
            action()
