"""The Shell package contains the code to operate the console."""
from LMI import Java
from lucifer.Help import help_menu


class Shell:
    from ._In import parseShellIn, getIn
    from ._Info import display_help, print_name, print_id, print_auto_vars
    from ._Spawn import spawn_shell, spawn
    from ._Options import show, show_options, command_set, change_auto_set_vars
    from ._Module import describe_module, run_module, use_module, set_vars, use, reindex_modules
    from ._Shell import open_shell, show_shells, set_name, command_name_id, \
        clear_shell, background_shell
    from ._Networking import listServers, killServer
    from ._Java import installJava, reinstallJava, uninstallJava, getJavaInstalls, setJavaJDK, startJavaJVM, \
        buildJar, loadLuciferJar

    def __init__(self, ID, lucifer_manager):
        """Per Shell Setup."""
        self.id = ID
        self.is_main = True if self.id == 0 else False
        self.luciferManager = lucifer_manager
        self.gui = False
        self.module = ""
        self.module_obj = None
        self.loaded_modules = {}
        self.program_name = "lucifer"
        self.shell_in = ""
        self.vars = {}
        self.auto_vars = lucifer_manager.auto_vars
        self.help_menu = help_menu
        self.name = "Shell " if not self.is_main else "Main Shell"
        self.alias = {
            "help": self.display_help,
            "set": self.command_set,
            "show": self.show,
            "quit": self.luciferManager.end,
            "exit": self.luciferManager.end,
            "id": self.print_id,
            "spawn_shell": self.spawn_shell,
            "open_shell": self.open_shell,
            "close": self.background_shell,
            "show_shells": self.show_shells,
            "name": self.print_name,
            "set_name": self.set_name,
            "set_name_id": self.command_name_id,
            "clear": self.clear_shell,
            "use": self.use,
            "run": self.run_module,
            "exploit": self.run_module,
            "set_vars": self.set_vars,
            "options": self.show_options,
            "description": self.describe_module,
            "describe": self.describe_module,
            "auto_vars": self.print_auto_vars,
            "change_auto_vars": self.change_auto_set_vars,
            "auto_var": self.print_auto_vars,
            "change_auto_var": self.change_auto_set_vars,
            "reindex": self.reindex_modules,
            "show_servers": self.listServers,
            "kill_sever": self.killServer,
        }
        self.luciferManager.shell_recur += 1

        self.Shell_Class = Shell
        if Java.Run.isJPypeInstalled:
            self.addJavaModules()

    def addJavaModules(self):
        javaCommands = {
            "install_java": self.installJava,
            "reinstall_java": self.reinstallJava,
            "uninstall_java": self.uninstallJava,
            "get_installs_java": self.getJavaInstalls,
            "get_java_installs": self.getJavaInstalls,
            "set_jdk_java": self.setJavaJDK,
            "set_jdk": self.setJavaJDK,
            "start_jvm_java": self.startJavaJVM,
            "start_jvm": self.startJavaJVM,
            "build_java_modules": self.buildJar,
            "build_java": self.buildJar,
            "build_modules": self.buildJar,
            "load_lucifer_jar": self.loadLuciferJar
        }
        self.alias.update(javaCommands)
