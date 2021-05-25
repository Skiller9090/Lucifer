from .LTFTest import LTFTest


class LTFSkippedTest(LTFTest):
    def __init__(self, name, reason, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.reason = reason

    def run(self):
        self.test_mappings[self.name] = {
            "time": None,
            "has_run": True,
            "errors": [],
            "failed": None
        }
        self.addError(self.name, Exception(self.reason), failed=None)
