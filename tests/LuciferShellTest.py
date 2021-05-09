from LMI import LTF
from lucifer.Shell import Shell


class LuciferShellTest(LTF.Tests.BooleanTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, requirements=[LTF.Requirements.RequireLuciferManager])
        self.luciferManager = None
        self.testShell = None

    def test_create_shell(self):
        if self.luciferManager.main_shell is not None:
            self.luciferManager.alternative_shells.append(
                Shell(self.luciferManager.next_shell_id, self.luciferManager)
            )
            self.testShell = self.luciferManager.alternative_shells[-1]
        else:
            self.luciferManager.main_shell = Shell(self.luciferManager.next_shell_id, self.luciferManager)
            self.testShell = self.luciferManager.main_shell
        self.luciferManager.next_shell_id += 1
        return True

    def test_load_module(self):
        self.testShell.use_module(["auxiliary/test_module"])
        return True

    def test_run_module(self):
        if self.testShell.module_obj is not None:
            self.testShell.module_obj.isShellRun = False
            self.testShell.module_obj.run()
            return True
        return False

    def test_close_shell(self):
        if self.testShell.is_main:
            self.luciferManager.main_shell = None
        else:
            self.luciferManager.alternative_shells.remove(self.testShell)
        return True
