from termcolor import colored

help_menu = f"""{colored('Help Menu', 'red', attrs=['bold', 'underline'])}
{colored("=========================================", "magenta")}
{colored('help', 'blue')}                - Displays This Menu
{colored('name', 'blue')}                - Shows name of current shell
{colored('id', 'blue')}                  - Displays current shell's id
{colored('show', 'blue')}                - Shows options or modules based on input,\
 EX: show <options/modules> 
{colored('options', 'blue')}             - Shows a list of variable/options already set
{colored('set', 'blue')}                 - Sets a variable or option, EX: set <var> <data>
{colored('set_vars', 'blue')}            - Auto sets need variables for loaded module
{colored('description', 'blue')}         - Displays description of the module loaded
{colored('auto_vars', 'blue')}           - Displays is auto_vars is True or False for\
current shell 
{colored('change_auto_vars', 'blue')}    - Changes the auto_var options for one shell, \
all shells or future shells 
{colored('reindex', 'blue')}                - Reindex all modules, allowing dynamic module changing
{colored('use', 'blue')}                 - Move into a module, EX: use <module>
{colored('run', 'blue')}                 - Runs the current module, can also use \
exploit to do the same 
{colored('spawn_shell', 'blue')}         - Spawns a alternative shell
{colored('open_shell', 'blue')}          - Open a shell by id EX: open_shell <id>
{colored('show_shells', 'blue')}         - Show all shell ids and attached name
{colored('set_name', 'blue')}            - Sets current shells name EX: set_name <name>
{colored('set_name_id', 'blue')}         - Set a shells name by id EX: set_name_id <id> \
<name> 
{colored('clear', 'blue')}               - Clear screen
{colored('close', 'blue')}               - Kills current input into opened shell
{colored('reset', 'blue')}               - Resets Everything
{colored('exit', 'blue')}                - Exits the program, can also use quit to do \
the same 
"""
