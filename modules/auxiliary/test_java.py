from modules.Module import BaseModule
from LMI import Java


class Module(BaseModule):
    def run(self):
        javaCheck = Java.Utils.checkJavaRequirements()
        if javaCheck is False:
            return

        if not Java.Run.luciferJVM.isLuciferJarLoaded:
            print("Lucifer Module Jar is not loaded!")
            return

        testPackage = Java.Run.luciferJVM.getPackage("com.github.skiller9090.test")
        testClass = testPackage.TestClass()
        if testClass.getTest() != 0:
            print("Java tests failed, testClass.getTest() does not equal zero!")
            return
        testClass.setTest(10)
        if testClass.getTest() != 10:
            print("Java tests failed, testClass.setTest() failed to set value to 10!")
            return
        print("Java is working!")

    def set_vars(self):
        default_vars = {
        }
        return default_vars

    def get_description(self):
        desc = """This module test to see if lucifer's java module extension is working correctly."""
        return desc
