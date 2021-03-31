from LMI import Java
from modules.Module import BaseModule


class Module(BaseModule):
    def run(self):
        if not Java.Run.isJPypeInstalled:
            print("You do not have 'jpype1' installed so you can not use lucifer java extensions!")
            return

        target_version_var = self.shell.vars.get("version", None)
        java_versions = Java.Installs.getVersions()

        if len(java_versions) < 1:
            print("No java installs, please install java first!")
            return

        if target_version_var is not None:
            for version in java_versions.keys():
                if java_versions[version]["version"].lower().startswith(target_version_var.lower()):
                    target_version = java_versions[version]
                    break
            else:
                print("Could not find the asked version defaulted to first found java instance.")
                target_version = java_versions[list(java_versions.keys())[0]]
        else:
            target_version = java_versions[list(java_versions.keys())[0]]

        print(f"Targeting java version: {target_version['version']}")

        if not Java.Run.luciferJVM.isJVMRunning:
            Java.Run.luciferJVM.setJavaPath(target_version["folderPath"])
            Java.Run.luciferJVM.startJVM()

        if not Java.Run.luciferJVM.isLuciferJarLoaded:
            Java.Run.javaCompiler.createLuciferModuleJar()
            print("Lucifer Module Jar Build Complete!")
            Java.Run.luciferJVM.addLuciferJar()
            Java.Run.luciferJVM.setSTDOUT()
            print("Loaded Lucifer Module Jar!")

        print("Started Java Automatically!")

    def set_vars(self):
        default_vars = {
        }
        return default_vars

    def get_description(self):
        desc = "Allows you to automatically select, build, start and load the lucifer JVM and Modules. Set the " \
               "variable 'version' to the target java version."
        return desc
