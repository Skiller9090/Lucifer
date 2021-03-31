import os
from glob import glob

from ..JavaData import _JavaInstallsData


def get_lucifer_java_versions():
    directories = glob(_JavaInstallsData.getInstance().LUCIFER_JDK_DIR + f"{os.sep}*{os.sep}", recursive=False)
    versionFolderNames = list(map(
        lambda x: x.replace(_JavaInstallsData.getInstance().LUCIFER_JDK_DIR, "").replace(os.sep, ""), directories
    ))
    javaVersions = {}
    for javaDirectory, versionFolderName in zip(directories, versionFolderNames):
        javaVersions[versionFolderName] = {
            "folderName": versionFolderName,
            "folderPath": javaDirectory,
            "variant": "Unknown",
            "version": versionFolderName.replace("jdk", ""),
            "location": _JavaInstallsData.getInstance().LUCIFER_RELATIVE_JDK_DIR,
            "releaseData": {}
        }
        if javaVersions[versionFolderName]["version"].startswith("-"):
            javaVersions[versionFolderName]["version"] = javaVersions[versionFolderName]["version"][1:]
        if os.path.exists(os.path.join(javaDirectory, "release")):
            with open(os.path.join(javaDirectory, "release"), "r") as f:
                rawReleaseData = f.read().strip()
            releaseData = {line.split("=")[0].replace("\"", ""): line.split("=")[1].replace("\"", "")
                           for line in rawReleaseData.split("\n")}
            javaVersions[versionFolderName]["releaseData"] = releaseData
    return javaVersions
