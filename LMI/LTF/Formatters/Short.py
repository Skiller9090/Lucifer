from .Utils import map_failed_test


class Short:
    def __init__(self, statistics):
        self.statistics = statistics

    def generate_display(self):
        data = ""
        for testSet in self.statistics:
            data += "====Test: " + testSet.__class__.__name__ + "====\n"
            for test in self.statistics[testSet]:
                testData = self.statistics[testSet][test]
                data += test + ": " + map_failed_test(testData["failed"]) + "\n"
            data += "\n"
        return data

    def show(self):
        print(self.generate_display())
