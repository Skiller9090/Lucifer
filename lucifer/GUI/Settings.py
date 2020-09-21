import tkinter as tk
from tkinter import ttk, font as tk_fonts

import lucifer.Settings


class Settings(tk.Tk):
    def __init__(self, luciferManager, GUI, *args, **kwargs):
        """The Settings Window Setup"""
        super().__init__(*args, **kwargs)
        self.luciferManager = luciferManager
        self.LuciferGUI = GUI

        self.title("Settings")

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
        """The Settings Font Menu Setup"""
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


class LuciferSettingsExit(ttk.Frame):
    def __init__(self, luciferManager, parent, GUI, **kwargs):
        """The Settings Exit And Apply Button Setup"""
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
        lucifer.Settings.update_setting("gui.font.name", self.LuciferGui.font[0])
        lucifer.Settings.update_setting("gui.font.size", self.LuciferGui.font[1])

    def exit(self):
        self.parent.destroy()

    def update_font(self):
        ttk.Style().configure("TButton", font=self.LuciferGui.font)


class LuciferSettingsViews(tk.LabelFrame):
    def __init__(self, luciferManager, parent, GUI, *args, **kwargs):
        """The Settings View Menu Setup"""
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
