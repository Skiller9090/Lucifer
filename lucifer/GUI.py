import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from .Errors import NoShellError, checkErrors
from .Indexing import index_modules
import sys
import re
import threading

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

    def flush(self):
        pass

    def fileno(self):
        if self.tag == "stdout":
            return 1
        else:
            return 2


class Closer:
    def on_close(self):
        if messagebox.askokcancel("Quit Lucifer", "Are you sure you want to quit Lucifer?"):
            self.parent.destroy()
            self.luciferManager.end()


class RetrieveShell:
    def get_shell(self):
        self.shell = self.luciferManager.main_shell if self.luciferManager.current_shell_id == 0 else None
        if self.shell is None:
            for shell in self.luciferManager.alternative_shells:
                if shell.id == self.luciferManager.current_shell_id:
                    self.shell = shell
                    break
            else:
                raise NoShellError("Couldn't Find Shell With ID: " + str(self.luciferManager.current_shell_id))


class LuciferModulesView(tk.Frame):
    def __init__(self, luciferManager, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.treeDirectory = []
        self.parent = parent
        self.expand = True
        self.luciferManager = luciferManager

        style = ttk.Style()
        style.configure("Treeview",
                        background="#E1E1E1",
                        foreground="#000000",
                        rowheight=25,
                        fieldbackground="#E1E1E1")
        style.map('Treeview', background=[('selected', '#BFBFBF')])

        self.moduleView = ttk.Treeview(self)

        self.moduleView["columns"] = "path"
        self.moduleView.heading("#0", text="Module", anchor=tk.W)
        self.moduleView.heading("#1", text="Path", anchor=tk.W)
        self.moduleView.bind("<Double-1>", self.run_Module)
        self.add_Modules()

        self.moduleView.pack(fill="both", side=tk.TOP, expand=True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def run_Module(self, event, *args, **kwargs):
        selected = self.moduleView.selection()
        if "M" == selected[0][0]:
            path = self.moduleView.item(selected[0])["values"][0]
            self.luciferManager.gui.console.console_in.set(f'use {path}')

    def add_Modules(self):
        _, modules, directories = index_modules()
        directories.sort()

        class Folder:
            def __init__(self, tree_obj, obj_path):
                self.obj = tree_obj
                self.path = obj_path

        for index, directory in enumerate(directories):
            layers = directory.split("/")
            name = layers[-1]
            base_obj = None
            if len(layers) > 1:
                for td in self.treeDirectory:
                    if td.path == directory.replace("/" + name, ""):
                        base_obj = td
                        break
                obj = self.moduleView.insert(base_obj.obj, tk.END, index + 1,
                                             text=name.title(), values=(directory,))
            else:
                obj = self.moduleView.insert("", tk.END, index + 1,
                                             text=name.title(), values=(directory,))
            self.treeDirectory.append(Folder(obj, directory))

        for i, k in enumerate(modules.keys()):
            module = modules[k]
            path = module["path"].replace("modules/", "")
            test_path = "/".join(path.split("/")[0:-1])
            name = module["name"]
            folder_obj = None

            for folder in self.treeDirectory:
                if folder.path == test_path:
                    folder_obj = folder
                    break
            self.moduleView.insert(folder_obj.obj, tk.END, "M" + str(i + 1), text=name,
                                   values=(path,))


class LuciferConsole(tk.Frame, RetrieveShell):
    def __init__(self, luciferManager, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.expand = True
        self.luciferManager = luciferManager
        self.console_in = tk.StringVar()
        self.ConsoleBox = tk.Text(self, font=font)
        self.ConsoleBox.configure(state="disabled")
        self.ConsoleBox.tag_configure("stderr", foreground="#b22222")

        self.y_scrollbar = ttk.Scrollbar(self)

        self.ConsoleBox.config(yscrollcommand=self.y_scrollbar.set)
        self.y_scrollbar.config(command=self.ConsoleBox.yview)
        self.ConsoleInput = ttk.Entry(self, textvariable=self.console_in)
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

        self.luciferManager.stdout = TextRedirect(self.ConsoleBox, "stdout")
        self.luciferManager.stderr = TextRedirect(self.ConsoleBox, "stderr")
        sys.stdout = self.luciferManager.stdout
        sys.stderr = self.luciferManager.stderr

        print("lucifer Prototype 1")
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
            self.ConsoleBox.see(tk.END)
        except Exception as e:
            checkErrors(e)
        self.luciferManager.gui.varView.display_vars()
        self.luciferManager.gui_thread_free = True


class LuciferToolbar(tk.Frame, Closer):
    def __init__(self, luciferManager, parent, GUI, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.luciferManager = luciferManager
        self.LuciferGui = GUI

        self.MenuBar = tk.Menu(self)
        self.parent.config(menu=self.MenuBar)

        self.fileMenu = tk.Menu(self.MenuBar)
        self.viewMenu = tk.Menu(self.MenuBar)

        self.fileMenu.add_command(label="Exit", command=self.on_close)
        self.viewMenu.add_command(label="Toggle Console", command=self.LuciferGui.toggle_console)
        self.viewMenu.add_command(label="Toggle Module View", command=self.LuciferGui.toggle_module_view)
        self.viewMenu.add_command(label="Toggle Variable View", command=self.LuciferGui.toggle_var_view)
        self.viewMenu.add_command(label="Toggle Right Pane", command=self.LuciferGui.toggle_right_pane)

        self.MenuBar.add_cascade(label="File", menu=self.fileMenu)
        self.MenuBar.add_cascade(label="View", menu=self.viewMenu)


class LuciferVarView(tk.Frame, RetrieveShell):
    def __init__(self, luciferManager, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.luciferManager = luciferManager
        self.get_shell()
        self.varViewVars = {}
        self.varViewObjects = []
        self.treeDirectory = []
        self.parent = parent
        self.expand = True

        style = ttk.Style()
        style.configure("Treeview",
                        background="#E1E1E1",
                        foreground="#000000",
                        rowheight=25,
                        fieldbackground="#E1E1E1")
        style.map('Treeview', background=[('selected', '#BFBFBF')])

        self.varView = ttk.Treeview(self)

        self.varView["columns"] = "path"
        self.varView.heading("#0", text="Variable", anchor=tk.W)
        self.varView.heading("#1", text="Value", anchor=tk.W)

        self.varView.pack(fill="both", side=tk.TOP, expand=True)
        self.display_vars()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def display_vars(self):
        self.get_shell()
        if self.varViewVars != self.shell.vars:
            self.clear_varView()
            self.varViewVars = self.shell.vars.copy()
            for k, v in zip(self.varViewVars.keys(), self.varViewVars.values()):
                obj = self.varView.insert("", tk.END, k, text=k, values=(v,))
                self.varViewObjects.append(obj)

    def clear_varView(self):
        self.varView.delete(*self.varView.get_children())


class LuciferGui(tk.Frame, Closer):
    def __init__(self, luciferManager, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.luciferManager = luciferManager

        self.isRightPaneEnabled = True
        self.isConsoleEnabled = True
        self.isVarViewEnabled = True
        self.isModuleViewEnabled = True

        self.parent.title("Lucifer")
        self.parent.geometry("1200x600")
        self.parent["bg"] = '#%02x%02x%02x' % (28, 28, 36)
        self.parent.protocol("WM_DELETE_WINDOW", self.on_close)

        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_rowconfigure(1, weight=1)

        self.mainPane = ttk.PanedWindow(orient=tk.HORIZONTAL)
        self.mainPane.pack(fill=tk.BOTH, expand=True)

        self.toolbar = LuciferToolbar(self.luciferManager, self.parent, self)
        self.console = LuciferConsole(self.luciferManager, self.parent)
        self.mainPane.add(self.console)

        self.rightPane = ttk.PanedWindow(orient=tk.VERTICAL)
        self.mainPane.add(self.rightPane)

        self.moduleView = LuciferModulesView(self.luciferManager, self.parent)
        self.varView = LuciferVarView(self.luciferManager, self.parent)
        self.rightPane.add(self.moduleView)
        self.rightPane.add(self.varView)

    def toggle_right_pane(self):
        if self.isRightPaneEnabled:
            self.mainPane.remove(self.rightPane)
        else:
            self.mainPane.add(self.rightPane)
        self.isRightPaneEnabled = not self.isRightPaneEnabled

    def toggle_console(self):
        if self.isConsoleEnabled:
            self.mainPane.remove(self.console)
        else:
            if len(self.mainPane.panes()) > 0:
                self.mainPane.insert(0, self.console)
            else:
                self.mainPane.add(self.console)
        self.isConsoleEnabled = not self.isConsoleEnabled

    def toggle_var_view(self):
        if self.isVarViewEnabled:
            self.rightPane.remove(self.varView)
        else:
            self.rightPane.add(self.varView)
        self.isVarViewEnabled = not self.isVarViewEnabled

    def toggle_module_view(self):
        if not self.isModuleViewEnabled:
            if len(self.rightPane.panes()) > 0:
                self.rightPane.insert(0, self.moduleView)
            else:
                self.rightPane.add(self.moduleView)
        else:
            self.rightPane.remove(self.moduleView)
        self.isModuleViewEnabled = not self.isModuleViewEnabled
