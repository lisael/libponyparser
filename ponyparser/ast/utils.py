from .visitor import Visitor


class _RegisterParents(Visitor):
    def visit(self, node):
        from .nodes import ModuleNode, PackageNode
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


class PositionFinder(Visitor):
    def __init__(self, lexpos):
        self.lexpos = lexpos
        self.result = None

    def visit(self, node):
        start, end = node.lexspan
        if start <= self.lexpos and self.lexpos <= end:
            self.result = node
            self.visit_children(node)


def node_at_lexpos(node, lexpos):
    finder = PositionFinder(lexpos)
    finder.visit(node)
    return finder.result
