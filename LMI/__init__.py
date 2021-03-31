"""
LMI (Lucifer Module Interface) allows you to easily interface with different parts of the application and system.

Modules:
    - Command: Allows you to run system commands with varying levels of output
    - Java: //
    - Networking: //
    - Reports: //
    - File: //
    - Interface: //
    - OS: //
    - Table: //
    - Utils: //
"""
from . import Java, Networking, Reports, Command, File, Interface, OS, Table, Utils
from .Interface import LuciferModuleInterfaceManager


__all__ = ["Java", "Networking", "Reports", "Command", "File", "Interface", "OS", "Table", "Utils", "LMI"]

LMI = LuciferModuleInterfaceManager.instance  # Late Definition
