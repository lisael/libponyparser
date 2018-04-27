class Visitor:
    def visit(self, node):
        name = node.__class__.__name__
        name = name.replace("Node", "")
        name = name.lower()
        name = "visit_%s" % name
        if hasattr(self, name):
            return getattr(self, name)(node)
        else:
            return self.visit_children(node)

    def visit_children(self, node):
        for c in node.iter_children():
            self.visit(c)
