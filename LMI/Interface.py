from lucifer import uniglobal


class LuciferManagerInterface:
    instance = None

    def __init__(self):
        if LuciferManagerInterface.instance is None:
            LuciferManagerInterface.instance = self
            self.cache = {}
            self.luciferManager = None

    def init(self):
        self.luciferManager = uniglobal.luciferManager
        self.luciferManager.isLMI = True
        print("LMI Loaded!")


LuciferManagerInterface()
LMI = LuciferManagerInterface.instance  # Earliest Definition
