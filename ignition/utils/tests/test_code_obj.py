from ignition.utils.code_obj import CodeObj, Statement, Variable, FunctionNode, LoopNode


def create_sum_squares():
    """Returns a code dag for sum of squares."""
    num_squares = Variable('N', var_type="int")
    sum_var = Variable('sum_var', var_type="int")

    sum_squares = FunctionNode('sum_squares', ret_type="int", inputs=[num_squares], output=sum_var)
    sum_squares.add_object(sum_var)
    sum_squares.add_statement("=", sum_var, 0)
    floop = LoopNode(kind='for', init=1, test=num_squares + 1, inc=1)
    s1 = Statement("*", floop.idx, floop.idx)
    floop.add_statement("+=", sum_var, s1)
    sum_squares.add_object(floop)
    code_dag = CodeObj().add_object(sum_squares)
    return code_dag


def test_for_loop_sum_squares():
    """Test for creating \sum_{i=1}^N i*i"""
    create_sum_squares()  # Should raise exception if fails.
