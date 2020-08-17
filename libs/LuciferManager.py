from . import termcolor
from . import colorama


class LuciferManager:
    def __init__(self):
        self.main_shell = None
        self.alternative_shells = []
        self.gui = False
        self.next_shell_id = 0
        self.shell_recur = 0
        self.colorama = colorama
        self.termcolor = termcolor

    def end(self, *args, **kwargs):
        print("Thank you for using Lucifer, see you next time!")
        exit(0)
