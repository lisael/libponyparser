"""
Package compilation hepers
"""
import os

from ponyparser.ast.nodes import PackageNode
from ponyparser.ast.utils import register_parents

from .module import compile_module

PACKAGES = {}


def get_package_from_path(path):
    try:
        return PACKAGES[path]
    except KeyError:
        PACKAGES[path] = PackageNode(path=path)
        return PACKAGES[path]


def package_modules_path(package):
    for file in os.listdir(package.path):
        fname = os.path.join(package.path, file)
        if file.endswith(".pony") and os.path.isfile(fname):
            yield fname


def compile_module_in_package(module_path, source=None):
    """
    Given a pony file, compile the module and create the enclosing
    package. The module is returned, with its package as parent
    """
    pkg = get_package_from_path(os.path.dirname(module_path))
    # just replace the old module
    mods = [m for m in pkg.modules if m.path == module_path]
    if mods:
        pkg.modules.remove(mods[0])
    mod = compile_module(module_path, source=source)
    register_parents(mod)
    pkg.modules.append(mod)
    mod.parent = pkg
    return mod


def compile_package(package):
    for path in package_modules_path(package):
        compile_module_in_package(path)
