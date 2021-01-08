from LMI.Command import return_output
from LMI.File import write_file_exists
from LMI.Table import generate_table
from LMI.Utils import check_int
from modules.Module import BaseModule
from LMI import OS
from termcolor import colored


class Module(BaseModule):
    def run(self):
        command = ["net", "user"]
        OS.check_os("windows")
        output_file, split_size, write_mode, args = self.get_vars()

        out = self.get_command_out(args, command)
        write_file_exists(output_file, out, write_mode)
        user_stripped_list = self.sort_to_lists(out, split_size)

        if self.isShellRun:
            print(generate_table(user_stripped_list[0], title="Local Users"))
            if user_stripped_list[1]:
                print(generate_table(user_stripped_list[1], title="Remote Users"))
            else:
                print(colored("No remote users", "red"))
        return user_stripped_list

    @staticmethod
    def sort_to_lists(out, split_size):
        user_stripped_list = []
        for o in out:
            gap_splitter = "            "
            user_temp = o.split(gap_splitter)
            user_temp = [y.split("\n") for y in user_temp]
            ut = []
            isUsers = False
            for z in user_temp:
                for e in z:
                    isUsers = False if "The command completed successfully." in e else isUsers
                    if isUsers:
                        ut.append(e.rstrip().strip())
                    isUsers = True if "--------" in e else isUsers
            user_stripped_list.append([ut[x:x + split_size] for x in range(0, len(ut), split_size)])
        return user_stripped_list

    @staticmethod
    def get_command_out(args, command):
        out = []
        for item in reversed(command):
            args.insert(0, item)
        for i in range(2):
            out.append(return_output(args))
            if i == 0:
                args.append("/domain")
        return out

    def get_vars(self):
        write_mode = self.shell.vars["write_mode"] if "write_mode" in self.shell.vars.keys() else "w"
        output_file = self.shell.vars["output_file"] if "output_file" in self.shell.vars.keys() else ""
        split_size = self.shell.vars["split_size"] if "split_size" in self.shell.vars.keys() else "3"
        split_size = int(split_size) if check_int(split_size) else 3
        args = self.shell.vars["args"].split(" ") if "args" in self.shell.vars.keys() else []
        while "" in args:
            args.remove("")
        return output_file, split_size, write_mode, args

    def set_vars(self):
        default_vars = {"output_file": "",
                        "write_mode": "w",
                        "split_size": "3",
                        "args": ""}
        return default_vars

    def get_description(self):
        desc = """Gets all user accounts on the computer and domain"""
        return desc
