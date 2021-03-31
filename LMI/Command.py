import subprocess
import sys
import os


def return_output(command, shell=False):
    all_output = process_command(command, stdout=subprocess.PIPE, shell=shell)
    return all_output


def tee_output(command, stdout=None, stderr=None, shell=False):
    if stdout is None:
        stdout = sys.stdout
    if stderr is None:
        stderr = sys.stderr
    tee_out = process_command(command, stdout, tee=True, stderr=stderr, shell=shell)
    return tee_out


def process_command(command, stdout=None, stderr=None, tee=False, shell=False):
    if stdout is None:
        stdout = sys.stdout
    if stderr is None:
        stderr = sys.stderr
    if not shell and isinstance(command, str) and os.name != "nt":
        command = command.split(" ")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=stderr, shell=shell)
    all_output = ""
    while True:
        output = process.stdout.readline().decode(sys.getfilesystemencoding(), "ignore")
        if output == '' and process.poll() is not None:
            break
        if output:
            all_output += output
            if tee:
                stdout.write(output)
    return all_output


def run_command(command):
    subprocess.call(command, stdout=subprocess.PIPE)
    return True


def async_run_command(command):
    interface = subprocess.Popen(command, stdout=subprocess.PIPE)
    return interface


def autoSilenceCommand(command, silent=False, verbose=False):
    if not silent:
        output = process_command(command, stdout=sys.stdout, stderr=sys.stderr, tee=verbose, shell=(os.name != "nt"))
    else:
        devNull = open(os.devnull, "w")
        output = process_command(command, stdout=devNull, stderr=devNull, tee=False, shell=(os.name != "nt"))
        devNull.close()
    return output


def tee_or_return_output(condition, args):
    if condition:
        out = tee_output(args)
    else:
        out = return_output(args)
    out = out.strip()
    return out


def checkCommandExists(command):
    try:
        autoSilenceCommand(command, silent=True, verbose=False)
        return True
    except FileNotFoundError as _:
        return False
