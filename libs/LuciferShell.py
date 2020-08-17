from .utils import check_int
from .LuciferErrors import IncompatibleSystemError
import re
import os
import importlib


class Shell:
    def __init__(self, ID, lucifer_manager):
        self.id = ID
        self.is_main = True if self.id == 0 else False
        self.luciferManager = lucifer_manager
        self.gui = False
        self.module = ""
        self.module_obj = None
        self.loaded_modules = {}
        self.program_name = "Lucifer"
        self.shell_in = ""
        self.vars = {}
        self.help_menu = """help        - Displays This Menu
show        - Shows options or modules based on input, EX: show <options/modules>
use         - Move into a module, EX: use <module>
set         - Sets a variable or option, EX: set <var> <data>
run         - Runs the current module, can also use exploit to do the same
reset       - Resets Everything
spawn_shell - Spawns a alternative shell
open_shell  - Open a shell by id EX: open_shell <id>
show_shells - Show all shell ids and attached name
set_name    - Sets current shells name EX: set_name <name>
set_name_id - Set a shells name by id EX: set_name_id <id> <name>
close       - Closes current shell
clear       - Clear screen
id          - Displays current shell's id
exit        - Exits the program, can also use quit to do the same
name        - Shows name of current shell"""
        self.name = "Shell " if not self.is_main else "Main Shell"
        self.alias = {
            "help": self.help,
            "set": self.command_set,
            "show": self.show,
            "quit": self.luciferManager.end,
            "exit": self.luciferManager.end,
            "id": self.print_id,
            "spawn_shell": self.spawn_shell,
            "open_shell": self.open_shell,
            "close": self.background_shell,
            "show_shells": self.show_shells,
            "name": self.print_name,
            "set_name": self.set_name,
            "set_name_id": self.set_name_id,
            "clear": self.clear_shell,
            "use": self.use,
            "run": self.run_module,
            "exploit": self.run_module

        }
        self.luciferManager.shell_recur += 1

    def getIn(self):
        self.shell_in = input(f"{self.program_name}|" +
                              f"{self.module if '.py' not in self.module else self.module.replace('.py', '')}" +
                              f"|{self.id}> ")

    def print_id(self, com_args: list):
        print(f"Shell ID: {self.id}")

    def print_name(self, com_args: list):
        print(f"Shell Name: {self.name}")

    def parseShellIn(self):
        com_args = self.shell_in.split(" ")
        while "" in com_args:
            com_args.remove("")
        if len(com_args) == 0:
            return
        com = com_args[0].lower().rstrip()
        if com in self.alias.keys():
            return_value = self.alias[com](com_args)
            return return_value
        return

    def help(self, com_args):
        print(self.help_menu)

    def spawn(self):
        while True:
            self.getIn()
            signal = self.parseShellIn()
            if signal == 7:
                break

    def command_set(self, com_args: list):
        com_args.pop(0)
        com_args = " ".join(com_args)
        vsl = com_args.split(" ")
        var = vsl.pop(0).rstrip()
        if var != "":
            var_string = " ".join(vsl)
            self.vars[var] = var_string
            print(f"{var} => {var_string}")
        else:
            print("Please specify a variable to set")

    def spawn_shell(self, com_args: list):
        self.luciferManager.alternative_shells.append(Shell(self.luciferManager.next_shell_id, self.luciferManager))
        self.luciferManager.next_shell_id += 1
        self.luciferManager.alternative_shells[-1].name += str(self.luciferManager.next_shell_id - 1)
        print(f"Opened New Shell With ID: {self.luciferManager.next_shell_id - 1}")

    def show(self, com_args: list):
        if len(com_args) > 1:
            if com_args[1].lower().strip() == "options" or com_args[1].lower().strip() == "vars":
                self.show_options()
                return
            else:
                print("Please enter a valid argument: options or modules")
        else:
            print("Please specify options or modules to show!")
        return

    def show_options(self):
        print(self.vars)
        return

    def use_module(self, mod_path: list):
        if self.module_obj is not None:
            self.loaded_modules[self.module] = self.module_obj
        print(mod_path)
        ori_path = mod_path.copy()
        file = mod_path.pop(-1)
        path = "modules"
        for directory in mod_path:
            path += "/" + directory
            if os.path.exists(path):
                if os.path.isdir(path):
                    continue
                else:
                    print(f"Module: {'/'.join(ori_path)} Does Not Exist!")
                    return
            else:
                print(f"Module: {'/'.join(ori_path)} Does Not Exist!")
                return
        else:
            if os.path.isfile(path + "/" + file):
                self.module = path + "/" + file
                print(f"Using module: {self.module}")
            elif os.path.isfile(path + "/" + file + ".py"):
                self.module = path + "/" + file + ".py"
                print(f"Using module: {self.module}")
            else:
                print(f"Module: {'/'.join(ori_path)} Does Not Exist!")
                return

        if self.module in self.loaded_modules.keys():
            self.module_obj = self.loaded_modules.get(self.module)
        else:
            to_import = (self.module.replace("/", ".")
                         if ".py" not in self.module else
                         self.module.replace(".py", "").replace("/", ".")).split(".")
            pkg = to_import.pop(-1)
            to_import = ".".join(to_import)
            imported_module = importlib.import_module(to_import + "." + pkg)
            self.module_obj = imported_module.Module(self.luciferManager, ShellRun=True)
            self.loaded_modules[self.module] = self.module_obj
        return

    def run_module(self, com_args: list):
        try:
            if self.module_obj is not None:
                self.module_obj.run()
                return
            else:
                print("Please Select A Module First!")
                return
        except IncompatibleSystemError as e:
            print(e)

    def open_shell(self, com_args: list):
        if len(com_args) > 1:
            openid = com_args[1].rstrip()
            if check_int(openid):
                openid = int(openid)
                if openid == 0:
                    self.luciferManager.main_shell.spawn()
                    return
                else:
                    found = False
                    for index, shell in enumerate(self.luciferManager.alternative_shells):
                        if shell.id == openid:
                            self.luciferManager.alternative_shells[index].spawn()
                            return
                    else:
                        print("Please specify a valid ID")
                        return
            else:
                print("Please specify a valid ID")
                return
        else:
            print("Please specify a valid ID")
            return

    def show_shells(self, com_args: list):
        print(f"{self.luciferManager.main_shell.name} => {self.luciferManager.main_shell.id}")
        for shell in self.luciferManager.alternative_shells:
            print(f"{shell.name} => {shell.id}")
        return

    def set_name(self, com_args: list):
        print(com_args)
        if len(com_args) > 1:
            com_args.pop(0)
            self.name = " ".join(com_args)
        return

    def set_name_id(self, com_args: list):
        if len(com_args) > 1:
            ID = com_args[1].rstrip()
            if check_int(ID):
                for i in range(2):
                    com_args.pop(0)
                name = " ".join(com_args)
                ID = int(ID)
                if ID == 0:
                    self.luciferManager.main_shell.name = name
                    print(f"{ID} => {name}")
                else:
                    for index, shell in enumerate(self.luciferManager.alternative_shells):
                        if shell.id == ID:
                            self.luciferManager.alternative_shells[index].name = name
                            print(f"{ID} => {name}")
                            break
                    else:
                        print("Not a valid ID")
                return
            else:
                print("Not a valid ID")
                return
        else:
            print("Please add a valid ID")
            return

    def clear_shell(self, com_args: list):
        print(self.luciferManager.colorama.ansi.clear_screen())

    def use(self, com_args: list):
        if len(com_args) > 1:
            if len(com_args) == 2:
                module_path = re.split(r"\\|/|,", com_args[1].rstrip())
            else:
                com_args.pop(0)
                module_path = re.split(r"\\| |/|,", " ".join(com_args).rstrip())
            if module_path:
                while "" in module_path:
                    module_path.remove("")
                self.use_module(module_path)
        else:
            print("Please add valid module path")
        return

    def background_shell(self, com_args: list):
        if self.luciferManager.shell_recur == 1:
            self.luciferManager.end()
        else:
            self.luciferManager.shell_recur -= 1
        return 7
