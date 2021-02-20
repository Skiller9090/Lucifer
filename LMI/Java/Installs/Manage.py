import os
import shutil

from termcolor import colored

from .. import _JavaInstallsData
from .Get import get_download, _download
from .Extract import getFileExt, _decompress_archive
from .Utils import normalize_version
from .List import get_lucifer_java_versions
from ... import Table

_JavaInstallsData = _JavaInstallsData.instance


def install(version, operating_system=_JavaInstallsData.OS, arch=_JavaInstallsData.ARCH,
            implementation=_JavaInstallsData.impl, verbose=True, vv=False):
    url = get_download(version, operating_system, arch, implementation)
    if not os.path.exists(_JavaInstallsData.LUCIFER_JDK_DIR):
        os.mkdir(_JavaInstallsData.LUCIFER_JDK_DIR)

    jdk_file = None
    try:
        jdk_file = _download(url, verbose=verbose, vv=vv)
        if jdk_file is None:
            print(colored("Java version could not be found for supplied arguments!", "red"))
            return None
        jdk_ext = getFileExt(jdk_file)
        jdk_dir = _decompress_archive(jdk_file, jdk_ext, _JavaInstallsData.LUCIFER_JDK_DIR,
                                      verbose=verbose, vv=vv)
        return jdk_dir
    finally:
        if jdk_file:
            os.remove(jdk_file)
            if verbose and vv:
                print(f"Removed {jdk_file}")


def uninstall(version, verbose=True, vv=False):
    version = normalize_version(version)
    version = f"jdk{version}"
    if verbose and vv:
        print(f"Looking for version: {version}")
    if not os.path.exists(_JavaInstallsData.LUCIFER_JDK_DIR):
        print("No java installations found for lucifer!")
        return
    versions = (v for v in os.listdir(_JavaInstallsData.LUCIFER_JDK_DIR) if version in v.replace("-", ""))
    deleted = 0
    for v in versions:
        if verbose:
            print(f"Uninstalling {v}")
        try:
            shutil.rmtree(os.path.join(_JavaInstallsData.LUCIFER_JDK_DIR, v))
        except PermissionError:
            print(colored(f"Failed to remove {v}, permission error, this could be due to no permissions or a lock. \n"
                          f"NOTE: {v} installation may be corrupted now, highly recommend to delete and reinstall.",
                          "red"))
            continue
        if verbose:
            deleted += 1
            print(colored(f"Uninstalled {v}", "green"))
    if verbose:
        print(f"Uninstalled {deleted} java installations matching {version}!")


def reinstall(version, operating_system=_JavaInstallsData.OS, arch=_JavaInstallsData.ARCH,
              implementation=_JavaInstallsData.impl, verbose=True, vv=False):
    uninstall(version, verbose=verbose, vv=vv)
    install(version, operating_system=operating_system, arch=arch, implementation=implementation,
            verbose=verbose, vv=vv)


def getVersions():
    table = Table.generate_table(
        [[str(i),
          x[0],
          x[1]["releaseData"]["JAVA_VERSION"] if "JAVA_VERSION" in x[1]["releaseData"].keys() else x[1]["version"],
          x[1]["releaseData"]["JVM_VARIANT"] if "JVM_VARIANT" in x[1]["releaseData"] else x[1]["variant"],
          x[1]["location"]
          ] for i, x in enumerate(zip(get_lucifer_java_versions().keys(), get_lucifer_java_versions().values()))],
        title="Java Versions",
        headings=[
            "ID",
            "Name",
            "Version",
            "Variant",
            "Location"
        ]
    )
    return table
