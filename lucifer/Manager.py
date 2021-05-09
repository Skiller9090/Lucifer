import sys
import time

import colorama
import termcolor

import lucifer.Indexing as Indexing
from lucifer.Help import HelpMenu, registerDefaultHelpMenu
from lucifer.Networking.Connections import Connections
from lucifer.Networking.Servers import Servers


class LuciferManager:
    def __init__(self, auto_vars=False):
        self.main_shell = None
        self.alternative_shells = []
        self.plugin_aliases = {}
        self.next_shell_id = 0
        self.shell_recur = 0
        self.colorama = colorama
        self.termcolor = termcolor
        self.current_shell_id = 0
        self.auto_vars = auto_vars
        self.log_file = None
        self.log_amount = 0
        self.gui = None
        self.gui_thread_free = True
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.isLMI = False
        self.runTests = False
        # MAJOR.MINOR.PATCH.STAGE.BUILD VERSIONING
        self.numeric_version = (0, 8, 7, 3, 1)
        self.numeric_stage = self.numeric_version[3]
        self.stage = ["Alpha", "Beta", "RC", "Release"][self.numeric_version[3]]
        self.shortStage = ["a", "b", "rc", "r"][self.numeric_version[3]]
        self.major = self.numeric_version[0]
        self.minor = self.numeric_version[1]
        self.patch = self.numeric_version[2]
        self.build = self.numeric_version[4]
        self.version = f"{self.stage} {self.major}.{self.minor}.{self.patch} " \
                       f"Build {self.build} " \
                       f"({self.major}.{self.minor}.{self.patch}{self.shortStage}" \
                       f"{self.build})"
        self.module_cache = None
        self.module_amount = 0
        self.index_modules()
        self.connections = Connections()
        self.servers = Servers()
        self.helpMenu = HelpMenu()
        registerDefaultHelpMenu(self)

    def end(self, *args, **kwargs):
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__
        print("Thank you for using lucifer, see you next time!")
        if self.log_amount > 0:
            if self.log_file is not None:
                self.log_file.close()
        if self.gui is not None:
            self.gui.parent.destroy()
        exit(0)

    def log_command(self, command):
        with open(self.log_file, "a") as f:
            f.write(f"Command:> {str(command)}\n")

    def index_modules(self, re=False):
        print("Indexing Modules...")
        start_clock = time.perf_counter_ns()
        self.module_cache = Indexing.index_modules()
        end_clock = time.perf_counter_ns()
        print(f"Indexing Of Modules Took: {(end_clock - start_clock) / 1000000} ms")
        self.module_amount = len(self.module_cache[1].keys())
        result = f"indexing Complete, Found {self.module_amount} Modules"
        if re:
            result = "re" + result
        print(result.title())

    def add_command_all(self, name, function):
        self.main_shell.alias[name] = function
        for shell in self.alternative_shells:
            shell.alias[name] = function
