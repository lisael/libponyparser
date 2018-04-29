class NameClash(Exception):
    """
    Raised when a symbol shadows another one
    """
    def __init__(self, key, shadowed):
        super(NameClash, self).__init__()
        self.key = key
        self.shadowed = shadowed

class PackageNotFound(Exception):
    """
    Raised if a package can't be found on PONYPATH
    """
