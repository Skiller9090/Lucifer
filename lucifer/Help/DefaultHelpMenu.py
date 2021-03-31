from LMI.Java import Run


def registerDefaultHelpMenu(luciferManager):
    luciferManager.helpMenu.registerMenu(
        "Core", "These are all the core commands of Lucifer",
        {
            "help": "Displays This Menu",
            "name": "Shows name of current shell",
            "id": "Displays current shell's id",
            "show": "Shows options or modules based on input, EX: show <options/modules>",
            "options": "Shows a list of variable/options already set",
            "set": "Sets a variable or option, EX: set <var> <data>",
            "set_vars": "Auto sets need variables for loaded module",
            "description": "Displays description of the module loaded",
            "auto_vars": "Displays is auto_vars is True or False for current shell",
            "change_auto_vars": "Changes the auto_var options for one shell, all shells or future shells",
            "reindex": "Reindex all modules, allowing dynamic module changing",
            "use": "Move into a module, EX: use <module>",
            "run": "Runs the current module, can also use exploit to do the same",
            "spawn_shell": "Spawns a alternative shell",
            "open_shell": "Open a shell by id EX: open_shell <id>",
            "show_shells": "Show all shell ids and attached name",
            "set_name": "Sets current shells name EX: set_name <name>",
            "set_name_id": "Set a shells name by id EX: set_name_id <id> <name>",
            "clear": "Clear screen",
            "close": "Kills current input into opened shell",
            "reset": "Resets Everything",
            "exit": "Exits the program, can also use quit to do the same"
        }
    )

    luciferManager.helpMenu.registerMenu(
        "LMI.Reports Extension", "These are all the commands to create reports from your command/module output",
        {
            "report_new": "Creates a new report if not exists else opens the report",
            "report_open": "Opens report file if exists else creates new one and opens that one",
            "report_start": "Starts reporting tabled output to the file, aliases: report_on",
            "report_stop": "Stops reporting tabled output to the file, aliases: report_pause, report_off"
        }
    )

    if Run.isJPypeInstalled:
        luciferManager.helpMenu.registerMenu(
            "LMI.Java Extension", "These are all the commands to work with java and python+java modules",
            {
                "install_java": "Install a java version of choice",
                "uninstall_java": "Uninstall a java version of choice",
                "get_java_installs": "List all installed java versions",
                "set_jdk": "Sets the current jdk by id",
                "start_jvm": "Starts the java jvm for lucifer",
                "build_java_modules": "Builds all of lucifer java files into jar file",
                "load_lucifer_jar": "Loads the created jar from the build_java_modules command"
            }
        )
