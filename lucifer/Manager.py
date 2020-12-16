import lucifer.Indexing as Indexing

import sys
import colorama
import termcolor
import time


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
        self.version = "Prototype 4"
        self.numeric_version = (0, 4)
        self.module_cache = None
        self.module_amount = 0
        self.index_modules()

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
        print(f"Indexing Of Modules Took: {(end_clock-start_clock)/1000000} ms")
        self.module_amount = len(self.module_cache[1].keys())
        result = f"indexing Complete, Found {self.module_amount} Modules"
        if re:
            result = "re"+result
        print(result.title())

    def add_command_all(self, name, function):
        self.main_shell.alias[name] = function
        for shell in self.alternative_shells:
            shell.alias[name] = function
