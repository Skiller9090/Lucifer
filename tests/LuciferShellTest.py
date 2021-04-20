from LMI import LTF
from lucifer.Shell import Shell


class LuciferShellTest(LTF.Tests.BooleanTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, requirements=[LTF.Requirements.RequireLuciferManager])
        self.luciferManager = None

    def test_create_shell(self):
        self.luciferManager.current_shell_id = 0
        self.luciferManager.main_shell = Shell(self.luciferManager.next_shell_id, self.luciferManager)
        self.luciferManager.next_shell_id += 1
        return True

    def test_load_module(self):
        self.luciferManager.main_shell.use_module(["auxiliary/test_module"])
        return True

    def test_run_module(self):
        if self.luciferManager.main_shell.module_obj is not None:
            self.luciferManager.main_shell.module_obj.isShellRun = False
            self.luciferManager.main_shell.module_obj.run()
            return True
        return False
