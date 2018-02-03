[![Build Status](https://travis-ci.org/lisael/libponyparser.svg?branch=master)](https://travis-ci.org/lisael/libponyparser)
# Libponyparser
Ponylang parser and AST written in python3

# Usage

```
>>> from pprint import pprint
>>> from ponyparser.lexer import Lexer
>>> from ponyparser.parser import Parser
>>> src = """
... class Main
...   new create(env: Env) =>
...     env.out.write("Hello world")
... """
>>> parser = Parser()
>>> ast = parser.parse(src, lexer=Lexer())
```

This creates an AST object that can be mainipulated to query info about the pony code...

```
>>> ast.class_defs[0].members[0].params.params[0].id.id
'env'
```

Let's change the code a bit...

```
>>> ast.class_defs[0].members[0].params.params[0].id.id = 'e'
>>> ast.class_defs[0].members[0].body.seq[0].fun.first.first.id.id = 'e'
```

At the moment the ast nodes can't be visited and don't expose helper functions.
This explains the awkward syntax of the ast transformation.

We can now print the resulting code:

```
>>> print(ast.pretty_pony())


class Main
  new create(e: Env) =>
    e.out.write("Hello world")
  

```

The AST can be changed to a python dict for debugging purpose. I plan to implement
the backward transformation to allow easy JSON serialisation of a complete AST

```
>>> pprint(ast.as_dict())
{'class_defs': [{'annotations': []
                 'cap': None,
                 'docstring': None,
                 'id': {'id': 'Main', 'node_type': 'id'},
                 'members': [{'annotations': [],

...

 'uses': []}
```

It's now easy to write pony fragments:

```
>>> from ponyparser.ast.nodes import FunMethod, IdNode, ParamsNode, Nominal, SeqNode, StringNode
>>> meth = FunMethod(
...     annotations = [
...         IdNode(id="annot1"),
...         IdNode(id="annot2")
...     ],
...     id=IdNode(id="my_function"),
...     params=ParamsNode(params=[]),
...     return_type=Nominal(id=IdNode(id="String")),
...     body=SeqNode(seq=[
...         StringNode(value='"Hi!"')
...     ])
... )
>>> print(meth.pretty_pony())
fun \annot1, annot2\ my_function(): String =>
  "Hi!"
```
