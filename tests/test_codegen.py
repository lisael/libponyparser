import os
from pprint import pprint
from unittest import skipIf

from ponyparser.lexer import Lexer
from ponyparser.parser import Parser
from ponyparser.ast import nodes
from ponyparser.utils import find_pony_stdlib_path


parsers_cache = {}


def parse_code(data, **parser_opts):
    "parse the code and check that the generated pony code is the same."
    cache_key = tuple(parser_opts.items())
    if cache_key not in parsers_cache:
        parsers_cache[cache_key] = Parser(**parser_opts)
    parser = parsers_cache[cache_key]
    expected = parser.parse(data, lexer=Lexer())
    # pprint(expected.as_dict())
    generated = expected.as_pony()
    for (lineno, line) in enumerate(expected.pretty_pony().splitlines()):
        print("{:4}".format(lineno + 1) + " " + line.rstrip())
    result = parser.parse(generated, lexer=Lexer())
    assert(result.as_dict() == expected.as_dict())


def test_call():
    data = """
        env.out.print("hello world")
    """
    parse_code(data, start='term')


def test_call_full():
    data = """
        foo("hello world", 42 where pos=3)
    """
    parse_code(data, start='term')


def test_if():
    data = """
        if \likely\ true then false end
    """
    parse_code(data, start='if')


def test_if_else():
    data = """
        if true then false else "hello" end
    """
    parse_code(data, start='if')


def test_uniontype():
    data = '''
    type BackpressureAuth is (AmbientAuth | ApplyReleaseBackpressureAuth)
    '''
    parse_code(data, start="class_def")


def test_lambdatype():
    data = """
        {ref(A!): B ?} iso^
    """
    parse_code(data, start="lambdatype")


def test_lambdatype_2():
    data = '''
    {(A): String}
    '''
    parse_code(data, start="lambdatype")


def test_ifdef():
    data = """
        ifdef os_haiku then false else "hello" end
    """
    parse_code(data, start='ifdef')


# def test_ifdef_elseifdef():
#     data = """
#         ifdef os_haiku then
#             "lol"
#         elseif os_hurd then
#             "dont do drugs"
#         else
#             "dunno"
#         end
#     """
#     parse_code(data, start='ifdef')


PONY_FILE = None

@skipIf(os.environ.get("SHORT_TESTS", 0), "perform short tests")
def test_parse_stdlib():
    path = find_pony_stdlib_path()
    for root, _, files in os.walk(path):
        for ponysrc in [f for f in files if f.endswith(".pony")]:
            fname = os.path.join(root, ponysrc)
            if PONY_FILE is None or fname == PONY_FILE:
                with open(fname) as src:
                    print(fname)
                    data = src.read()
                    parse_code(data)
