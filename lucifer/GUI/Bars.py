import tkinter as tk
from tkinter import ttk

from lucifer.GUI.Settings import Settings
from lucifer.GUI.Utils import Closer


class LuciferStatus(tk.Frame):
    def __init__(self, luciferManager, parent, GUI, *args, **kwargs):
        """The Status Bar Setup"""
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.luciferManager = luciferManager
        self.LuciferGui = GUI

        self.status = tk.StringVar()
        self.status.set("Idle")

        style = ttk.Style()
        style.configure("Label", foreground="white", background='#%02x%02x%02x' % (56, 56, 72))

        self.statusWidget = ttk.Label(self, textvariable=self.status,
                                      relief=tk.SUNKEN, anchor=tk.E,
                                      font=self.LuciferGui.font)
        self.statusWidget.config(style="Label")
        self.statusWidget.pack(fill=tk.X, expand=False)


class LuciferToolbar(tk.Frame, Closer):
    def __init__(self, luciferManager, parent, GUI, *args, **kwargs):
        """The Tool Bar Setup"""
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
