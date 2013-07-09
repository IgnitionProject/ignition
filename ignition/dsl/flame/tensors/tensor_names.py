"""Module for manipulating tensor names according to Householder notation"""

RM_2_GREEK = {"a":"alpha", "b":"beta", "c":"gamma", "d":"delta",
            "e":"epsilon", "h":"eta", "i":"iota", "k":"kappa", "l":"lambda",
            "m":"mu", "n":"nu", "o":"omicron", "p":"pi", "r":"rho",
            "s":"sigma", "t":"tau", "u":"upsilon", "x":"chi", "z":"zeta"}
GREEK_ALPHA = ["theta", "xi", "phi", "psi", "omega"] + RM_2_GREEK.values()
RM_ALPHA = []

LOWER_TOK = '_'
UPPER_TOK = '^'
TRANS_TOK = 'T'
HAT_TOK = 'H'
INV_TOK = '-'
UP_TOKS = [TRANS_TOK, HAT_TOK, INV_TOK]


def split_name (name):
    """Returns base, lower, upper strings of name"""
    def _find (n, s):
        idx = n.find(s)
        return idx if idx > 0 else len(n)

    base_end = min(map(lambda x: _find(name, x), [LOWER_TOK, UPPER_TOK]))
    low_start = _find(name, LOWER_TOK)
    up_start = _find(name, UPPER_TOK)
    low_end = up_start if up_start > low_start else len(name)
    up_end = low_start if up_start < low_start else len(name)
    base = name[:base_end]
    low = name[low_start:low_end].strip(LOWER_TOK + '{' + '}')
    up = name[up_start:up_end].strip(UPPER_TOK + '{' + '}')
    return base, low, up

def join_name (name, lower, upper, latex=False):
    """Returns name string with upper and lower indices.
    
    >>> join_name("A", "0", "1")
    A_0^1
    >>> join_name("A", "bl", "2")
    A_bl^2
    >>> join_name("A", "bl", "2", latex=True)
    A_{bl}^2
    """
    ret_val = name
    if lower:
        ret_val += LOWER_TOK
        if latex and len(lower) > 1:
            ret_val += '{' + lower + '}'
        else:
            ret_val += lower
    if upper:
        ret_val += UPPER_TOK
        if latex and len(upper) > 1:
            ret_val += '{' + upper + '}'
        else:
            ret_val += upper
    return ret_val

def add_idx (name, idx, latex=False):
    """Returns a name with an added index.
    
    >>> add_idx("a", "r")
    "a[r]"
    >>> add_idx("a_0^2", "r")
    "a[r]_0^2"
    >>> add_idx("a[r]", "n")
    "a[r][n]"
    >>> add_idx("a", 3)
    "a[3]"
    >>> add_idx("a_02", "delta", latex=True)
    "a[\delta]_{02}
    """
    b, l, u = split_name(name)
    b = b + "[" + str(idx) + "]"
    return join_name(b, l, u, latex)

def to_latex(name):
    """Returns name for latex printing.
    
    >>> to_latex("A_01^T")
    'A_{01}^T'
    >>> to_latex("alpha")
    '\\alpha'
    """
    n, l, u = split_name(name)
    if n in GREEK_ALPHA:
        n = '\\' + n
    return join_name(n, l, u, latex=True)

def base (name):
    return split_name(name)[0]

def lower (name):
    return split_name(name)[1]

def upper (name):
    return split_name(name)[2]

def add_upper_ind (name, ind):
    base, l, u = split_name(name)
    if ind in u:
        return name
    u += ind
    return join_name(base, l, ''.join(sorted(u)))

def set_upper_ind (name, ind):
    base, l, _ = split_name(name)
    return join_name(base, l, ind)

def add_lower_ind (name, ind):
    base, l, u = split_name(name)
    if ind in l:
        return name
    l += ind
    return join_name(base, ''.join(sorted(l)), u)

def set_lower_ind (name, ind):
    base, _, u = split_name(name)
    return join_name(base, ind, ''.join(sorted(u)))

def transpose_name (name):
    return add_upper_ind(name, TRANS_TOK)

def hat_name (name):
    return add_upper_ind(name, HAT_TOK)

def inv_name (name):
    return add_upper_ind(name, INV_TOK)

def householder_name (name, rank):
    """Returns if the name conforms to Householder notation.
    
    >>> householder_name('A_1', 2)
    True
    >>> householder_name('foobar', 1)
    False
    """
    base, _, _ = split_name(name)
    if base in ['0', '1']:
        return True
    elif rank == 0:
        if base in GREEK_ALPHA:
            return True
    elif rank == 1:
        if len(base) == 1 and base.isalpha() and base.islower():
            return True
    elif rank == 2:
        if len(base) == 1 and base.isupper() and base.isalpha():
            return True
    return False

def convert_name (name, rank):
    """Converts a Householder name to a specific rank. 
    
    Will return non-Householder names unchanged.
    
    >>> convert_name("A", 1)
    'a'
    >>> convert_name("alpha_01", 2)
    'A_01'
    >>> convert_name("foo_bar", 1)
    'foo_bar'
    """
    name_rank = rank_from_name(name)
    if name_rank == rank:
        return name
    if not householder_name(name, name_rank):
        return name

    base, low, up = split_name(name)
    if base[0] in ['0', '1']:
        return name
    elif name_rank == 2:
        r_1 = join_name(base.lower(), low, up)
        if rank == 1:
            return r_1
        elif rank == 0:
                return convert_name(r_1, 0)

    elif name_rank == 1:
        if rank == 2:
            return join_name(base.upper(), low, up)
        if rank == 0:
            sca_name = RM_2_GREEK.get(base, None)
            if sca_name:
                return join_name(sca_name, low, up)
            else:
                return join_name("s" + base, low, up)
    elif name_rank == 0:
        alpha_name = None
        if base[0] == 's':
            alpha_name = base[1:]
        else:
            for k, v in RM_2_GREEK.iteritems():
                if v == base:
                    alpha_name = k
                    break
        if alpha_name:
            r_1 = join_name(alpha_name, low, up)
            if rank == 2:
                return convert_name(r_1, 2)
            elif rank == 1:
                return r_1
    raise ValueError("Unable to convert name: %s." % name)

def rank_from_name (name):
    base, _, _ = split_name(name)
    if len(base) == 1 and base.isalpha():
        if base.isupper():
            return 2
        if base.islower():
            return 1
    if base in GREEK_ALPHA:
        return 0
    return None

