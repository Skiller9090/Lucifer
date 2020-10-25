import importlib
import os
import re

from lucifer.Errors import checkErrors


def use_module(self, mod_path: list):
    file, ori_path, path, use_cache = use_arg_setup(mod_path, self)
    for directory in mod_path:
        path += "/" + directory
        if os.path.exists(path):
            if os.path.isdir(path):
                continue
            else:
                print(f"Module: {'/'.join(ori_path)} Does Not Exist!")
                return
        else:
            print(f"Module: {'/'.join(ori_path)} Does Not Exist!")
            return
    if os.path.isfile(path + "/" + file):
        self.module = path + "/" + file
        print(f"Using module: {self.module}")
    elif os.path.isfile(path + "/" + file + ".py"):
        self.module = path + "/" + file + ".py"
        print(f"Using module: {self.module}")
    else:
        print(f"Module: {'/'.join(ori_path)} Does Not Exist!")
        return
    open_module(self, use_cache)
    if self.auto_vars:
        self.set_vars()
    return


def open_module(self, use_cache):
    isInCache = self.module in self.loaded_modules.keys()
    if isInCache and use_cache:
        print(f"Loading {self.module} from cache, use -R to override this.")
        self.module_obj = self.loaded_modules.get(self.module)
    else:
        if isInCache:
            print(f"{self.module} in cache, ignoring it...")
        print(f"Loading {self.module} from file.")
        to_import = (self.module.replace("/", ".")
                     if ".py" not in self.module else
                     self.module.replace(".py", "").replace("/", "."))
        to_import = to_import.split(".")
        pkg = to_import.pop(-1)
        to_import = ".".join(to_import)
        importlib.invalidate_caches()
        try:
            imported_module = importlib.import_module(to_import + "." + pkg)
            if self.module in self.loaded_modules.keys():
                importlib.reload(imported_module)
            self.module_obj = imported_module.Module(self.luciferManager,
                                                     ShellRun=True)
            self.loaded_modules[self.module] = self.module_obj
        except ModuleNotFoundError as e:
            handle_module_error(e, pkg, self)
        except AttributeError as e:
            handle_module_error(e, pkg, self)


def handle_module_error(e, pkg, self):
    error = f'Error: Cant find attribute Module in {pkg}'
    self.module_obj = None
    self.module = ""
    print(f"{self.luciferManager.termcolor.colored(error, 'red')}")


def use_arg_setup(mod_path, self):
    use_cache = True
    if "-R" in mod_path:
        mod_path.remove("-R")
        use_cache = False
    if self.module_obj is not None:
        self.loaded_modules[self.module] = self.module_obj
    ori_path = mod_path.copy()
    file = mod_path.pop(-1)
    path = "modules"
    return file, ori_path, path, use_cache


def run_module(self, *args, **kwargs):
    try:
        if self.module_obj is not None:
            self.module_obj.run()
        else:
            print("Please Select A Module First!")
    except Exception as e:
        checkErrors(e, ModuleError=True)


def describe_module(self, *args, **kwargs):
    try:
        if self.module_obj is not None:
            print(self.module_obj.get_description())
            return
        print("Please Select A Module First!")
    except Exception as e:
        checkErrors(e)


def set_vars(self, *args, **kwargs):
    try:
        if self.module_obj is not None:
            self.vars.update(self.module_obj.set_vars())
            return
        print("Please Select A Module First!")
    except Exception as e:
        checkErrors(e)


def use(self, com_args: list):
    if len(com_args) > 1:
        if len(com_args) == 2:
            module_path = re.split(r"\\|/|,", com_args[1].rstrip())
        else:
            com_args.pop(0)
            module_path = re.split(r"\\| |/|,", " ".join(com_args).rstrip())
        if module_path:
            while "" in module_path:
                module_path.remove("")
            self.use_module(module_path)
    else:
        print("Please add valid module path")
