import pkg_resources

isJPypeInstalled = True if pkg_resources.working_set.by_key.get("jpype1") is not None else False

__all__ = ["JavaCompiler", "LuciferJVM"]

if isJPypeInstalled:
    print("Jpype is installed enabling LMI.Java extension!")
    from .JavaCompiler import javaCompiler
    from .LuciferJVM import luciferJVM

    print("Enabled LMI.Java extension.")
