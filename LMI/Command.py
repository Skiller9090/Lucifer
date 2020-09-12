import subprocess
import sys


def return_output(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    all_output = ""
    while True:
        output = process.stdout.readline().decode(sys.getfilesystemencoding(), "ignore")
        if output == '' and process.poll() is not None:
            break
        if output:
            all_output += output
    return all_output


def tee_output(command, stdout=sys.stdout):
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    all_output = ""
    while True:
        output = process.stdout.readline().decode(sys.getfilesystemencoding(), "ignore")
        if output == '' and process.poll() is not None:
            break
        if output:
            all_output += output
            stdout.write(output)
    return all_output


def run_command(command):
    subprocess.call(command, stdout=subprocess.PIPE)
    return True


def async_run_command(command):
    interface = subprocess.Popen(command, stdout=subprocess.PIPE)
    return interface
