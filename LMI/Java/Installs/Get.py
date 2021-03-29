import cgi
import os
import sys
from urllib import request, error

from termcolor import colored

from .Utils import normalize_version
from ..Data import _JavaInstallsData
from ...Interface import LMI


def get_download(version, operatingSystem, architecture, implementation):
    version = normalize_version(version)
    return f"https://api.adoptopenjdk.net/v3/binary/latest/" \
           f"{version}/ga/{operatingSystem}/{architecture}/jdk/{implementation}" \
           f"/normal/adoptopenjdk"


def _download(download_url, verbose=True, vv=False):
    req = request.Request(download_url, headers={"User-Agent": "Mozilla/5.0"})
    jdk_file = None
    try:
        with request.urlopen(req) as open_request:
            info = open_request.info()
            if "Content-Disposition" in info:
                content_disposition = info["Content-Disposition"]
                _, params = cgi.parse_header(content_disposition)
                if "filename" in params:
                    jdk_file = params["filename"]
                    if verbose:
                        print(f"Downloading: {jdk_file} from {download_url}")
                    jdk_file = os.path.join(_JavaInstallsData.LUCIFER_JDK_DIR, jdk_file)
                    fileSize = int(info["Content-Length"])
                    downloadFileWProgressBar(open_request, jdk_file, fileSize, verbose=verbose)
        if verbose and vv:
            print(colored(f"\nDownloaded jdk to {jdk_file}", "green"))
        elif verbose:
            print(colored("\nDownload Complete", "green"))
        else:
            sys.stdout.write("\n")
            sys.stdout.flush()
        return jdk_file
    except error.HTTPError:
        return None


def downloadFileWProgressBar(open_request, file_name, fileSize, verbose=False):
    with open(file_name, "wb") as out_file:
        copy_bufferSize = 1024 * 1024 if _JavaInstallsData.IS_WINDOWS else 64 * 1024
        total_downloaded = 0
        updateGUI = False
        if LMI.luciferManager is not None and LMI.luciferManager.gui is not None:
            updateGUI = True
        length = 0
        if not length:
            length = copy_bufferSize
        while True:
            buf = open_request.read(length)
            if not buf:
                break
            out_file.write(buf)
            if verbose:
                total_downloaded += len(buf)
                percentDone = total_downloaded / fileSize * 100
                doneBar = int(percentDone / 5)
                sys.stdout.write(f"\r[{'=' * doneBar + '>'}"
                                 f"{' ' * (20 - doneBar)}]"
                                 f" {round(percentDone)}%")
                sys.stdout.flush()
                if updateGUI:
                    LMI.luciferManager.gui.statusFrame.progressBar["value"] = percentDone
