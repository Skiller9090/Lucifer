from LMI.CLang import clang
import ctypes

compiler = clang.compiler

compiler.compileAuto(
    "external-modules/c/sources/Tests/cppTests.cpp"
)


dll = ctypes.CDLL("external-modules/c/builds/Tests/cppTests.dll")
dll.runTests()
