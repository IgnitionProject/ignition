from ignition.dsl.flame.tensors.tensor_names import (convert_name,
    add_lower_ind, add_upper_ind, set_lower_ind, set_upper_ind, to_latex)

def test_convert_name():
    assert(convert_name("A", 2) == "A")
    assert(convert_name("A", 1) == "a")
    assert(convert_name("A", 0) == "alpha")
    assert(convert_name("a", 2) == "A")
    assert(convert_name("a", 1) == "a")
    assert(convert_name("a", 0) == "alpha")
    assert(convert_name("alpha", 2) == "A")
    assert(convert_name("alpha", 1) == "a")
    assert(convert_name("alpha", 0) == "alpha")
    assert(convert_name("A_TL", 2) == "A_TL")
    assert(convert_name("a^T", 2) == "A^T")
    assert(convert_name("alpha_01", 2) == "A_01")
    assert(convert_name("foo_bar", 1) == "foo_bar")

def test_inds():
    assert(set_upper_ind("A", "TL") == "A^TL")
    assert(set_upper_ind("A_01", "TL") == "A_01^TL")
    assert(set_upper_ind("A_TL^T", "TL") == "A_TL^TL")
    assert(set_lower_ind("A", "TL") == "A_TL")
    assert(set_lower_ind("A_01", "TL") == "A_TL")
    assert(set_lower_ind("A_TL^T", "TL") == "A_TL^T")

def test_to_latex():
    assert(to_latex("A_01^T") == "A_{01}^T")
    assert(to_latex("alpha") == "\\alpha")
