from ponyparser.ast.nodes import FunMethodNode, IdNode, ParamsNode, NominalNode, SeqNode, StringNode


def validate_ast(ast, expected_code):
    assert ast.pretty_pony() == expected_code


def test_method():
    ast = FunMethodNode(
        annotations=[
            "annot1",
            "annot2"
        ],
        id="my_function",
        params=[],
        return_type=NominalNode("String"),
        body=SeqNode(
            StringNode('"Hi!"')
        )
    )
    validate_ast(
        ast,
        r'''fun \annot1, annot2\ my_function(): String =>
  "Hi!"
''')
