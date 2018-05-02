"""
Exceptions in compilation process
"""


class CompilationError(Exception):
    """
    Base class for errors raised durring compilation
    """
    def __init__(self, node):
        super(CompilationError, self).__init__()
        self.node = node

    def position(self):
        """
        0-indexed (fname, line, col) position of the error
        """


class NameClash(CompilationError):
    """
    Raised when a symbol shadows another one
    """
    def __init__(self, key, shadowed, *args):
        super(NameClash, self).__init__(*args)
        self.key = key
        self.shadowed = shadowed


class PackageNotFound(CompilationError):
    """
    Raised if a package can't be found on PONYPATH
    """
