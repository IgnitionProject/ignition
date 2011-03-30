"""Tools for manipulating strings of code"""

def indent_code (code_str, indent):
    """Indent a snippet of code with indent number of spaces"""
    if indent == 0:
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
