from LMI import LTF
from .Indexing import index_python_files
import importlib
import inspect
import os


def run_all_tests():
    test_runner = LTF.TestsRunner()
    _, modules, _ = index_python_files("tests/", full=True)
    for module in modules:
        module = modules[module]["path"]
        module = os.path.normpath(module)
        to_import = (module.replace("/", ".").replace("\\", ".")
                     if ".py" not in module else
                     module.replace(".py", "").replace("/", ".").replace("\\", "."))
        importlib.invalidate_caches()
        imported_module = importlib.import_module(to_import)
        for _, obj in inspect.getmembers(imported_module):
            if inspect.isclass(obj) and obj.__module__ == to_import:
                if issubclass(obj, LTF.Tests.LTFTest):
                    test_runner.add_LTF_test(obj)
    test_runner.runAll()
    breakdown = LTF.Formatters.PercentageShort(test_runner.statistics)
    breakdown.show()
