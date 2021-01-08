from LMI import OS
from LMI.Table import generate_table
from modules.Module import BaseModule


class Module(BaseModule):
    def run(self):
        if self.isShellRun:
            OSInfo = OS.get_OS()[1]
            table_show = OSInfo.copy()
            print(table_show)
            del table_show["uname"]
            print(generate_table(list(zip(table_show.keys(), table_show.values())),
                                 title="OS Info",
                                 headings=["Key", "Value"]))
            print(f"Uname: {OSInfo.get('uname')}")
        else:
            return OS.get_OS()[1]

    def set_vars(self):
        default_vars = {}
        return default_vars

    def get_description(self):
        desc = """Returns all OS information"""
        return desc
