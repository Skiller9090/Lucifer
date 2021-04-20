from .Errors import NotLTFTestError
from .Tests import AssertTest, LTFTest


class TestsRunner:
    def __init__(self):
        self.tests = {}
        self.statistics = {}

    def runAll(self):
        for test in self.tests.keys():
            if isinstance(test, LTFTest):
                test.run()
                self.statistics[test] = test.test_mappings
            else:
                raise NotLTFTestError("Not a LTF Test compatible Test!")

    def add_function_assert_test(self, testFunction):
        self.tests[AssertTest(testFunction)] = {
            "hasRun": False,
            "Failed": False,
            "Time": None,
            "Error": None
        }

    def add_LTF_test(self, LTFClass):
        if isinstance(LTFClass, type):
            LTFClass = LTFClass()
        self.tests[LTFClass] = {
            "hasRun": False,
            "Failed": False,
            "Time": None,
            "Error": None
        }
