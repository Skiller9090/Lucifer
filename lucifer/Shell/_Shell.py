from lucifer.Utils import check_int
from lucifer.Errors import checkErrors


def show_shells(self, *args, **kwargs):
    print(f"{self.luciferManager.main_shell.name} => {self.luciferManager.main_shell.id}")
    for shell in self.luciferManager.alternative_shells:
        print(f"{shell.name} => {shell.id}")
    return


def set_name(self, com_args: list):
    if len(com_args) > 1:
        com_args.pop(0)
        self.name = " ".join(com_args)
        print(f"{self.id} => {self.name}")
    return


def set_name_id(self, com_args: list):
    if len(com_args) > 1:
        ID = com_args[1].rstrip()
        if check_int(ID):
            for _ in range(2):
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
    if self.luciferManager.gui is not None:
        self.luciferManager.gui.console.clear()
    else:
        print(self.luciferManager.colorama.ansi.clear_screen())


def open_shell(self, com_args: list):
    if len(com_args) > 1:
        openid = com_args[1].rstrip()
        if check_int(openid):
            openid = int(openid)
            if openid == 0:
                self.luciferManager.gui.console.opened_order.append(openid)
                self.luciferManager.current_shell_id = openid
                try:
                    self.luciferManager.main_shell.spawn()
                except Exception as e:
                    checkErrors(e)
                return
            else:
                for index, shell in enumerate(self.luciferManager.alternative_shells):
                    if shell.id == openid:
                        self.luciferManager.current_shell_id = openid
                        self.luciferManager.gui.console.opened_order.append(openid)
                        try:
                            self.luciferManager.alternative_shells[index].spawn()
                        except Exception as e:
                            checkErrors(e)
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


def background_shell(self, com_args: list):
    if self.luciferManager.gui is None:
        if self.luciferManager.shell_recur == 1:
            self.luciferManager.end()
        else:
            self.luciferManager.shell_recur -= 1
        return 7
    else:
        if len(self.luciferManager.gui.console.opened_order) > 1:
            self.luciferManager.gui.console.opened_order.pop(-1)
            self.luciferManager.current_shell_id = self.luciferManager.gui.console.opened_order[-1]
        else:
            self.luciferManager.end()
