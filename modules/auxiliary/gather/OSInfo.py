from LMI import OS

from modules.Module import BaseModule


class Module(BaseModule):
    def run(self):
        if self.isShellRun:
            OSInfo = OS.getOS()[1]
            max_k = 0
            for i in OSInfo.keys():
                if len(i) > max_k:
                    max_k = len(i)
            for name, data in zip(OSInfo.keys(), OSInfo.values()):
                print(f"{name}{' '*(max_k-len(name))} : {data}")
        else:
            return OS.getOS()

    def set_vars(self):
        default_vars = {}
        return default_vars

    def get_description(self):
        desc = """Returns all OS infomation"""
        return desc
