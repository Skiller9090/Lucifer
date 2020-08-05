from .utils import check_int


class Shell:
    def __init__(self, ID, lucifer_manager):
        self.id = ID
        self.is_main = True if self.id == 0 else False
        self.luciferManager = lucifer_manager
        self.gui = False
        self.module = ""
        self.program_name = "Lucifer"
        self.shell_in = ""
        self.vars = {}
        self.help_menu = """help        - Displays This Menu
show        - Shows options or modules based on input, EX: show <options/modules>
use         - Move into a module, EX: use <module>
set         - Sets a variable or option, EX: set <var> <data>
reset       - Resets Everything
spawn_shell - Spawns a alternative shell
open_shell  - Open a shell by id EX: open_shell <id>
show_shells - Show all shell ids and attached name
set_name    - Sets current shells name EX: set_name <name>
set_name_id - Set a shells name by id EX: set_name_id <id> <name>
close       - Closes current shell
id          - Displays current shell's id
exit        - Exits the program, can also use quit to do the same
name        - Shows name of current shell"""
        self.name = "Shell " if not self.is_main else "Main Shell"

    def getIn(self):
        self.shell_in = input(f"{self.program_name}|{self.module}|> ")

    def print_id(self):
        print(f"Shell ID: {self.id}")

    def print_name(self):
        print(f"Shell Name: {self.name}")

    def set_name(self, name):
        self.name = name

    def set_name_id(self, ID, name):
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

    def parseShellIn(self):
        com_args = self.shell_in.split(" ")
        while "" in com_args:
            com_args.remove("")
        if len(com_args) == 0:
            return
        if len(com_args) == 1:
            command = com_args[0].lower()
            if command == "help" or command == "h":
                self.help()
                return
        com = com_args[0].lower().rstrip()
        if com == "set":
            com_args.pop(0)
            com_args = " ".join(com_args)
            self.command_set(com_args)
            return
        if com == "show":
            if len(com_args) > 1:
                if com_args[1].lower().strip() == "options" or com_args[1].lower().strip() == "vars":
                    self.show_options()
                    return
                else:
                    print("Please enter a valid argument: options or modules")
            else:
                print("Please specify options or modules to show!")
        if com == "quit" or com == "exit":
            print("Thank you for using Lucifer, see you next time!")
            exit(0)
        if com == "id":
            self.print_id()
            return
        if com == "spawn_shell":
            self.spawn_shell()
            return
        if com == "open_shell":
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
        if com == "close":
            return 7
        if com == "show_shells":
            print("Main Shell => 0")
            for shell in self.luciferManager.alternative_shells:
                print(f"{shell.name} => {shell.id}")
            return
        if com == "name":
            self.print_name()
            return
        if com == "set_name":
            if len(com_args) > 1:
                com_args.pop(0)
                self.set_name(" ".join(com_args))
                return
        if com == "set_name_id":
            if len(com_args) > 1:
                ID = com_args[1].rstrip()
                if check_int(ID):
                    for i in range(2):
                        com_args.pop(0)
                    self.set_name_id(int(ID), " ".join(com_args))
                else:
                    print("Not a valid ID")
            else:
                print("Please add a valid ID")
        return

    def help(self):
        print(self.help_menu)

    def spawn(self):
        while True:
            self.getIn()
            signal = self.parseShellIn()
            if signal == 7:
                break

    def command_set(self, var_string):
        vsl = var_string.split(" ")
        var = vsl.pop(0).rstrip()
        if var != "":
            var_string = " ".join(vsl)
            self.vars[var] = var_string
            print(f"{var} => {var_string}")
        else:
            print("Please specify a variable to set")

    def spawn_shell(self):
        self.luciferManager.alternative_shells.append(Shell(self.luciferManager.next_shell_id, self.luciferManager))
        self.luciferManager.next_shell_id += 1
        self.luciferManager.alternative_shells[-1].name += str(self.luciferManager.next_shell_id-1)
        print(f"Opened New Shell With ID: {self.luciferManager.next_shell_id-1}")

    def show_options(self):
        print(self.vars)
# help
# show <options/modules>
# use <module>
# set <var> <string>
# reset
