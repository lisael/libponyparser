"""
Add scopes to the AST
"""
from ponyparser.ast.visitor import Visitor
from .package import compile_package
from .exceptions import NameClash, PackageNotFound


class Scope(dict):
    """
    a recursive dict
    """
    def __init__(self, parent=None):
        super(Scope, self).__init__()
        self.parent = parent

    def __getitem__(self, key):
        try:
            super(Scope, self).__getitem__(key)
        except KeyError:
            if self.parent is not None:
                return self.parent[key]
            else:
                raise
        assert False, "unreachable"
        return None

    def __setitem__(self, key, value):
        try:
            shadowed = self[key]
        except KeyError:
            super(Scope, self).__setitem__(key, value)
        except Exception:
            raise
        else:
            raise NameClash(key, shadowed)


class ModuleScope(Scope):
    """
    Module scope are special because they must retain the local
    name of packages in case of named `use`s
    """
    def __init__(self, *args, **kwargs):
        super(ModuleScope, self).__init__(*args, **kwargs)
        self.pkgmap = {}


class ScopeProvider(Visitor):
    "Add scope to nodes"

    def visit_package(self, node):
        """
        Create the top level scope
        """
        scope = Scope()
        super(ScopeProvider, self).visit_children(node, scope=scope)

    def visit_module(self, node, scope):
        """
        Adds the module scope
        """
        node.scope = scope
        super(ScopeProvider, self).visit_children(node, scope=scope,
                                                  exclude=node.does_scope)
        scope = ModuleScope(scope)
        super(ScopeProvider, self).visit_children(node, scope=scope,
                                                  only=node.does_scope)

    # pylint: disable=keyword-arg-before-vararg,arguments-differ
    def visit_children(self, node, scope=None, only=None, exclude=None,
                       *args, **kwargs):
        """
        Adds a the scope to all children. Create a new one if needed
        """
        node.scope = scope
        if node.does_scope is not None:
            super(ScopeProvider, self).visit_children(node, scope=scope,
                                                      exclude=node.does_scope)
            scope = Scope(scope)
            super(ScopeProvider, self).visit_children(node, scope=scope,
                                                      only=node.does_scope)
        else:
            super(ScopeProvider, self).visit_children(node, scope)


def add_scopes(node):
    """
    Adds a scopes to a package.
    """
    spr = ScopeProvider()
    spr.visit(node)


class _ModuleExporter(Visitor):
    def __init__(self):
        self.exported = {}

    def visit_classdef(self, node):
        if not node.id.id.startswith("_"):
            self.exported[node.id.id] = node

    visit_actor = visit_classdef
    visit_type = visit_classdef
    visit_class = visit_classdef
    visit_interface = visit_classdef
    visit_trait = visit_classdef
    visit_primitive = visit_classdef
    visit_struct = visit_classdef


def export_package_symbols(pkg):
    exporter = _ModuleExporter()
    exporter.visit(pkg)
    return exporter.exported


class _SymbolResolver(Visitor):
    """
    Walk the AST, register names and resolve references.
    This must be run after the scopes are in places (using ScopeProvider or add_scopes)
    """
    def __init__(self, program):
        self.program = program
        self.errors = []

    def visit_module(self, node):
        for use in node.uses:
            try:
                pkg = self.program.resolve_package(use.package.strip('"'))
            except PackageNotFound as exc:
                self.errors = exc
                continue
            compile_package(pkg)
            symbols = export_package_symbols(pkg)
            if use.id:
                node.scope[use.id.id] = symbols
            else:
                node.scope.update(symbols)


def resolve_symbols(node, program):
    """
    Walk the AST, register names and resolve references.
    This must be run after the scopes are in places (using ScopeProvider or add_scopes)
    """
    res = _SymbolResolver(program)
    res.visit(node)
















