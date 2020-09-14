import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from lucifer.Font import FontFind
from lucifer.GUI.Bars import LuciferStatus, LuciferToolbar
from lucifer.GUI.Console import LuciferConsole
from lucifer.GUI.Utils import Closer
from lucifer.GUI.Views import LuciferModulesView, LuciferVarView
from lucifer import Settings


class LuciferGui(tk.Frame, Closer, FontFind):
    def __init__(self, luciferManager, parent, *args, **kwargs):
        """The Full GUI Application Setup"""
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.luciferManager = luciferManager

        self.base_font_name = self.find_font(['TkDefaultFont', 'arial', 'helvetica'])
        self.base_font_size = 8
        self.font = (self.base_font_name, self.base_font_size)

        self.isRightPaneEnabled = tk.IntVar(self)
        self.isConsoleEnabled = tk.IntVar(self)
        self.isVarViewEnabled = tk.IntVar(self)
        self.isModuleViewEnabled = tk.IntVar(self)

        self.enable_Panes()
        self.setup_App()
        self.configure_grid()

        self.mainPane = ttk.PanedWindow(orient=tk.HORIZONTAL)
        self.statusFrame = LuciferStatus(self.luciferManager,
                                         self.parent, self)
        self.toolbar = LuciferToolbar(self.luciferManager, self.parent, self)
        self.console = LuciferConsole(self.luciferManager, self.parent, self)
        self.rightPane = ttk.PanedWindow(orient=tk.VERTICAL)
        self.moduleView = LuciferModulesView(self.luciferManager,
                                             self.parent, self)
        self.varView = LuciferVarView(self.luciferManager, self.parent, self)

        self.pack_all()

        self.load_settings()

    def pack_all(self):
        self.statusFrame.pack(fill=tk.X, expand=False, side=tk.BOTTOM)
        self.mainPane.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        self.mainPane.add(self.console)
        self.mainPane.add(self.rightPane)
        self.rightPane.add(self.moduleView)
        self.rightPane.add(self.varView)

    def setup_App(self):
        self.parent.title("Lucifer")
        self.parent.geometry("1200x600")
        image = Image.open("assets/lucifer.png")
        self.parent.iconphoto(True, ImageTk.PhotoImage(image))
        self.parent["bg"] = '#%02x%02x%02x' % (28, 28, 36)
        self.parent.protocol("WM_DELETE_WINDOW", self.on_close)

    def configure_grid(self):
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_rowconfigure(1, weight=1)

    def enable_Panes(self):
        self.isVarViewEnabled.set(1)
        self.isConsoleEnabled.set(1)
        self.isRightPaneEnabled.set(1)
        self.isModuleViewEnabled.set(1)

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

    def load_settings(self):
        if Settings.is_settings():
            font_settings = Settings.get_setting("gui.font")
            try:
                self.font = (font_settings["name"], font_settings["size"])
                self.update_font()
            except TypeError as e:
                print("\nProblem Loading 'settings.yml' file, Ignoring user settings.\n"
                      "To Fix this problem please delete or edit the 'settings.yml' file!")
        else:
            Settings.create_settings(self.font)

