"""
LMI (Lucifer Module Interface) allows you to easily interface with different parts of the application and system.

Modules:
    - Command: Allows you to run system commands with varying levels of output
"""
from . import Java
from .Interface import LuciferManagerInterface

LMI = LuciferManagerInterface.instance  # Late Definition
