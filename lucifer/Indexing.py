import os


def recursive_scan_dir(dirname, base_path):
    sub_folders = [f.path for f in os.scandir(dirname)
                   if f.is_dir() and "__pycache__" not in f.path]
    for dirname in list(sub_folders):
        sub_folders.extend(recursive_scan_dir(dirname, base_path))
    return [fo.replace(base_path, "").replace("\\", "/")
            for fo in sub_folders]


def scan_modules(dirname):
    modules = [f.path for f in os.scandir(dirname)
               if f.is_file() and "__init__.py" not in f.path]
    return [fo.replace(dirname, "").replace("/", "").replace("\\", "") for fo in modules]


def index_modules():
    base_path = "modules/"
    return index_python_files(base_path)


def index_python_files(base_path, full=False):
    sub_folders = recursive_scan_dir(base_path, base_path)
    if full:
        sub_folders.insert(0, "")
    # {"file_name": {"folders": {}# , "modules": {}}}
    tree = {}
    modules = {}
    for sf in sub_folders:
        split_path = sf.split("/")
        current_node = tree
        enum_split_path(base_path, current_node, modules, split_path)
    return tree, modules, sub_folders


def enum_split_path(base_path, current_node, modules, split_path):
    for ind, dir_name in enumerate(split_path):
        if dir_name not in current_node.keys():
            current_node[dir_name] = {
                "folders": {},
                "modules": {}
            }
            for module in scan_modules(
                    base_path + "/".join(split_path[0:ind + 1])):
                current_node[dir_name]["modules"][module] = {
                    "name": module,
                    "path": base_path + "/".join(
                        split_path[0:ind + 1]) + "/" + module
                }
                modules[base_path + "/".join(
                    split_path[0:ind + 1]) + "/" + module] = {
                    "name": module,
                    "path": base_path + "/".join(
                        split_path[0:ind + 1]) + "/" + module
                }
        current_node = current_node[dir_name]["folders"]
