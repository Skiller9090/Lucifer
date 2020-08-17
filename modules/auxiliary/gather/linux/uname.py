from modules.Module import BaseModule
from subprocess import check_output


class Module(BaseModule):
    def get_uname(self):
        return check_output(["uname", "-a"]).decode()

    def run(self):
        print("Working!")