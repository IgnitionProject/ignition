from sympy import *
import pprint


from ignition import *
from ignition.dsl.flame.tensors.basic_operators import add_invertible

su_12, delta_11 = map(lambda x: Tensor(x, 0), ["su_12", "delta_11"])
p_1, p_2, r_1, r_2, x_1, x_2, u_02 = \
    map(lambda x: Tensor(x, 1), ["p_1", "p_2", "r_1", "r_2", "x_1", "x_2", "u_02"])
A, P_0 = map(lambda x: Tensor(x, 2), ["A", "P_0"])

add_invertible(T(P_0) * A * P_0)
add_invertible(T(P_0) * A ** 2 * P_0)

sols_tups = \
    [({ p_2: P_0 * u_02 + su_12 * p_1 + r_2,
        r_2:-(-delta_11 * A * p_1 + r_1),
        u_02:-((T(P_0) * A * P_0) ** -1) * T(P_0) * A * r_2,
        x_2:-(-delta_11 * p_1 + x_1),
        delta_11: (T(r_1) * r_1) * ((T(r_1) * A * p_1) ** -1),
        su_12: (-(T(p_1) * A * P_0 * u_02) - (T(p_1) * A * r_2)) * ((T(p_1) * A * p_1) ** -1)},
       [p_2, su_12, u_02, x_2, r_2, delta_11]),
    ({ p_2: P_0 * u_02 + su_12 * p_1 + r_2,
       r_2:-(-delta_11 * A * p_1 + r_1),
       u_02:-((T(P_0) * A * P_0) ** -1) * T(P_0) * A * r_2,
       x_2:-(-delta_11 * p_1 + x_1),
       delta_11: (T(r_1) * r_1) * ((T(r_1) * A * p_1) ** -1),
       su_12: (-(T(p_1) * A * r_2) + (T(p_1) * A * P_0 * ((T(P_0) * A * P_0) ** -1) * T(P_0) * A * r_2)) * ((T(p_1) * A * p_1) ** -1)},
     [p_2, x_2, u_02, su_12, r_2, delta_11]),
    ({ p_2: P_0 * u_02 + su_12 * p_1 + r_2,
       r_2:-(-delta_11 * A * p_1 + r_1),
       u_02: ((T(P_0) * A * P_0) ** -1) * (T(P_0) * A * r_1 - delta_11 * T(P_0) * A ** 2 * p_1),
       x_2:-(-delta_11 * p_1 + x_1),
       delta_11: (T(r_1) * r_1) * ((T(r_1) * A * p_1) ** -1),
       su_12: (-(T(p_1) * A * P_0 * u_02) - (T(p_1) * A * r_2)) * ((T(p_1) * A * p_1) ** -1)},
     [p_2, su_12, r_2, x_2, u_02, delta_11]),
     ]

print "-" * 80
print "Without CSE"
print "-" * 80
for d, ord in sols_tups:
    for v,e in d.iteritems():
        print pprint.pformat("%s = %s" % (v, e), 0, 80)
    print "order:", pprint.pformat(list(reversed(ord)), 0, 80)
    print "=" * 80

print "-" * 80
print "Just call CSE"
print "-" * 80
for d, ord in sols_tups:
    new_sym, new_exprs = cse(d.values())
    print pprint.pformat(new_sym, 0, 80)
    for v,e in zip(d.keys(),new_exprs):
        print pprint.pformat("%s = %s" % (v, e), 0, 80)
    print "order:", pprint.pformat(list(reversed(ord)), 0, 80)
    print "=" * 80

print "-" * 80
print "Sub first then call CSE"
print "-" * 80

for d, ord in sols_tups:
    exprs = []
    for k, v in d.iteritems():
        for k_sub, v_sub in d.iteritems():
            if k != k_sub:
                nv = v.subs(v_sub, k_sub)
        exprs.append(nv)
    new_sym, new_exprs = cse(exprs)
    print pprint.pformat(new_sym, 0, 80)
    for v,e in zip(d.keys(),new_exprs):
        print pprint.pformat("%s = %s" % (v, e), 0, 80)
    print "order:", pprint.pformat(list(reversed(ord)), 0, 80)
    print "=" * 80



