import sympy

from ignition.dsl.riemann.language import *

def test_construction():
    """Test construction of Riemann expressions"""
    q = Conserved('q')
    h, uh = q.fields(['h', 'uh'])
    assert(h == Field('h'))
    assert(uh == Field('uh'))
    g = Constant('g')
    u = uh / h
    expr = u * uh + .5 * g * h ** 2
    assert(str(expr) == '0.5*g*h**2 + uh**2/h')
    print q.jacobian([uh, u*uh + .5*g*h**2])
    print  sympy.Matrix([[ 0, 1], [g*h - uh**2/h**2, 2*uh/h]])

    assert(q.jacobian([uh, u*uh + .5*g*h**2]) == \
           sympy.Matrix([[ 0, 1], [1.0*g*h - uh**2/h**2, 2*uh/h]]))

