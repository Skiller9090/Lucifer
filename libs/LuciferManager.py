from . import termcolor
from . import colorama


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

    def end(self, *args, **kwargs):
        print("Thank you for using Lucifer, see you next time!")
        exit(0)
