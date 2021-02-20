from .LuciferJVM import luciferJVM
from ...Command import process_command
import os
import sys
import shutil
import re


class Compiler:
    def __init__(self):
        self.luciferJVM = luciferJVM

    def javaToClass(self, topDirectory, filePath, out="build", verbose=False, multi=False, silent=False):
        if multi:
            relativePath = list(map(
                lambda x: os.path.relpath(os.path.abspath(os.path.join(topDirectory, x)), start=topDirectory),
                filePath))
        else:
            relativePath = os.path.relpath(os.path.abspath(os.path.join(topDirectory, filePath)), start=topDirectory)
        outPath = os.path.abspath(os.path.join(topDirectory, out))
        if not os.path.exists(outPath):
            os.makedirs(outPath, exist_ok=True)
        if multi:
            print(f"Compiling {len(relativePath)} files:")
            for file in relativePath:
                print(f"Compiling: {file}")
        else:
            print(f"Compiling : {relativePath}")
        command = f'"{self.luciferJVM.JavaJavacPath}" '
        if multi:
            for file in filePath:
                command += f'"{os.path.abspath(os.path.join(topDirectory, file))}" '
        else:
            command += f'"{os.path.abspath(os.path.join(topDirectory, filePath))}" '
        command += f'-d "{outPath}"'
        if verbose:
            command += " -verbose"
        if not silent:
            output = process_command(command, stdout=sys.stdout, tee=verbose)
        else:
            devNull = open(os.devnull, "w")
            output = process_command(command, stdout=devNull, tee=False)
            devNull.close()
        if "file not found" in output.lower():
            print(f"Can't find {filePath} to compile!")
            return
        if multi:
            print(f"Compiled {len(relativePath)} files")
        else:
            print(f"Compiled : {relativePath}")

    def jarBuild(self, topDirectory, outputName=None, buildDirectory="build", verbose=False, silent=False):
        if outputName is None:
            outputName = self.luciferJVM.luciferJarName
        print(f"Creating Jar: {outputName}")
        buildPath = os.path.abspath(os.path.join(topDirectory, buildDirectory))
        if not os.path.exists(buildPath):
            print(f"Can't find build directory: {buildPath}!")
            return
        outputPath = os.path.abspath(os.path.join(topDirectory, outputName))
        if os.path.exists(outputPath):
            os.remove(outputPath)
        args = "-cvf" if verbose else "-cf"
        command = f'"{self.luciferJVM.JavaJarPath}" '
        command += f'{args} {outputPath} '
        command += f'-C "{buildPath}" .'
        if not silent:
            process_command(command, stdout=sys.stdout, tee=verbose)
        else:
            devNull = open(os.devnull, "w")
            process_command(command, stdout=devNull, tee=False)
            devNull.close()
        print(f"Jar Created: {outputName}")

    @staticmethod
    def cleanDirectory(topDirectory, buildDirectory="build", verbose=True):
        if verbose:
            print(f"Cleaning: {topDirectory}")
        buildDirectoryPath = os.path.abspath(os.path.join(topDirectory, buildDirectory))
        if os.path.exists(buildDirectoryPath):
            shutil.rmtree(buildDirectoryPath)
        for dirPath, _, files in os.walk(os.path.abspath(topDirectory)):
            for filename in files:
                fName = os.path.join(dirPath, filename)
                if re.match('.*(.)(class)', fName):
                    os.remove(fName)
        if verbose:
            print(f"Cleaned: {topDirectory}")

    def directoryToClass(self, topDirectory, directoryPath, out="build", verbose=False, silent=False):
        toCompile = []
        for dirPath, _, files in os.walk(os.path.abspath(os.path.join(topDirectory, directoryPath))):
            for filename in files:
                fName = str(os.path.join(dirPath, filename))
                if re.match(".*(.)(java)", fName):
                    toCompile.append(fName)
        self.javaToClass(topDirectory, toCompile, out, verbose=verbose, multi=True, silent=silent)

    def createLuciferModuleJar(self):
        self.directoryToClass(
            self.luciferJVM.luciferJavaSrcPath, "",
            out=f"../builds/java-{self.luciferJVM.getJavaMajorVersion()}/classes", silent=True
        )
        compiler.jarBuild(f"./javaModules/builds/java-{self.luciferJVM.getJavaMajorVersion()}",
                          buildDirectory="classes", silent=True)

    def createLoadLuciferModuleJar(self):
        self.createLuciferModuleJar()
        self.luciferJVM.addLuciferJar()


compiler = Compiler()