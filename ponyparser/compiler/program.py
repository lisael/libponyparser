import os

from ponyparser.utils import find_pony_stdlib_path, is_package

from .package import compile_module_in_package, get_package_from_path
from .exceptions import PackageNotFound


class Program:
    def __init__(self, project_root=".", ponypath=None, stdlibpath=None):
        self.project_root = project_root
        stdlibpath = stdlibpath if stdlibpath else find_pony_stdlib_path()
        ponypath = ponypath if ponypath is not None else [project_root]
        self.ponypath = [stdlibpath] + ponypath
        self.pkgs = {}

    def resolve_package(self, pkgname):
        "return the package if found. Otherwise, return None"
        if pkgname not in self.pkgs:
            chunks = pkgname.split("/")
            for path in self.ponypath:
                full_path = os.path.join(path, *chunks)
                if is_package(full_path):
                    pkg = get_package_from_path(full_path)
                    pkg.name = pkgname
                    self.pkgs[pkgname] = pkg
                    return pkg
            # Don't cache if not found. It can be created in the
            # meantime.
            raise PackageNotFound(pkgname)
        else:
            pkg = self.pkgs[pkgname]
            if is_package(pkg.path):
                return pkg
            else:
                del self.pkgs[pkgname]
                raise PackageNotFound(pkgname)

    def compile_module(self, source_path, source=None):
        mod = compile_module_in_package(source_path, source)
        pkg = mod.parent
        pkg.name = self.findpkgname(pkg)
        if pkg.name is not None:
           self.pkgs[pkg.name] = pkg
        return mod

    def findpkgname(self, package):
        """
        Given a package, return the "use" name, or None if
        the package is not on the ponypath.
        """
        for path in self.ponypath:
            if package.path.startswith(path):
                return package.path[len(path):]
        return None



class StableProgram(Program):
    def __init__(self, project_root=".", stdlibpath=None):
        self.project_root = project_root
        stdlibpath = stdlibpath if stdlibpath else find_pony_stdlib_path()
        self.ponypath = [stdlibpath] + _get_ponypath()

    def _get_ponypath(self):
        return []


