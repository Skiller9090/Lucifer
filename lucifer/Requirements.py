import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict


def check_requirements():
    with open("requirements.txt", "r") as f:
        packages = f.read().split("\n")
    if len(packages) > 0:
        try:
            pkg_resources.require(packages)
        except DistributionNotFound as e:
            print(f'{e.req} is need for lucifer to run\nPlease install requirements.txt with:\n'
                  f'    pip install -r requirements.txt')
            exit(1)
