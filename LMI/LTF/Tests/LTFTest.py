import abc
import timeit

from ...Utils import RunTimeReturn


class LTFTest(metaclass=abc.ABCMeta):
    testIdentifiers = ["test_"]

    def __init__(self, requirements=None):
        self.requirements = []
        self.all_functions = {}
        self.extra_tests = []
        self.test_mappings = {}
        self.has_run = False
        if requirements is not None:
            for requirement in requirements:
                self.requirements.append(requirement(self))

    def findFunctions(self):
        self.all_functions = {}
        for function in self.extra_tests:
            self.all_functions["extra-" + function.__name__] = function
        for functionName in self.__class__.__dict__.keys():
            for identifier in LTFTest.testIdentifiers:
                if functionName.startswith(identifier):
                    self.all_functions[functionName] = (self.__class__.__dict__.get(functionName))
                    break

    def satisfyRequirements(self):
        allSatisfied = True
        for requirement in self.requirements:
            if not requirement.check_satisfied():
                requirement.satisfyRequirement()
            if not requirement.check_satisfied():
                allSatisfied = False
        return allSatisfied

    def timeWithReturnFunction(self, function):
        with RunTimeReturn() as RTR:
            function = function.__get__(self)
            timeTaken, outValue = RTR.run(function, number=1)
        return timeTaken, outValue

    def timeFunction(self, function):
        function = function.__get__(self)
        timeTaken = timeit.timeit(function, number=1)
        return timeTaken

    def addError(self, functionName, error, failed=True):
        self.test_mappings[functionName]["errors"].append(error)
        self.test_mappings[functionName]["failed"] = failed

    def setDefaultTestValues(self, functionName):
        self.test_mappings[functionName] = {
            "time": None,
            "has_run": False,
            "errors": [],
            "failed": False
        }

    @abc.abstractmethod
    def run(self):
        pass
