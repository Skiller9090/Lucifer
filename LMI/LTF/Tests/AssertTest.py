from .LTFTest import LTFTest


class AssertTest(LTFTest):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        for test_func in args:
            self.extra_tests.append(test_func)

    def run(self):
        self.findFunctions()
        allSatisfied = self.satisfyRequirements()
        for functionName, function in zip(self.all_functions.keys(), self.all_functions.values()):
            if not allSatisfied:
                self.test_mappings[functionName]["failed"] = None
                self.addError(functionName, Exception("Failed to satisfy requirements for the test set!"))
                continue
            self.setDefaultTestValues(functionName)
            try:
                timeTaken = self.timeFunction(function)
                self.test_mappings[functionName]["time"] = timeTaken
            except Exception as e:
                self.addError(functionName, e)
            self.test_mappings[functionName]["has_run"] = True
        self.has_run = True
