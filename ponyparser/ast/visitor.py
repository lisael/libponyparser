class Visitor:
    def visit(self, node, *args, **kwargs):
        name = node.__class__.__name__
        name = name.replace("Node", "")
        name = name.lower()
        name = "visit_%s" % name
        if hasattr(self, name):
            return getattr(self, name)(node, *args, **kwargs)
        else:
            return self.visit_children(node, *args, **kwargs)

    # pylint: disable=keyword-arg-before-vararg
    def visit_children(self, node, only=None, exclude=None, *args, **kwargs):
        for c in node.iter_children(only=only, exclude=exclude):
            self.visit(c, *args, **kwargs)
