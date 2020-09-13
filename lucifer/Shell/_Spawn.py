def spawn(self):
    if self.luciferManager.gui is None:
        while True:
            self.getIn()
            signal = self.parseShellIn()
            if signal == 7:
                break


def spawn_shell(self, *args, **kwargs):
    from . import Shell
    self.luciferManager.alternative_shells.append(Shell(self.luciferManager.next_shell_id, self.luciferManager))
    self.luciferManager.next_shell_id += 1
    self.luciferManager.alternative_shells[-1].name += str(self.luciferManager.next_shell_id - 1)
    print(f"Opened New Shell With ID: {self.luciferManager.next_shell_id - 1}")

