from LMI import Reports
import os


def newReport(self, com_args):
    if len(com_args) < 2:
        if com_args[0] == "report_new":
            print("You need to add a file name to create a new report!")
            print("EX: report_new myNewReport")
        else:
            print("You need to add a file name to open a new report!")
            print("EX: report_open myNewReport")
            print("Note: will create the report if doesn't exist")
        return
    fileName = com_args[1]
    reportFile = os.path.join(Reports.HTMLReport.path,
                              fileName if fileName.lower().endswith(".html") else (fileName + ".html"))
    if not os.path.exists(os.path.abspath(reportFile)):
        print("Report file does not exist, creating a new one!")

    Reports.HTMLReport.newReport(fileName)
    print(f"Opened report file: {Reports.HTMLReport.name}")


def startReporting(self, com_args):
    Reports.isReporting = True
    print("Reporting On")


def pauseReporting(self, com_args):
    Reports.isReporting = False
    print("Reporting Off")
