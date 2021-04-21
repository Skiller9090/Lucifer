from .Requirement import Requirement


class RequireLuciferManager(Requirement):
    def satisfyRequirement(self):
        from LMI import LMI
        self.instance.luciferManager = LMI.luciferManager

    def check_satisfied(self):
        if hasattr(self.instance, "luciferManger"):
            return True
        return False
