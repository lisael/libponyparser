from ponyparser.ast.nodes import FunMethod, IdNode, ParamsNode, Nominal, SeqNode, StringNode


def validate_ast(ast, expected_code):
    assert ast.pretty_pony() == expected_code

def test_method():
    ast = FunMethod(
        annotations = [
            IdNode(id="annot1"),
            IdNode(id="annot2")
        ],
        id=IdNode(id="my_function"),
        params=ParamsNode(params=[]),
        return_type=Nominal(id=IdNode(id="String")),
        body=SeqNode(seq=[
            StringNode(value='"Hi!"')
        ])
    )
    validate_ast(ast,
    r'''fun \annot1, annot2\ my_function(): String =>
  "Hi!"
''')
