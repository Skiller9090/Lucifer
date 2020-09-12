import sys
import threading
import tkinter as tk
from tkinter import ttk

from lucifer.Errors import checkErrors
from lucifer.GUI.Utils import ansi_escape
from lucifer.Utils import RetrieveShell


class TextRedirect(object):
    def __init__(self, widget, tag="stdout"):
        """The Object to Redirect output into the tkinter console box"""
        self.widget = widget
        self.tag = tag

    def write(self, string):
        self.widget.configure(state="normal")
        self.widget.insert("end", ansi_escape.sub("", string), (self.tag,))
        self.widget.configure(state="disabled")
        self.widget.see(tk.END)

    def flush(self):
        pass

    def fileno(self):
        if self.tag == "stdout":
            return 1
        else:
            return 2


class LuciferConsole(tk.Frame, RetrieveShell):
    def __init__(self, luciferManager, parent, GUI, *args, **kwargs):
        """The Console Box Setup"""
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.expand = True
        self.luciferManager = luciferManager
        self.LuciferGui = GUI

        self.console_in = tk.StringVar()
        self.ConsoleBox = tk.Text(self, font=self.LuciferGui.font)
        self.ConsoleBox.configure(state="disabled")
        self.ConsoleBox.tag_configure("stderr", foreground="#b22222")
        self.command_history = []
        self.command_index = None
        self.opened_order = [0]

        self.y_scrollbar = ttk.Scrollbar(self)

        self.ConsoleBox.config(yscrollcommand=self.y_scrollbar.set)
        self.y_scrollbar.config(command=self.ConsoleBox.yview)
        self.ConsoleInput = ttk.Entry(self, textvariable=self.console_in, font=self.LuciferGui.font)
        self.get_shell()

        self.ConsoleBox["bg"] = '#%02x%02x%02x' % (28, 28, 36)
        self.ConsoleBox["foreground"] = '#%02x%02x%02x' % (255, 255, 255)

        self.ConsoleInput.insert(0, 'Enter Command...')

        self.ConsoleInput.pack(side=tk.BOTTOM, anchor=tk.W, expand=False, fill="x")
        self.y_scrollbar.pack(side=tk.RIGHT, fill="y", anchor=tk.E, expand=False)
        self.ConsoleBox.pack(fill="both", side=tk.LEFT, anchor=tk.E, expand=True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.ConsoleInput.bind('<FocusIn>', self.on_entry_click)
        self.ConsoleInput.bind('<FocusOut>', self.on_focusout)
        self.ConsoleInput.bind("<Return>", self.send_command)
        self.ConsoleInput.bind("<Up>", self.history_up)
        self.ConsoleInput.bind("<Down>", self.history_down)

        self.luciferManager.stdout = TextRedirect(self.ConsoleBox, "stdout")
        # self.luciferManager.stderr = TextRedirect(self.ConsoleBox, "stderr")
        sys.stdout = self.luciferManager.stdout
        sys.stderr = self.luciferManager.stderr
        print("Lucifer Prototype 2")
        print(f"{self.shell.program_name}|" +
              f"{self.shell.module if '.py' not in self.shell.module else self.shell.module.replace('.py', '')}" +
              f"|{self.shell.id}> ", end="")

    def on_entry_click(self, *args, **kwargs):
        if self.ConsoleInput.get() == 'Enter Command...':
            self.ConsoleInput.delete(0, "end")
            self.ConsoleInput.insert(0, '')

    def on_focusout(self, *args, **kwargs):
        if self.ConsoleInput.get() == '':
            self.ConsoleInput.insert(0, 'Enter Command...')

    def send_command(self, *args, **kwargs):
        if self.luciferManager.gui_thread_free:
            self.luciferManager.gui_thread_free = False
            thread = threading.Thread(target=self.send_command_daemon)
            thread.setDaemon(True)
            thread.start()

    def clear(self):
        self.ConsoleBox.configure(state="normal")
        self.ConsoleBox.delete(1.0, tk.END)
        self.ConsoleBox.configure(state="disabled")

    def send_command_daemon(self):
        try:
            self.luciferManager.gui.statusFrame.status.set("Starting Command")
            self.get_shell()
            self.shell.shell_in = self.console_in.get()
            self.command_index = None
            self.command_history.append(self.shell.shell_in)
            self.luciferManager.gui.statusFrame.status.set(f"Running Command: {self.shell.shell_in}")
            print(self.shell.shell_in)
            self.console_in.set("")
            self.shell.parseShellIn()
            self.get_shell()
            print(f"{self.shell.program_name}|" +
                  f"{self.shell.module if '.py' not in self.shell.module else self.shell.module.replace('.py', '')}" +
                  f"|{self.shell.id}> ", end="")
            if self.luciferManager.log_file is not None:
                if self.luciferManager.log_amount == 1:
                    self.luciferManager.log_command(self.shell.shell_in)
        except Exception as e:
            checkErrors(e)
        self.luciferManager.gui.statusFrame.status.set("Idle")
        self.luciferManager.gui.varView.display_vars()
        self.luciferManager.gui_thread_free = True

    def history_up(self, *args, **kwargs):
        if self.command_index is None:
            if len(self.command_history) > 0:
                self.command_index = len(self.command_history) - 1
                self.ConsoleInput.delete(0, "end")
                self.ConsoleInput.insert(0, self.command_history[self.command_index])
        else:
            if self.command_index > 0:
                self.command_index -= 1
                self.ConsoleInput.delete(0, "end")
                self.ConsoleInput.insert(0, self.command_history[self.command_index])

    def history_down(self, *args, **kwargs):
        if self.command_index is not None:
            if len(self.command_history) - 1 > self.command_index:
                self.command_index += 1
                self.ConsoleInput.delete(0, "end")
                self.ConsoleInput.insert(0, self.command_history[self.command_index])
            else:
                self.command_index = None
                self.ConsoleInput.delete(0, "end")
