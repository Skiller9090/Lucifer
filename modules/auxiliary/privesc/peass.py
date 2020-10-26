import os
import platform

from LMI import Command
from lucifer.Errors import IncompatibleSystemError
from modules.Module import BaseModule


class Module(BaseModule):
    def run(self):
        args = []

        platform_name = platform.system()
        write_mode = self.shell.vars["write_mode"] if "write_mode" in self.shell.vars.keys() else "w"
        output_file = self.shell.vars["output_file"] if "output_file" in self.shell.vars.keys() else ""
        path = "dependencies/peass/" + 'winPEASany.exe' \
            if platform_name == "Windows" else 'peass.sh'

        if os.path.exists(path):
            if "args" in self.shell.vars.keys():
                args = self.shell.vars["args"].split(" ")
            print("Running PEASS, this might take sometime!")
            args.insert(0, path)
            if self.isShellRun:
                out = Command.tee_output(args)
            else:
                out = Command.return_output(args)
            out = out.strip()
            if output_file != "":
                with open(self.shell.vars["output_file"], write_mode) as f:
                    f.write(out)
            if self.isShellRun:
                # print(out)
                pass
            else:
                return out
        else:
            raise IncompatibleSystemError("Unsupported OS or Architecture")

    def set_vars(self):
        default_vars = {"output_file": "",
                        "write_mode": "w",
                        "args": ""}
        return default_vars

    def get_description(self):
        desc = """Privilege Escalation tester script for Windows and Linux"""
        return desc
