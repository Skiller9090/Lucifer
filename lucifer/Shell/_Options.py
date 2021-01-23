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


def show(self, com_args: list):
    if len(com_args) > 1:
        if (com_args[1].lower().strip() == "options"
                or com_args[1].lower().strip() == "vars"):
            self.show_options()
            return
        print("Please enter a valid argument: options/vars or modules")
    else:
        print("Please specify options or modules to show!")


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
    coloured_title = self.luciferManager.termcolor.colored('Vars',
                                                           'green',
                                                           attrs=['bold',
                                                                  'underline'])
    print(f"{' ' * title_padding}" +
          f"{coloured_title}")
    print("=" * (2 * title_padding + 5))
    for k, v in zip(self.vars.keys(), self.vars.values()):
        print(f"{k}{' ' * (max_l - len(k))}| {v}")


def change_auto_set_vars(self, com_args: list):
    com_args.pop(0)
    if len(com_args) > 0:
        inclusive, set_for_new, set_global, to_set = change_auto_parse_args(com_args)
        if to_set is None:
            print("Please Add An Argument!")
            return
        set_auto_vars(inclusive, self, set_for_new, set_global, to_set)
        return
    print("Please Add Arguments!")


def set_auto_vars(inclusive, self, set_for_new, set_global, to_set):
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


def change_auto_parse_args(com_args):
    to_set = None
    set_global = False
    set_for_new = False
    inclusive = False
    for argument in com_args:
        argument = argument.rstrip()
        if (argument.lower() == "true"
                or argument.lower() == "t" or argument.lower() == "-t"):
            to_set = True
        elif (argument.lower() == "false"
              or argument.lower() == "f" or argument.lower() == "-f"):
            to_set = False
        elif argument.lower() == "-g":
            set_global = True
        elif argument.lower() == "-n":
            set_for_new = True
        elif argument.lower() == "-i":
            inclusive = True
    return inclusive, set_for_new, set_global, to_set
