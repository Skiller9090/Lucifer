from LMI.CLang import clang
from modules.Module import BaseModule


class Module(BaseModule):
    def run(self):
        cWorking = False
        cppWorking = False
        possibleCompiles = clang.getPossibleCompiles()
        if possibleCompiles["c"]:
            cTestLib = clang.load("Tests/cTests")
            output = cTestLib.runTests()
            if output == 60:
                cWorking = True
        else:
            print("No compiler to compile c sources, please install gcc and place in current environment!")

        if possibleCompiles["cpp"]:
            cppTestLib = clang.load("Tests/cppTests")
            output = cppTestLib.runTests()
            if output == 60:
                cppWorking = True
        else:
            print("No compiler to compile c++ sources, please install g++ and place in current environment!")

        print(f"c: {'working' if cWorking else 'not working'}")
        print(f"c++: {'working' if cppWorking else 'not working'}")

    def set_vars(self):
        default_vars = {
        }
        return default_vars

    def get_description(self):
        desc = """This module test to see if lucifer's c and c++ module extension is working correctly."""
        return desc
