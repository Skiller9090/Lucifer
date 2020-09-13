import subprocess
import sys


def return_output(command):
    all_output = process_command(command, stdout=subprocess.PIPE)
    return all_output


def tee_output(command, stdout=sys.stdout):
    tee_out = process_command(command, stdout, tee=True)
    return tee_out


def process_command(command, stdout, tee=False):
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
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
