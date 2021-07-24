import os
import sys
from importlib import import_module
from importlib.util import find_spec


def load_modules(module_name: str, prefix: str, class_name=""):
    module_name = "%s.%s" % (prefix, module_name)

    if not find_spec(module_name):
        print('%s: No such module.' % module_name, file=sys.stderr)
        exit(1)
    module = import_module(module_name)

    if len(class_name) == 0:
        class_name = module_name.rsplit('.', 1)[-1]

    return getattr(module, class_name)


def load_modules_from_dir(file, path: str):
    # we have filename = /path/filename.py, we
    # first we remove path
    # os.sep returns correct "/" per os
    class_name = file.rsplit(os.sep, 1)[-1]
    # we have class_name = filename.py
    # and now we remove extension
    class_name = class_name[:-3]
    # we have class_name = filename

    return load_modules(class_name, path)
