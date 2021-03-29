from lucifer import Uniglobal


class LuciferManagerInterface:
    instance = None

    def __init__(self):
        if LuciferManagerInterface.instance is None:
            LuciferManagerInterface.instance = self
            self.cache = {}
            self.luciferManager = None

    def init(self):
        self.luciferManager = Uniglobal.luciferManager
        self.luciferManager.isLMI = True
        print("LMI Loaded!")


LuciferManagerInterface()
LMI = LuciferManagerInterface.instance  # Earliest Definition
