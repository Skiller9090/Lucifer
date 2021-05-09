from .Requirement import Requirement


class RequireLuciferManager(Requirement):
    def satisfyRequirement(self):
        from LMI import LMI
        if hasattr(self.instance, "luciferManager"):
            self.instance.luciferManager = LMI.luciferManager
        else:
            setattr(self.instance, "luciferManager", LMI.luciferManager)

    def check_satisfied(self):
        if hasattr(self.instance, "luciferManager") and self.instance.luciferManager is not None:
            return True
        return False
