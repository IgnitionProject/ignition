"""Tools for manipulating strings of code"""

def comment_code(code_str, line_comment=None, block_comment=None):
    """Adds comments to a snippet of code.

    If line_comment is a given string then each line is prepended with the
    line_comment string.

    If block_comment is a tuple of two strings (begin, end) the code str is
    surrounded by the strings.

    Example:

    >>> code = "This is \\na mulitiline\\ncomment"
    >>> print comment_code(code, line_comment="//")
    // This is
    // a mulitiline
    // comment
    >>> print comment_code(code, block_comment=("/*","*/")
    /*
    This is
    a mulitiline
    comment
    */

    """
    ret_code = code_str
    if code_str == "":
        return code_str
    if line_comment in [None, ""] and block_comment in [None,""]:
        raise ValueError("comment_code require a line_comment of block_comment")
    if line_comment:
        line_comment += " "
        ret_code = line_comment + \
                   line_comment.join(map(lambda line: line.rstrip()+'\n',
                                         code_str.splitlines()))
    elif block_comment:
        ret_code = block_comment[0] + "\n" + code_str + "\n" + block_comment[1]
    return ret_code

def indent_code(code_str, indent):
    """Indent a snippet of code with indent number of spaces"""
    if code_str == "" or indent == 0:
        return code_str
    if code_str[0] != '\n':
        code_str = ' ' * indent + code_str
    idx = code_str.find('\n')
    while (idx != -1  and idx < len(code_str) - 1):
        if code_str[idx + 1] not in ['\n']:
            code_str = code_str[:idx + 1] + ' ' * indent + code_str[idx + 1:]
            idx = code_str.find('\n', idx + 1)
        else:
            idx = code_str.find('\n', idx + 1)
    return code_str
