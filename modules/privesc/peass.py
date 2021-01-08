from LMI import Command, OS
from lucifer.Errors import IncompatibleSystemError
from modules.Module import BaseModule
from LMI.File import write_file_exists


class Module(BaseModule):
    def run(self):
        args = []

        platform_name = OS.get_os_type()
        write_mode = self.shell.vars["write_mode"] if "write_mode" in self.shell.vars.keys() else "w"
        output_file = self.shell.vars["output_file"] if "output_file" in self.shell.vars.keys() else ""
        path = "dependencies/peass/" + 'winPEASany.bat' \
            if platform_name == "Windows" else 'peass.sh'

        if OS.path_exists(path):
            path = OS.absolute_path(path)
            if "args" in self.shell.vars.keys():
                args = self.shell.vars["args"].split(" ")
            print("Running PEASS, this might take sometime!")
            args.insert(0, path)
            out = Command.tee_or_return_output(self.isShellRun, args)
            write_file_exists(output_file, out, write_mode)
            return out
        raise IncompatibleSystemError("Unsupported OS or Architecture")

    def set_vars(self):
        default_vars = {"output_file": "",
                        "write_mode": "w",
                        "args": ""}
        return default_vars

    def get_description(self):
        desc = """Privilege Escalation tester script for Windows and Linux"""
        return desc
