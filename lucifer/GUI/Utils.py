import re
from tkinter import messagebox

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


class Closer:
    def on_close(self):
        if messagebox.askokcancel("Quit Lucifer", "Are you sure you want to quit Lucifer?"):
            self.luciferManager.end()


