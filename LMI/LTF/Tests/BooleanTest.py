from .LTFTest import LTFTest
import timeit


class BooleanTest(LTFTest):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        for test_func in args:
            self.extra_tests.append(test_func)
        self.timeitOld = None

    def setupTimeit(self):
        self.timeitOld = timeit.template
        timeit.template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        retval = {stmt}
    _t1 = _timer()
    return _t1 - _t0, retval
"""

    def exitTimeit(self):
        timeit.template = self.timeitOld

    def run(self):
        self.find_functions()
        self.satisfyRequirements()
        self.setupTimeit()
        for functionName in self.all_functions:
            function = self.all_functions[functionName]
            self.test_mappings[functionName] = {
                "time": None,
                "has_run": False,
                "errors": [],
                "failed": False
            }
            timeTaken, outValue = timeit.timeit(lambda: function(self), number=1)
            self.test_mappings[functionName]["time"] = timeTaken
            if outValue is None:
                self.test_mappings[functionName]["failed"] = None
            elif not outValue:
                self.test_mappings[functionName]["errors"].append(Exception("Failed boolean test"))
                self.test_mappings[functionName]["failed"] = True
            self.test_mappings[functionName]["has_run"] = True
        self.has_run = True
        self.exitTimeit()
