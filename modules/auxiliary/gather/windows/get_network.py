from LMI.Command import return_output
from modules.Module import BaseModule
from LMI.File import write_file_exists
from LMI import OS
from LMI.Table import generate_table


class Module(BaseModule):
    def run(self):
        command = ["ipconfig"]
        OS.check_os("windows")
        output_file, write_mode, args = self.get_vars()

        out = self.get_command_out(args, command)
        write_file_exists(output_file, out, write_mode)

        interfaces = self.output_to_interfaces(out)
        interface_dictionaries = self.interfaces_to_dict(interfaces)
        if self.isShellRun:
            for interface in interface_dictionaries:
                name = interface["name"]
                del interface["name"]
                print(generate_table(list(zip(interface.keys(), interface.values())),
                                     title=name,
                                     headings=["Key", "Value"]))
                interface["name"] = name
            return interface_dictionaries
        else:
            return interface_dictionaries

    @staticmethod
    def output_to_interfaces(out):
        lines = [o.strip().replace("\r", "") for o in out.split("\n")]
        interfaces = []
        last = 0
        for i, value in enumerate(lines):
            if len(lines) == i + 1:
                continue
            if len(value) < 2:
                continue
            if value[-1] == ":" and lines[i + 1] == "" and value[-2] != " ":
                interfaces.append(lines[last:i])
                last = i
        interfaces = interfaces[1:]
        return interfaces

    @staticmethod
    def interfaces_to_dict(interfaces):
        interface_dictionaries = []
        for i in interfaces:
            while "" in i:
                i.remove("")
            interface = {"name": i[0][:-1]}
            if len(i) > 1:
                prevS = None
                for setting in i[1:]:
                    split = setting.split(":")
                    if len(split) > 1:
                        k, v = split[0].replace(" .", "").strip(), ":".join(split[1:]).strip()
                        placed = False
                        i = 1
                        check = k
                        while not placed:
                            if check not in interface.keys():
                                interface[check] = v
                                prevS = check
                                placed = True
                            else:
                                i += 1
                                check = f"{k} {i}"
                    else:
                        if prevS is not None:
                            interface[prevS] += "\n" + split[0]
            interface_dictionaries.append(interface)
        return interface_dictionaries

    @staticmethod
    def get_command_out(args, command):
        args.insert(0, command[0])
        out = return_output(args)
        return out

    def get_vars(self):
        write_mode = self.shell.vars["write_mode"] if "write_mode" in self.shell.vars.keys() else "w"
        output_file = self.shell.vars["output_file"] if "output_file" in self.shell.vars.keys() else ""
        args = self.shell.vars["args"].split(" ") if "args" in self.shell.vars.keys() else []
        while "" in args:
            args.remove("")
        return output_file, write_mode, args

    def set_vars(self):
        default_vars = {"output_file": "",
                        "write_mode": "w",
                        "args": ""}
        return default_vars

    def get_description(self):
        desc = """Gets Network Information"""
        return desc
