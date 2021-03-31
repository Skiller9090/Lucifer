from termcolor import colored


class HelpMenu:
    def __init__(self):
        self.registeredHelpMenus = {}
        self.header = f"{colored('Help Menu', 'red', attrs=['bold', 'underline'])}"
        self.footer = "\n\n"
        self.padding = 2

    def registerMenu(self, name, desc, defaultHelp):
        default = {
            "name": name,
            "desc": desc,
            "help-lines": {},
            "max_len_key": -1,
        }
        max_len_key = -1
        for key, value in zip(defaultHelp.keys(), defaultHelp.values()):
            len_key = len(str(key))
            if len_key > max_len_key:
                max_len_key = len_key
            default["help-lines"][str(key)] = str(value)
        default["max_len_key"] = max_len_key
        self.registeredHelpMenus[name] = default

    def registerCustom(self, helpObject):
        self.registeredHelpMenus[helpObject["name"]] = helpObject

    def getMenus(self):
        return self.registeredHelpMenus

    def getMenuNames(self):
        return [x["name"] for x in self.registeredHelpMenus]

    def showHelpMenu(self, name):
        if name in self.registeredHelpMenus.keys():
            self.displayMenu(self.registeredHelpMenus[name])
            return True
        return False

    def showHelpMenus(self, names):
        self.showHeader()
        for name in names:
            self.showHelpMenu(name)
        self.showFooter()

    def showAllHelpMenus(self):
        self.showHeader()
        for helpMenu in self.registeredHelpMenus.values():
            self.displayMenu(helpMenu)
        self.showFooter()

    def displayMenu(self, menu):
        max_len_key = menu["max_len_key"]
        toDisplay = ""
        toDisplay += f"{colored('='*5 + menu['name'] + '='*5, 'magenta')}\n"
        toDisplay += f"{colored(menu['desc'], 'grey')}\n\n"
        for key, value in zip(menu["help-lines"].keys(), menu["help-lines"].values()):
            spaceLeft = (max_len_key + self.padding) - len(key)
            toDisplay += f"{colored(key, 'blue')}{' ' * spaceLeft}-{' ' * self.padding}{value}\n"
        print(toDisplay)

    def showHeader(self):
        print(self.header)

    def showFooter(self):
        print(self.footer)
