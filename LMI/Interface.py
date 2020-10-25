from lucifer import uniglobal


class LuciferManagerInterface:
    def __init__(self):
        self.cache = {}
        self.luciferManager = None

    def init(self):
        self.luciferManager = uniglobal.luciferManager
        self.luciferManager.isLMI = True
        print("LMI Loaded!")
