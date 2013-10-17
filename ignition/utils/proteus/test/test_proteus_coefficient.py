from ignition.dsl.sfl.language import *
from ignition.utils.proteus.coefficient import sfl_coefficient

def test_poisson():
    u = Variable('u', dim=3, space='L2')
    K = Constant('K', rank=0)

    strong_form = StrongForm(div(K * grad(u)))

    ### Just test for object creation for now.
    coefficient = sfl_coefficient(strong_form)


if __name__=="__main__":
    test_poisson()
