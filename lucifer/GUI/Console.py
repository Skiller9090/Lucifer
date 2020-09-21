import sys
import threading
import tkinter as tk
from tkinter import ttk

from lucifer.Errors import checkErrors
from lucifer.Utils import RetrieveShell


class TextRedirect(object):
    def __init__(self, widget, tag="stdout"):
        """The Object to Redirect output into the tkinter console box."""
        self.all_tags = {
            "30": "black",
            "31": "red",
            "32": "green",
            "33": "yellow",
            "34": "blue",
            "35": "cyan",
            "36": "magenta",
            "37": "white",
            "0": "stdout"
        }
        self.widget = widget
        self.esc_seq = u"\u001b["
        self.tag = tag

    def write(self, string):
        self.widget.configure(state="normal")
        if self.esc_seq in string:
            tag_string = self.process_text(string)
            for insert_tuple in tag_string:
                tags = self.tag_map(insert_tuple[0])
                self.widget.insert("end", (str(insert_tuple[1])), tags)
        else:
            self.widget.insert("end", string, (self.tag,))
        self.widget.configure(state="disabled")
        self.widget.see(tk.END)

    def process_text(self, string):
        to_process = string.split(self.esc_seq)
        tag_string = []
        while "" in to_process:
            to_process.remove("")
        for text in to_process:
            if "m" in text:
                m_ind = text.index("m")
                if len(text) - 1 != m_ind:
                    tag_string.append(([text[0:m_ind]], text[(m_ind + 1):]))
            else:
                tag_string.append(("stdout", text))
        return tag_string

    def flush(self):
        pass

    def fileno(self):
        if self.tag == "stdout":
            return 1
        return 2

    def tag_map(self, tag_ids):
        tags = []
        for tid in tag_ids:
            mapped_tag = self.all_tags.get(tid)
            if mapped_tag is None:
                tags.append("stdout")
            else:
                tags.append(mapped_tag)
        return tuple(tags)


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
        self.add_colour_tags()
        self.command_history = []
        self.command_index = None
        self.opened_order = [0]

        self.y_scrollbar = ttk.Scrollbar(self)
        self.ConsoleInput = ttk.Entry(self, textvariable=self.console_in, font=self.LuciferGui.font)

        self.setup_console_widget()

        self.luciferManager.stdout = TextRedirect(self.ConsoleBox, "stdout")
        # self.luciferManager.stderr = TextRedirect(self.ConsoleBox, "stderr")
        sys.stdout = self.luciferManager.stdout
        sys.stderr = self.luciferManager.stderr
        print(self.luciferManager.termcolor.colored(self.luciferManager.version, "red", attrs=["bold", "underline"]))
        print(f"{self.shell.program_name}|" +
              f"{self.shell.module if '.py' not in self.shell.module else self.shell.module.replace('.py', '')}" +
              f"|{self.shell.id}> ", end="")

    def add_colour_tags(self):
        self.ConsoleBox.tag_configure("stderr", foreground="#b22222")
        self.ConsoleBox.tag_configure("stdout", foreground="#FFFFFF")
        self.ConsoleBox.tag_configure("black", foreground="#555555")
        self.ConsoleBox.tag_configure("red", foreground="#FF5555")
        self.ConsoleBox.tag_configure("green", foreground="#55FF55")
        self.ConsoleBox.tag_configure("yellow", foreground="#FFFF55")
        self.ConsoleBox.tag_configure("blue", foreground="#0D98BA")
        self.ConsoleBox.tag_configure("cyan", foreground="#FF55FF")
        self.ConsoleBox.tag_configure("magenta", foreground="#55FFFF")
        self.ConsoleBox.tag_configure("white", foreground="#FFFFFF")

    def setup_console_widget(self):
        self.link_scrollbar()
        self.get_shell()
        self.ConsoleBox["bg"] = '#%02x%02x%02x' % (28, 28, 36)
        self.ConsoleBox["foreground"] = '#%02x%02x%02x' % (255, 255, 255)
        self.ConsoleInput.insert(0, 'Enter Command...')
        self.pack_all()
        self.setup_grid()
        self.bind_shortcuts()

    def link_scrollbar(self):
        self.ConsoleBox.config(yscrollcommand=self.y_scrollbar.set)
        self.y_scrollbar.config(command=self.ConsoleBox.yview)

    def pack_all(self):
        self.ConsoleInput.pack(side=tk.BOTTOM, anchor=tk.W, expand=False, fill="x")
        self.y_scrollbar.pack(side=tk.RIGHT, fill="y", anchor=tk.E, expand=False)
        self.ConsoleBox.pack(fill="both", side=tk.LEFT, anchor=tk.E, expand=True)

    def bind_shortcuts(self):
        self.ConsoleInput.bind('<FocusIn>', self.on_entry_click)
        self.ConsoleInput.bind('<FocusOut>', self.on_focusout)
        self.ConsoleInput.bind("<Return>", self.send_command)
        self.ConsoleInput.bind("<Up>", self.history_up)
        self.ConsoleInput.bind("<Down>", self.history_down)

    def setup_grid(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

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
