class Requirement:
    def __init__(self, instance):
        self.instance = instance
        self.isSatisfied = False

    def check_satisfied(self):
        return self.isSatisfied

    def satisfyRequirement(self):
        self.isSatisfied = True
