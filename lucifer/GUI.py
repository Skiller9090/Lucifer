import tkinter as tk
from tkinter import ttk
from .Errors import NoShellError
import sys
import re

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
font = None


class TextRedirect(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, string):
        self.widget.configure(state="normal")
        self.widget.insert("end", ansi_escape.sub("", string), (self.tag,))
        self.widget.configure(state="disabled")


class LuciferConsole(tk.Frame):
    def __init__(self, luciferManager, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.expand = True
        self.luciferManager = luciferManager
        self.console_in = tk.StringVar()
        self.ConsoleBox = tk.Text(self, font=font)
        self.ConsoleBox.configure(state="disabled")
        self.ConsoleBox.tag_configure("stderr", foreground="#b22222")

        self.yscrollbar = ttk.Scrollbar(self)

        self.ConsoleBox.config(yscrollcommand=self.yscrollbar.set)
        self.yscrollbar.config(command=self.ConsoleBox.yview)
        self.ConsoleInput = ttk.Entry(self, textvariable=self.console_in)
        self.get_shell()

        self.ConsoleBox["bg"] = '#%02x%02x%02x' % (28, 28, 36)
        self.ConsoleBox["foreground"] = '#%02x%02x%02x' % (255, 255, 255)

        self.ConsoleInput.pack(side=tk.BOTTOM, anchor=tk.W, expand=False, fill="x")
        self.yscrollbar.pack(side=tk.RIGHT, fill="y", anchor=tk.E, expand=False)
        self.ConsoleBox.pack(fill="both", side=tk.LEFT, anchor=tk.E, expand=True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.ConsoleInput.bind("<Return>", self.send_command)
        sys.stdout = TextRedirect(self.ConsoleBox, "stdout")
        sys.stderr = TextRedirect(self.ConsoleBox, "stderr")
        print("lucifer Prototype 1")
        print(f"{self.shell.program_name}|" +
              f"{self.shell.module if '.py' not in self.shell.module else self.shell.module.replace('.py', '')}" +
              f"|{self.shell.id}> ", end="")

    def send_command(self, *args, **kwargs):
        self.get_shell()
        self.shell.shell_in = self.console_in.get()
        print(self.shell.shell_in)
        self.console_in.set("")
        self.shell.parseShellIn()
        print(f"{self.shell.program_name}|" +
              f"{self.shell.module if '.py' not in self.shell.module else self.shell.module.replace('.py', '')}" +
              f"|{self.shell.id}> ", end="")
        if self.luciferManager.log_file is not None:
            if self.luciferManager.log_amount == 1:
                self.luciferManager.log_command(self.shell.shell_in)

    def get_shell(self):
        self.shell = self.luciferManager.main_shell if self.luciferManager.current_shell_id == 0 else None
        if self.shell is None:
            for shell in self.luciferManager.alternative_shells:
                if shell.id == self.luciferManager.current_shell_id:
                    self.shell = shell
                    break
            else:
                raise NoShellError("Couldn't Find Shell With ID: " + str(self.luciferManager.current_shell_id))


class LuciferToolbar(tk.Frame):
    def __init__(self, luciferManager, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.luciferManager = luciferManager

        self.MenuBar = tk.Menu(self)
        self.parent.config(menu=self.MenuBar)
        self.fileMenu = tk.Menu(self.MenuBar)
        self.fileMenu.add_command(label="Exit", command=luciferManager.end)
        self.MenuBar.add_cascade(label="File", menu=self.fileMenu)


class LuciferGui(tk.Frame):
    def __init__(self, luciferManager, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.luciferManager = luciferManager

        self.parent.title("Lucifer")
        self.parent.geometry("1200x600")
        self.parent["bg"] = '#%02x%02x%02x' % (28, 28, 36)

        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_rowconfigure(1, weight=1)

        self.toolbar = LuciferToolbar(self.luciferManager, self.parent)
        self.console = LuciferConsole(self.luciferManager, self.parent)

        self.console.grid(column=0, row=0, sticky=tk.NSEW, rowspan=2, columnspan=1)
