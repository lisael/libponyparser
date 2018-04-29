"""
Module compiler utils
"""
from ponyparser.parser import Parser
from ponyparser.lexer import Lexer

PARSERS_CACHE = {}


def compile_module(source_path=None, source=None, **kwargs):
    "Parse a module given a source_path or raw source"
    if source is None:
        if source_path is None:
            raise ValueError("A source or a filname must be provided")
        with open(source_path, 'r') as srcf:
            source = srcf.read()
    if not isinstance(source, str):
        try:
            source = source.read()
        except AttributeError:
            raise ValueError("source must be a string or a file like object")
    cache_key = tuple(kwargs.items())
    if cache_key not in PARSERS_CACHE:
        PARSERS_CACHE[cache_key] = Parser(**kwargs)
    parser = PARSERS_CACHE[cache_key]
    module = parser.parse(source, lexer=Lexer())
    module.path = source_path
    return module
