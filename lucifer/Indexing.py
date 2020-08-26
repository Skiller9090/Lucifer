import os


def recursive_scan_dir(dirname):
    sub_folders = [f.path for f in os.scandir(dirname) if f.is_dir() and "__pycache__" not in f.path]
    for dirname in list(sub_folders):
        sub_folders.extend(recursive_scan_dir(dirname))
    return [fo.replace("modules\\", "") for fo in sub_folders]


def scan_modules(dirname):
    modules = [f.path for f in os.scandir(dirname) if f.is_file() and "__init__.py" not in f.path]
    return [fo.replace(dirname, "").replace("\\", "") for fo in modules]


def index_modules():
    base_path = "modules\\"
    path = ""
    sub_folders = recursive_scan_dir(base_path)  # {"file_name": {"folders": {}, "modules": {}}}
    tree = {}
    modules = {}
    for sf in sub_folders:
        split_path = sf.split("\\")
        current_node = tree
        for ind, dir in enumerate(split_path):
            if dir not in current_node.keys():
                current_node[dir] = {
                    "folders": {},
                    "modules": {}
                }
                for module in scan_modules(base_path + "\\".join(split_path[0:ind + 1])):
                    current_node[dir]["modules"][module] = {
                        "name": module,
                        "path": base_path + "\\".join(split_path[0:ind + 1]) + "\\" + module
                    }
                    modules[base_path + "\\".join(split_path[0:ind + 1]) + "\\" + module] = {
                        "name": module,
                        "path": base_path + "\\".join(split_path[0:ind + 1]) + "\\" + module
                    }
            current_node = current_node[dir]["folders"]
    return tree, modules, sub_folders



