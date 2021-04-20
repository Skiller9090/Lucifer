from LMI import LTF
from LMI.CLang.MakeCL.MakeCLFile import MakeCLFile


class CLMakeTests(LTF.Tests.BooleanTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, requirements=[])
        self.makeCLFIle = None

    def test_MakeCL_load_file(self):
        try:
            self.makeCLFIle = MakeCLFile("external-modules/c/sources/Tests/make.clucifer")
            return True
        except Exception as e:
            _ = e
            return False

    def test_MakeCL_Lexed_Parse(self):
        try:
            self.makeCLFIle.getFileDirectives()
            return True
        except Exception as e:
            _ = e
            return False
