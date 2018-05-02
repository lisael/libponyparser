import os

from ponyparser.compiler.program import Program
from ponyparser.compiler.package import compile_package
from ponyparser.compiler.scope import add_scopes, resolve_symbols

from ponyparser.utils import find_pony_stdlib_path


HERE = os.path.dirname(os.path.abspath(__file__))


def test_program():
    prg = Program(project_root=os.path.join(HERE, "test_program"))
    collections = prg.resolve_package("collections")
    assert collections.path == os.path.join(find_pony_stdlib_path(), "collections")
    collections2 = prg.resolve_package("collections")
    assert collections2 is collections
    package_one = prg.resolve_package("package_one")
    assert package_one.path == os.path.join(HERE, "test_program", "package_one")


def test_program_compile():
    prg = Program(project_root=os.path.join(HERE, "test_program"))
    src = os.path.join(HERE, "test_program", "package_one", "main.pony")
    mod = prg.compile_module(src)
    package_one = prg.resolve_package("package_one")
    assert package_one is mod.parent
    assert mod in package_one.modules
    compile_package(package_one)
    assert mod not in package_one.modules

def test_scopes():
    prg = Program(project_root=os.path.join(HERE, "test_program"))
    package_one = prg.resolve_package("package_one")
    compile_package(package_one)
    add_scopes(package_one)
    # TODO: asserts on scopes

def test_symbol_resolver():
    prg = Program(project_root=os.path.join(HERE, "test_program"))
    package_one = prg.resolve_package("package_one")
    compile_package(package_one)
    add_scopes(package_one)
    errors = resolve_symbols(package_one, prg)
    import ipdb; ipdb.set_trace()
