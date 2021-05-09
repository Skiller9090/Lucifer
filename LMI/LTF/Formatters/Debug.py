from .Utils import map_failed_test


class Debug:
    def __init__(self, statistics):
        self.statistics = statistics

    def generate_display(self):
        data = ""
        for testSet in self.statistics:
            data += "====Test: " + testSet.__class__.__name__ + "====\n\n"
            for test in self.statistics[testSet]:
                testData = self.statistics[testSet][test]
                data += "----" + test + "----\n"
                data += "Succeeded: " + map_failed_test(testData["failed"]) + "\n"
                data += "Time Taken: " + str(testData["time"]) + "\n"
                data += "Errors:"
                if len(testData["errors"]) < 1:
                    data += " No errors\n"
                else:
                    data += f" {len(testData['errors'])} Errors-\n"
                    for error in testData["errors"]:
                        data += f"\t{error}\n"
                data += "\n"
        return data

    def show(self):
        print(self.generate_display())
