class BaseModule:
    def __init__(self, luciferManager):
        self.luciferManager = luciferManager
        self.actions = []

    def run(self):
        for action in self.actions:
            action()
