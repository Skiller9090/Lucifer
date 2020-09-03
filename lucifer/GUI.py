import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font as tk_fonts
from .Errors import NoShellError, checkErrors
from .Indexing import index_modules
from .Font import FontFind
import sys
import re
import threading

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


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
            self.luciferManager.end()


class Settings(tk.Tk):
    def __init__(self, luciferManager, GUI, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.luciferManager = luciferManager
        self.LuciferGUI = GUI

        self.title("Settings")
        self.iconbitmap("assets/lucifer.ico")

        self.font_settings = LuciferSettingsFont(self.luciferManager, self, self.LuciferGUI)
        self.view_settings = LuciferSettingsViews(self.luciferManager, self, self.LuciferGUI)
        self.apply_exit = LuciferSettingsExit(self.luciferManager, self, self.LuciferGUI)

        self.font_settings.grid(column=0, row=0, sticky=tk.NSEW)
        self.view_settings.grid(column=1, row=0, sticky=tk.NSEW)
        self.apply_exit.grid(column=1, row=1)

        self.update_font()

    def update_font(self):
        self.font_settings.update_font()
        self.view_settings.update_font()
        self.apply_exit.update_font()
        ttk.Style().configure("TLabelframe.Label", font=self.LuciferGUI.font)


class LuciferSettingsFont(tk.LabelFrame):
    def __init__(self, luciferManager, parent, GUI, *args, **kwargs):
        super().__init__(parent, text="Fonts", *args, **kwargs)
        self.parent = parent
        self.luciferManager = luciferManager
        self.LuciferGui = GUI

        self.all_fonts = list(tk_fonts.families())
        self.all_fonts.sort()
        self.current_font = None

        self.font_box = ttk.Combobox(self, values=self.all_fonts)
        self.font_box.current(self.all_fonts.index(self.LuciferGui.font[0]))
        self.size_box = ttk.Combobox(self, values=list(range(1, 41)))
        self.size_box.current(int(self.LuciferGui.font[1]) - 1)

        self.font_preview = tk.Label(self, text="Lucifer is a great hacking tool!\n==+-*/!<>?|@~{}")
        self.font_preview["bg"] = '#%02x%02x%02x' % (28, 28, 36)
        self.font_preview["foreground"] = '#%02x%02x%02x' % (255, 255, 255)

        self.font_box.bind("<<ComboboxSelected>>", self.font_preview_update)
        self.size_box.bind("<<ComboboxSelected>>", self.font_preview_update)

        self.font_box.grid(row=0, column=0, sticky=tk.EW)
        self.size_box.grid(row=0, column=1, sticky=tk.EW)
        self.font_preview.grid(row=1, column=0, columnspan=2)

        self.font_preview_update()

    def font_preview_update(self, *args, **kwargs):
        font = self.font_box.get()
        size = int(self.size_box.get())
        self.font_preview.config(font=(font, size))
        self.current_font = (font, size)

    def update_font(self):
        ttk.Style().configure("TCombobox", font=self.LuciferGui.font)


class LuciferSettingsViews(tk.LabelFrame):
    def __init__(self, luciferManager, parent, GUI, *args, **kwargs):
        super().__init__(parent, text="Views", *args, **kwargs)
        self.parent = parent
        self.luciferManager = luciferManager
        self.LuciferGui = GUI

        self.prev_console = tk.IntVar(self, value=self.LuciferGui.isConsoleEnabled.get())
        self.prev_var_view = tk.IntVar(self, value=self.LuciferGui.isVarViewEnabled.get())
        self.prev_module_view = tk.IntVar(self, value=self.LuciferGui.isModuleViewEnabled.get())
        self.prev_right_pane = tk.IntVar(self, value=self.LuciferGui.isRightPaneEnabled.get())

        self.ConsoleCheck = ttk.Checkbutton(self, text="Console", variable=self.prev_console)
        self.VarViewCheck = ttk.Checkbutton(self, text="Variable View", variable=self.prev_var_view)
        self.ModuleViewCheck = ttk.Checkbutton(self, text="Module View", variable=self.prev_module_view)
        self.RightPaneCheck = ttk.Checkbutton(self, text="Right Pane", variable=self.prev_right_pane)

        self.ConsoleCheck.pack(fill=tk.X)
        self.VarViewCheck.pack(fill=tk.X)
        self.ModuleViewCheck.pack(fill=tk.X)
        self.RightPaneCheck.pack(fill=tk.X)

    def update_font(self):
        ttk.Style().configure("TCheckbutton", font=self.LuciferGui.font)

    def apply_view_settings(self):
        if self.prev_console.get() != self.LuciferGui.isConsoleEnabled.get():
            self.LuciferGui.toggle_console()
        if self.prev_var_view.get() != self.LuciferGui.isVarViewEnabled.get():
            self.LuciferGui.toggle_var_view()
        if self.prev_module_view.get() != self.LuciferGui.isModuleViewEnabled.get():
            self.LuciferGui.toggle_module_view()
        if self.prev_right_pane.get() != self.LuciferGui.isRightPaneEnabled.get():
            self.LuciferGui.toggle_right_pane()


class LuciferSettingsExit(ttk.Frame):
    def __init__(self, luciferManager, parent, GUI, **kwargs):
        super().__init__(parent, **kwargs)

        self.parent = parent
        self.luciferManager = luciferManager
        self.LuciferGui = GUI

        self.ApplyButton = ttk.Button(self, text="Apply", command=self.apply_settings)
        self.ExitButton = ttk.Button(self, text="Exit", command=self.exit)

        self.ApplyButton.pack(side=tk.LEFT)
        self.ExitButton.pack(side=tk.RIGHT)

    def apply_settings(self):
        self.parent.view_settings.apply_view_settings()
        self.LuciferGui.font = self.parent.font_settings.current_font
        self.LuciferGui.update_font()

    def exit(self):
        self.parent.destroy()

    def update_font(self):
        ttk.Style().configure("TButton", font=self.LuciferGui.font)


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
    def __init__(self, luciferManager, parent, GUI, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.treeDirectory = []
        self.parent = parent
        self.expand = True
        self.luciferManager = luciferManager
        self.LuciferGui = GUI

        style = ttk.Style()
        style.configure("Treeview",
                        background="#E1E1E1",
                        foreground="#000000",
                        rowheight=25,
                        fieldbackground="#E1E1E1",
                        font=self.LuciferGui.font)
        style.configure("Treeview.Heading", font=self.LuciferGui.font)
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
    def __init__(self, luciferManager, parent, GUI, *args, **kwargs):
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
            self.ConsoleBox.see(tk.END)
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


class LuciferStatus(tk.Frame):
    def __init__(self, luciferManager, parent, GUI, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.luciferManager = luciferManager
        self.LuciferGui = GUI

        self.status = tk.StringVar()
        self.status.set("Idle")

        style = ttk.Style()
        style.configure("Label", foreground="white")

        self.statusWidget = ttk.Label(self, textvariable=self.status,
                                      relief=tk.SUNKEN, anchor=tk.E,
                                      font=self.LuciferGui.font)
        self.statusWidget.config(style="Label")
        self.statusWidget.pack(fill=tk.X, expand=False)


class LuciferToolbar(tk.Frame, Closer):
    def __init__(self, luciferManager, parent, GUI, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.luciferManager = luciferManager
        self.LuciferGui = GUI

        self.isSettingsOpen = False
        self.settings_window = None

        self.MenuBar = tk.Menu(self)
        self.parent.config(menu=self.MenuBar)

        self.fileMenu = tk.Menu(self.MenuBar, tearoff=0)
        self.viewMenu = tk.Menu(self.MenuBar, tearoff=0)

        self.fileMenu.add_command(label="Settings", command=self.open_settings,
                                  font=self.LuciferGui.font)
        self.fileMenu.add_command(label="Exit", command=self.on_close,
                                  font=self.LuciferGui.font)
        self.viewMenu.add_command(label="Toggle Console", command=self.LuciferGui.toggle_console,
                                  font=self.LuciferGui.font)
        self.viewMenu.add_command(label="Toggle Module View", command=self.LuciferGui.toggle_module_view,
                                  font=self.LuciferGui.font)
        self.viewMenu.add_command(label="Toggle Variable View", command=self.LuciferGui.toggle_var_view,
                                  font=self.LuciferGui.font)
        self.viewMenu.add_command(label="Toggle Right Pane", command=self.LuciferGui.toggle_right_pane,
                                  font=self.LuciferGui.font)

        self.MenuBar.add_cascade(label="File", menu=self.fileMenu, font=self.LuciferGui.font)
        self.MenuBar.add_cascade(label="View", menu=self.viewMenu, font=self.LuciferGui.font)

    def open_settings(self):
        self.isSettingsOpen = True
        self.settings_window = Settings(self.luciferManager, self.LuciferGui)
        self.settings_window.mainloop()
        self.settings_window = None
        self.isSettingsOpen = False


class LuciferVarView(tk.Frame, RetrieveShell):
    def __init__(self, luciferManager, parent, GUI, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.luciferManager = luciferManager
        self.LuciferGui = GUI
        self.get_shell()
        self.varViewVars = {}
        self.varViewObjects = []
        self.treeDirectory = []
        self.parent = parent
        self.expand = True

        self.style = ttk.Style()
        self.style.configure("Treeview",
                             background="#E1E1E1",
                             foreground="#000000",
                             rowheight=25,
                             fieldbackground="#E1E1E1",
                             font=self.LuciferGui.font)
        self.style.configure("Treeview.Heading", font=self.LuciferGui.font)
        self.style.map('Treeview', background=[('selected', '#BFBFBF')])

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


class LuciferGui(tk.Frame, Closer, FontFind):
    def __init__(self, luciferManager, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.luciferManager = luciferManager

        self.base_font_name = self.find_font(['TkDefaultFont', 'arial', 'helvetica'])
        self.base_font_size = 8
        self.font = (self.base_font_name, self.base_font_size)

        self.isRightPaneEnabled = tk.IntVar(self)
        self.isRightPaneEnabled.set(1)
        self.isConsoleEnabled = tk.IntVar(self)
        self.isConsoleEnabled.set(1)
        self.isVarViewEnabled = tk.IntVar(self)
        self.isVarViewEnabled.set(1)
        self.isModuleViewEnabled = tk.IntVar(self)
        self.isModuleViewEnabled.set(1)

        self.parent.title("Lucifer")
        self.parent.geometry("1200x600")
        self.parent.iconbitmap("assets/lucifer.ico")
        self.parent["bg"] = '#%02x%02x%02x' % (28, 28, 36)
        self.parent.protocol("WM_DELETE_WINDOW", self.on_close)

        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_rowconfigure(1, weight=1)

        self.mainPane = ttk.PanedWindow(orient=tk.HORIZONTAL)
        self.statusFrame = LuciferStatus(self.luciferManager, self.parent, self)
        self.statusFrame.pack(fill=tk.X, expand=False, side=tk.BOTTOM)
        self.mainPane.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        self.toolbar = LuciferToolbar(self.luciferManager, self.parent, self)
        self.console = LuciferConsole(self.luciferManager, self.parent, self)
        self.mainPane.add(self.console)

        self.rightPane = ttk.PanedWindow(orient=tk.VERTICAL)
        self.mainPane.add(self.rightPane)

        self.moduleView = LuciferModulesView(self.luciferManager, self.parent, self)
        self.varView = LuciferVarView(self.luciferManager, self.parent, self)
        self.rightPane.add(self.moduleView)
        self.rightPane.add(self.varView)

    def toggle_right_pane(self):
        if self.isRightPaneEnabled.get():
            self.mainPane.remove(self.rightPane)
        else:
            self.mainPane.add(self.rightPane)
        self.isRightPaneEnabled.set(int(not self.isRightPaneEnabled.get()))

    def toggle_console(self):
        if self.isConsoleEnabled.get():
            self.mainPane.remove(self.console)
        else:
            if len(self.mainPane.panes()) > 0:
                self.mainPane.insert(0, self.console)
            else:
                self.mainPane.add(self.console)
        self.isConsoleEnabled.set(int(not self.isConsoleEnabled.get()))

    def toggle_var_view(self):
        if self.isVarViewEnabled.get():
            self.rightPane.remove(self.varView)
        else:
            self.rightPane.add(self.varView)
        self.isVarViewEnabled.set(int(not self.isVarViewEnabled.get()))

    def toggle_module_view(self):
        if not self.isModuleViewEnabled.get():
            if len(self.rightPane.panes()) > 0:
                self.rightPane.insert(0, self.moduleView)
            else:
                self.rightPane.add(self.moduleView)
        else:
            self.rightPane.remove(self.moduleView)
        self.isModuleViewEnabled.set(int(not self.isModuleViewEnabled.get()))

    def update_font(self):
        self.console.ConsoleBox.config(font=self.font)
        self.console.ConsoleInput.config(font=self.font)
        self.statusFrame.statusWidget.config(font=self.font)
        self.varView.style.configure("Treeview",
                                     font=self.font)
        self.varView.style.configure("Treeview.Heading",
                                     font=self.font)
        if self.toolbar.isSettingsOpen:
            self.toolbar.settings_window.update_font()
