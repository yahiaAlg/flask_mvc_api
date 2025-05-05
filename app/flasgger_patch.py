"""
Patch for flasgger to work with Python 3.12
"""
import importlib.util
import sys
import types

# Create a module to replace the deprecated 'imp' module
class ImpModule(types.ModuleType):
    @staticmethod
    def load_source(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

# Create a fake 'imp' module and add it to sys.modules
sys.modules['imp'] = ImpModule('imp')