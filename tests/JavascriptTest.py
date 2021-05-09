from LMI import LTF
from LMI.Javascript.JsFile import JsFile


class JavascriptTests(LTF.Tests.BooleanTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, requirements=[LTF.Requirements.RequireJavascriptEnabled])
        self.jsLoadedTests = None

    def test_Javascript(self):
        jsFile = JsFile("external-modules/javascript/sources/lucifer/tests/test.js")
        self.jsLoadedTests = jsFile.importFile()
        if int(self.jsLoadedTests.simpleMathTest1()) == 100 and int(self.jsLoadedTests.simpleMathTest2()) == 300:
            return True
        return False

    def test_Javascript_lucifer_API_access(self):
        return self.jsLoadedTests.canAccessLuciferAPI()

    def test_Javascript_lucifer_manager_access(self):
        return self.jsLoadedTests.canAccessLuciferManager()
