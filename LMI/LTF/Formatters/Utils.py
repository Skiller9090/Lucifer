def generate_percent_breakdown(statistics):
    data = ""
    failedTests = 0
    totalTests = 0
    failedTestSets = 0
    totalTestSets = 0
    for testSet in statistics:
        setFailed = False
        for test in statistics[testSet]:
            testData = statistics[testSet][test]
            if testData["failed"]:
                failedTests += 1
                setFailed = True
            totalTests += 1
        if setFailed:
            failedTestSets += 1
        totalTestSets += 1
    data += "#### Final Breakdown ####\n"
    data += "Failed Tests: " + str(failedTests) + "/" + str(totalTests) + "\n"
    data += "Failed Test Sets: " + str(failedTestSets) + "/" + str(totalTestSets) + "\n"
    data += "Test Succeeded: " + str(round(((totalTests - failedTests) / totalTests) * 100, 2)) + "%\n"
    data += "Test Sets Succeeded: " + str(round(
        ((totalTestSets - failedTestSets) / totalTestSets) * 100, 2)
    ) + "%\n"
    return data


def map_failed_test(failed_value):
    return {
        True: "no",
        False: "yes",
        None: "skipped"
    }.get(failed_value, "unknown")
