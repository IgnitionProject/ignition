from ignition.utils.code_obj import CodeObj, Statement, Variable


def create_sum_squares():
    """Returns a code dag for sum of squares."""
    code_dag = CodeObj()
    num_squares = Variable('N', var_type=int)
    sum_var = Variable('sum_var', var_type=int)
    sum_squares = code_dag.add_function('sum_squares', inputs=[num_squares])
    floop = sum_squares.add_for_loop(start=1, stop=num_squares + 1)
    s1 = Statement("*", floop.idx, floop.idx)
    floop.add_statement(Statement("+=", sum_var, s1))
    sum_squares.add_return(sum_var)
    return code_dag


def test_for_loop_sum_squares():
    """Test for creating \sum_{i=1}^N i*i"""
    create_sum_squares()  # Should raise exception if fails.
