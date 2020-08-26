from libs import termcolor
from libs import colorama
import sys

class LuciferManager:
    def __init__(self, auto_vars=False):
        self.main_shell = None
        self.alternative_shells = []
        self.gui = False
        self.next_shell_id = 0
        self.shell_recur = 0
        self.colorama = colorama
        self.termcolor = termcolor
        self.current_shell_id = 0
        self.auto_vars = auto_vars
        self.log_file = None
        self.log_amount = 0
        self.gui = None
        self.gui_thread_free = True
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    def end(self, *args, **kwargs):
        print("Thank you for using lucifer, see you next time!")
        exit(0)
        if self.log_amount > 0:
            if self.log_file is not None:
                self.log_file.close()

    def log_command(self, command):
        with open(self.log_file, "a") as f:
            f.write(f"Command:> {str(command)}\n")
