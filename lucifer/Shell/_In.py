def getIn(self):
    self.shell_in = input(f"{self.program_name}|" +
                          f"{self.module if '.py' not in self.module else self.module.replace('.py', '')}" +
                          f"|{self.id}> ")
    if self.luciferManager.log_file is not None:
        if self.luciferManager.log_amount == 1:
            self.luciferManager.log_command(self.shell_in)


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