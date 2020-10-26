import tkinter as tk
from tkinter import ttk

from lucifer.Indexing import index_modules
from lucifer.Utils import RetrieveShell


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
        if selected:
            if "M" == selected[0][0]:
                path = self.moduleView.item(selected[0])["values"][0]
                self.luciferManager.gui.console.console_in.set(f'use {path}')

    def add_Modules(self):
        self.moduleView.delete(*self.moduleView.get_children())
        _, modules, directories = self.luciferManager.module_cache
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
