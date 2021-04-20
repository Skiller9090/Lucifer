from LMI import LTF


class AssertTests(LTF.Tests.AssertTest):
    def __init__(self, *args):
        super().__init__(*args, requirements=[])
        self.luciferManager = None

    def test_Assert_Test(self):
        assert 1 == 1


class BooleanTests(LTF.Tests.BooleanTest):
    def __init__(self, *args):
        super().__init__(*args, requirements=[])

    def test_Boolean_Tests(self):
        return True
