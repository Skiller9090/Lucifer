import argparse
import os
import re as _re
import sys

from ttkthemes import themed_tk

from .GUI.GUI import LuciferGui
from .Manager import LuciferManager
from .Shell import Shell
from .Indexing import index_python_files


def get_lines(parts, indent, text_width, prefix=None):
    lines = []
    line = []
    if prefix is not None:
        line_len = len(prefix) - 1
    else:
        line_len = len(indent) - 1
    for part in parts:
        if line_len + 1 + len(part) > text_width:
            lines.append(indent + ' '.join(line))
            line = []
            line_len = len(indent) - 1
        line.append(part)
        line_len += len(part) + 1
    if line:
        lines.append(indent + ' '.join(line))
    if prefix is not None:
        lines[0] = lines[0][len(indent):]
    return lines


def ext_prog(opt_parts, pos_parts, prefix, prog, text_width):
    if len(prefix) + len(prog) <= 0.75 * text_width:
        lines = ext_short(opt_parts, pos_parts, prefix, prog, text_width)

    # if prog is long, put it on its own line
    else:
        lines = ext_long(opt_parts, pos_parts, prefix, prog, text_width)
    return lines


def ext_long(opt_parts, pos_parts, prefix, prog, text_width):
    indent = ' ' * len(prefix)
    parts = opt_parts + pos_parts
    lines = get_lines(parts, indent, text_width)
    if len(lines) > 1:
        lines = []
        lines.extend(get_lines(opt_parts, indent, text_width))
        lines.extend(get_lines(pos_parts, indent, text_width))
    lines = [prog] + lines
    return lines


def ext_short(opt_parts, pos_parts, prefix, prog, text_width):
    indent = ' ' * (len(prefix) + len(prog) + 1)
    if opt_parts:
        lines = get_lines([prog] + opt_parts, indent, text_width, prefix)
        lines.extend(get_lines(pos_parts, indent, text_width))
    elif pos_parts:
        lines = get_lines([prog] + pos_parts, indent, text_width, prefix)
    else:
        lines = [prog]
    return lines


class CapitalisedHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Usage: '
        usage = self.generate_usage(groups, prefix, actions)
        return super(CapitalisedHelpFormatter, self).add_usage(
            usage, actions, groups, prefix)

    def generate_usage(self, groups, prefix, actions):
        formats, optionals, positionals, prog, usage = self.build_usage_string(actions, groups)
        text_width = self._width - self._current_indent

        if len(prefix) + len(usage) > text_width:
            # break usage into wrappable parts
            part_regexp = r'\(.*?\)+|\[.*?\]+|\S+'
            opt_usage = formats(optionals, groups)
            pos_usage = formats(positionals, groups)
            opt_parts = _re.findall(part_regexp, opt_usage)
            pos_parts = _re.findall(part_regexp, pos_usage)
            assert ' '.join(opt_parts) == opt_usage
            assert ' '.join(pos_parts) == pos_usage

            # if prog is short, follow it with optionals or positionals
            lines = ext_prog(opt_parts, pos_parts, prefix, prog, text_width)

            # join lines into usage
            usage = '\n'.join(lines)
        return usage.replace("()", "python main.py")

    def build_usage_string(self, actions, groups):
        prog = '%(prog)s' % dict(prog=self._prog)
        # split optionals from positionals
        optionals = []
        positionals = []
        for action in actions:
            if action.option_strings:
                optionals.append(action)
            else:
                positionals.append(action)
        # build full usage string
        formats = self._format_actions_usage
        action_usage = formats(optionals + positionals, groups)
        usage = ' '.join([s for s in [prog, action_usage] if s])
        return formats, optionals, positionals, prog, usage


class LuciferParser(argparse.ArgumentParser):
    def __init__(self, lucifer_manager: LuciferManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.args = None
        self.luciferManager = lucifer_manager
        self.formatter_class = CapitalisedHelpFormatter

    def error_usage(self, message: str):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(os.EX_USAGE)

    def check_gui(self):
        if self.args.gui:
            self.luciferManager.gui = True
            self.luciferManager.main_shell = Shell(self.luciferManager.next_shell_id, self.luciferManager)
            self.luciferManager.next_shell_id += 1
            root = themed_tk.ThemedTk()
            root.set_theme("arc", toplevel=None, themebg=('#%02x%02x%02x' % (39, 44, 53)))
            self.luciferManager.root = root
            application = LuciferGui(self.luciferManager, root)
            self.luciferManager.gui = application
            root.mainloop()

        else:
            self.luciferManager.colorama.init(autoreset=True)
            print(self.luciferManager.termcolor.colored(self.luciferManager.version,
                                                        "red", attrs=["bold", "underline"]))
            self.luciferManager.main_shell = Shell(self.luciferManager.next_shell_id, self.luciferManager)
            self.luciferManager.next_shell_id += 1
            self.luciferManager.main_shell.spawn()

    def check_autoSet(self):
        if self.args.auto_set_vars:
            self.luciferManager.auto_vars = True
            print("Auto Set Variables Enabled")

    def check_logging(self):
        if self.args.logger_loc is not None:
            if not os.path.exists(self.args.logger_loc):
                open(self.args.logger_loc, "w").close()
            self.luciferManager.log_file = self.args.logger_loc
            self.luciferManager.log_amount = 1  # 0 - None, 1 - Commands

    def check_tests(self):
        if self.args.test:
            self.luciferManager.runTests = True
            print("Starting lucifer tests...")

    @staticmethod
    def runTests():
        from LMI import LTF
        import importlib
        import inspect

        test_runner = LTF.TestsRunner()
        _, modules, _ = index_python_files("tests/", full=True)
        for module in modules:
            module = modules[module]["path"]
            module = os.path.normpath(module)
            to_import = (module.replace("/", ".").replace("\\", ".")
                         if ".py" not in module else
                         module.replace(".py", "").replace("/", ".").replace("\\", "."))
            importlib.invalidate_caches()
            imported_module = importlib.import_module(to_import)
            for name, obj in inspect.getmembers(imported_module):
                if inspect.isclass(obj) and obj.__module__ == to_import:
                    if issubclass(obj, LTF.Tests.LTFTest):
                        test_runner.add_LTF_test(obj)
        test_runner.runAll()
        breakdown = LTF.Formatters.PercentageShort(test_runner.statistics)
        breakdown.show()

    def run(self):
        self.check_logging()
        self.check_tests()
        self.check_autoSet()
        if not self.luciferManager.runTests:
            self.check_gui()
        else:
            self.runTests()

    def add_lucifer_args(self):
        self.add_argument("-l", "--log-commands", dest="logger_loc", help="Enables Command Logging To File",
                          action="store", required=False)
        self.add_argument("-g", "--gui", help="Enables The Gui Mode",
                          action="store_true", required=False)
        self.add_argument("-a", "--auto-set-vars", dest="auto_set_vars",
                          help="Enables Auto Setting of Vars On Module Load",
                          action="store_true", required=False)
        self.add_argument("-S", "--skip-requirements-check", dest="skip_requirements",
                          help="Skips the checking of requirements within lucifer",
                          action="store_true", required=False)
        self.add_argument("-T", "--test", dest="test",
                          help="Runs all the lucifer tests",
                          action="store_true", required=False)
