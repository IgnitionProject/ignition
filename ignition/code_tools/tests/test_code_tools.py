from ignition.code_tools import comment_code, indent_code

def test_comment_code ():
    code = "This is \na mulitiline\ncomment"
    line_commented_code = '// This is\n// a mulitiline\n// comment\n'
    block_commented_code = "/*\nThis is \na mulitiline\ncomment\n*/"
    assert(comment_code(code, line_comment="//") == line_commented_code)
    assert(comment_code(code, block_comment=("/*", "*/")) == block_commented_code)
    assert(comment_code("",line_comment="//") == "")

def test_indent_code ():
    code = "python\nrequires\nfour\nspaces"
    indented_code = "    python\n    requires\n    four\n    spaces"
    assert(indent_code(code, 4) == indented_code)
    assert(indent_code("",4) == "")
    assert(indent_code("foobar",0) == "foobar")
