from lucifer.utils import check_int
from .Errors import checkErrors
from .Help import help_menu
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
        self.program_name = "lucifer"
        self.shell_in = ""
        self.vars = {}
        self.auto_vars = lucifer_manager.auto_vars
        self.help_menu = help_menu
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
            "exploit": self.run_module,
            "set_vars": self.set_vars,
            "options": self.show_options,
            "description": self.describe_module,
            "describe": self.describe_module,
            "auto_vars": self.print_auto_vars,
            "change_auto_vars": self.change_auto_set_vars,
            "auto_var": self.print_auto_vars,
            "change_auto_var": self.change_auto_set_vars
        }
        self.luciferManager.shell_recur += 1

    def getIn(self):
        self.shell_in = input(f"{self.program_name}|" +
                              f"{self.module if '.py' not in self.module else self.module.replace('.py', '')}" +
                              f"|{self.id}> ")
        if self.luciferManager.log_file is not None:
            if self.luciferManager.log_amount == 1:
                self.luciferManager.log_command(self.shell_in)

    def print_id(self, *args, **kwargs):
        print(f"Shell ID: {self.id}")

    def print_name(self, *args, **kwargs):
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

    def help(self, *args, **kwargs):
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

    def spawn_shell(self, *args, **kwargs):
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
                print("Please enter a valid argument: options/vars or modules")
        else:
            print("Please specify options or modules to show!")
        return

    def show_options(self, *args, **kwargs):
        max_l = 0
        for k, v in zip(self.vars.keys(), self.vars.values()):
            if len(k) + 2 > max_l:
                max_l = len(k) + 2
            if len(v) > max_l:
                max_l = len(v)
        if (2 * max_l - 3) % 2 != 0:
            max_l += 1
        title_padding = int((2 * max_l - 3) / 2)
        print(f"{' ' * title_padding}" +
              f"{self.luciferManager.termcolor.colored('Vars', 'green', attrs=['bold', 'underline'])}")
        print("=" * (2 * title_padding + 5))
        for k, v in zip(self.vars.keys(), self.vars.values()):
            print(f"{k}{' ' * (max_l - len(k))}| {v}")
        return

    def use_module(self, mod_path: list):
        if self.module_obj is not None:
            self.loaded_modules[self.module] = self.module_obj
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
        if self.auto_vars:
            self.set_vars()
        return

    def run_module(self, *args, **kwargs):
        try:
            if self.module_obj is not None:
                self.module_obj.run()
                return
            else:
                print("Please Select A Module First!")
                return
        except Exception as e:
            checkErrors(e)

    def describe_module(self, *args, **kwargs):
        try:
            if self.module_obj is not None:
                print(self.module_obj.get_description())
                return
            else:
                print("Please Select A Module First!")
                return
        except Exception as e:
            checkErrors(e)

    def set_vars(self, *args, **kwargs):
        try:
            if self.module_obj is not None:
                self.vars.update(self.module_obj.set_vars())
                return
            else:
                print("Please Select A Module First!")
                return
        except Exception as e:
            checkErrors(e)

    def open_shell(self, com_args: list):
        if len(com_args) > 1:
            openid = com_args[1].rstrip()
            if check_int(openid):
                openid = int(openid)
                if openid == 0:
                    self.luciferManager.current_shell_id = 0
                    self.luciferManager.main_shell.spawn()
                    return
                else:
                    found = False
                    for index, shell in enumerate(self.luciferManager.alternative_shells):
                        if shell.id == openid:
                            self.luciferManager.current_shell_id = openid
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

    def show_shells(self, *args, **kwargs):
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

    def clear_shell(self, *args, **kwargs):
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

    def change_auto_set_vars(self, com_args: list):
        com_args.pop(0)
        if len(com_args) > 0:
            to_set = None
            set_global = False
            set_for_new = False
            inclusive = False
            for argument in com_args:
                argument = argument.rstrip()
                if argument.lower() == "true" or argument.lower() == "t" or argument.lower() == "-t":
                    to_set = True
                elif argument.lower() == "false" or argument.lower() == "f" or argument.lower() == "-f":
                    to_set = False
                elif argument.lower() == "-g":
                    set_global = True
                elif argument.lower() == "-n":
                    set_for_new = True
                elif argument.lower() == "-i":
                    inclusive = True
            if to_set is None:
                print("Please Add An Argument!")
                return
            if set_global:
                self.luciferManager.main_shell.auto_vars = to_set
                for shell in self.luciferManager.alternative_shells:
                    shell.auto_vars = to_set
                print(f"Auto Variable On All Shells => {to_set}")
            if (not set_for_new and not set_global) or inclusive:
                self.auto_vars = to_set
                print(f"This Shell Auto Vars => {to_set}")
            if set_for_new:
                self.luciferManager.auto_vars = to_set
                print(f"Future Shells Will Have Auto Vars => {to_set}")
            return
        else:
            print("Please Add Arguments!")

    def print_auto_vars(self, *args, **kwargs):
        print(f"Auto Var => {self.auto_vars}")
