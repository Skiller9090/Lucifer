from LMI import LTF


class AssertTests(LTF.Tests.AssertTest):
    def __init__(self, *args):
        super().__init__(*args, requirements=[])
        self.luciferManager = None

    @staticmethod
    def test_Assert():
        assert 1 == 1


class BooleanTests(LTF.Tests.BooleanTest):
    def __init__(self, *args):
        super().__init__(*args, requirements=[])

    @staticmethod
    def test_Boolean():
        return True
