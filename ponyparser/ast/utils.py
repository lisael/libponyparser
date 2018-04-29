from .visitor import Visitor
from .nodes import ModuleNode, PackageNode



class _RegisterParents(Visitor):
    def visit(self, node):
        if isinstance(node, (ModuleNode, PackageNode)):
            if not hasattr(node, "parent"):
                node.parent = None
        for child in node.iter_children():
            child.parent = node
            self.visit(child)


def register_parents(node):
    """
    Recursively add the parent node as `parent` attribute.
    """
    _RegisterParents().visit(node)
