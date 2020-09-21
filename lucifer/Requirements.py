from pkg_resources import DistributionNotFound, VersionConflict, require


def check_requirements():
    with open("requirements.txt", "r") as f:
        packages = f.read().split("\n")
    not_installed = []
    conflicting_versions = []
    for pkg in packages:
        try:
            require(pkg)
        except DistributionNotFound as e:
            not_installed.append(e.req)
        except VersionConflict as e:
            conflicting_versions.append((e.req, e.dist))

    if not_installed or conflicting_versions:
        if not_installed:
            print("The following packages are needed to be installed to run:")
            for pkg in not_installed:
                print(f"{pkg}")
        if conflicting_versions:
            print("The following packages have conflict errors:")
            for pkg in conflicting_versions:
                print(f"Current: {pkg[1]}, Needed: {pkg[0]}")
        print(f'Please install requirements.txt with:\n     pip install -r requirements.txt'
              f' {"--upgrade" if conflicting_versions else ""}')
        exit(1)
