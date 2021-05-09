from lucifer import Uniglobal
from ._SystemData import _SystemData


class LuciferModuleInterfaceManager:
    instance = None

    def __init__(self):
        if LuciferModuleInterfaceManager.instance is None:
            LuciferModuleInterfaceManager.instance = self
            self.cache = {}
            self.luciferManager = None
            self._systemData = _SystemData.getInstance()

    def init(self):
        self.luciferManager = Uniglobal.luciferManager
        self.luciferManager.isLMI = True
        print("LMI Loaded!")

    @property
    def systemData(self):
        return self._systemData


LuciferModuleInterfaceManager()
LMI = LuciferModuleInterfaceManager.instance  # Earliest Definition
