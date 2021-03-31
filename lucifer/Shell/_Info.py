def print_id(self, *args, **kwargs):
    print(f"Shell ID: {self.id}")


def print_name(self, *args, **kwargs):
    print(f"Shell Name: {self.name}")


def display_help(self, *args, **kwargs):
    self.luciferManager.helpMenu.showAllHelpMenus()


def print_auto_vars(self, *args, **kwargs):
    print(f"Auto Var => {self.auto_vars}")
