from .Requirement import Requirement


class RequireJavascriptEnabled(Requirement):
    def satisfyRequirement(self):
        pass

    def check_satisfied(self):
        from LMI.Javascript import isJs2PyInstalled
        if isJs2PyInstalled:
            return True
        return False
