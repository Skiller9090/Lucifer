import lzma
import os
import subprocess
import tarfile
import zipfile

from termcolor import colored

from ..Data import _JavaInstallsData


def getFileExt(fileName):
    if fileName.endswith(".tar.gz"):
        return "tar.gz"
    if "." in fileName:
        return fileName.split(".")[-1]
    return ""


def _extract_files(file, file_ending, destination_folder, verbose=True, vv=False):
    if verbose and vv:
        print(f"Archive Type: {file_ending}")
    if os.path.isfile(file):
        if verbose and vv:
            print("Extracting jdk")
        start_listing = set(os.listdir(destination_folder))
        if file_ending == "tar":
            with tarfile.open(file, "r:") as tar:
                tar.extractall(path=destination_folder)
        elif file_ending == "tar.gz":
            with tarfile.open(file, "r:gz") as tar:
                tar.extractall(path=destination_folder)
        elif file_ending == "zip":
            with zipfile.ZipFile(file) as z:
                z.extractall(path=os.path.abspath(destination_folder))
        elif file_ending == "7z":
            with lzma.open(file) as z:
                z.extractall(path=destination_folder)
        else:
            if verbose:
                print(colored("Not a supported archive type!", "red"))
        end_listing = set(os.listdir(destination_folder))
        try:
            jdk_directory = next(iter(end_listing.difference(start_listing)))
        except StopIteration:
            jdk_directory = ""
        if verbose:
            print(colored("Installation of Java JDK Complete!", "green"))
        return os.path.join(destination_folder, jdk_directory)


def _path_parse(file_path):
    dirname = os.path.dirname(file_path)
    base = os.path.basename(file_path)
    name, ext = os.path.splitext(base)
    return _JavaInstallsData.Path(dir=dirname, base=base, name=name, ext=ext)


def _unpack_jars(fs_path, java_bin_path):
    if os.path.exists(fs_path):
        if os.path.isdir(fs_path):
            for f in os.listdir(fs_path):
                current_path = os.path.join(fs_path, f)
                _unpack_jars(current_path, java_bin_path)
        else:
            file_name, file_ext = os.path.splitext(fs_path)
            if file_ext.endswith("pack"):
                p = _path_parse(fs_path)
                name = os.path.join(p.dir, p.name)
                tool_path = os.path.join(java_bin_path, _JavaInstallsData.UNPACK200)
                subprocess.run([tool_path, _JavaInstallsData.UNPACK200_ARGS, f"{name}.pack", f"{name}.jar"])


def _decompress_archive(repo_root, file_ending, destination_folder, verbose=True, vv=False):
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)

    jdk_file = os.path.normpath(repo_root)

    if verbose and vv:
        print(f"jdk file: {jdk_file}")
    if os.path.isfile(jdk_file):
        jdk_directory = _extract_files(jdk_file, file_ending, destination_folder, verbose=verbose, vv=vv)
        if verbose and vv:
            print(f"jdk directory: {jdk_directory}")
        jdk_bin = os.path.join(jdk_directory, "bin")
        _unpack_jars(jdk_directory, jdk_bin)
        return jdk_directory
    elif os.path.isdir(jdk_file):
        return jdk_file
