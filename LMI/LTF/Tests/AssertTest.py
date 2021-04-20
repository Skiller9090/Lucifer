from .LTFTest import LTFTest
import timeit


class AssertTest(LTFTest):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        for test_func in args:
            self.extra_tests.append(test_func)

    def run(self):
        self.find_functions()
        self.satisfyRequirements()
        for functionName in self.all_functions:
            function = self.all_functions[functionName]
            self.test_mappings[functionName] = {
                "time": None,
                "has_run": False,
                "errors": [],
                "failed": False
            }
            try:
                timeTaken = timeit.timeit(lambda: function(self), number=1)
                self.test_mappings[functionName]["time"] = timeTaken
            except AssertionError as e:
                self.test_mappings[functionName]["errors"].append(e)
                self.test_mappings[functionName]["failed"] = True
            self.test_mappings[functionName]["has_run"] = True
        self.has_run = True

