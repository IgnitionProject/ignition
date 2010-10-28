"""Several solvers for overdetermined tensor systems."""

from copy import copy
from sympy import expand, S
from sympy.utilities.iterables import postorder_traversal

from tensors import solve_vec_eqn
from ignition.utils.iterators import UpdatingPermutationIterator

DEBUG = False

def get_eqns_unk (eqns, knowns):
    """Returns the list of unknowns, given the knowns, from a list of equations"""
    if not isinstance(eqns, (list, tuple)):
        eqns = [eqns]
    atoms = reduce(lambda acc, eqn: acc.union(eqn.atoms()), eqns, set())
    return filter(lambda x: not x.is_Number, atoms - set(knowns))

def forward_solve(eqns, knowns, branching=False):
    """Returns a dict of unknowns:solutions from a simple backward solve.
    
    Does a simple backward solver for a list of eqn given a list of unknowns. 
    Each equation should be an expression that equals zero.  If an unknown is 
    not solved for, then its entry in the solution dict will be None.
    
     
    >>> q, r, s = map(lambda x: Tensor(x, rank=1), 'qrs')
    >>> delta = Tensor('delta', rank=0)
    >>> eqn1 = s + q
    >>> eqn2 = delta * r - q
    >>> forward_solve([eqn1, eqn2], [delta, r])
    {q: delta*r, s: -q}

    Will raise same exceptions as solve_vec_eqn.
    """
    sol_dict = {}
    unsolved = copy(eqns)
    unknowns = get_eqns_unk(unsolved, knowns)

    for atom in unknowns:
        sol_dict[atom] = None

    while True:
        solved = []
        if branching:
            sol_unks = []
        for eqn in unsolved:
            eqn_unk = get_eqns_unk(eqn, eqn.atoms() - set(unknowns))
            if len(eqn_unk) > 1:
                continue
            elif len(eqn_unk) == 0:
                solved.append(eqn)
                continue
            eqn_unk = eqn_unk.pop()
            try:
                if DEBUG:
                    print "solving eqn", eqn, "for", eqn_unk
                try:
                    sol = solve_vec_eqn(eqn, eqn_unk)
                except RuntimeError as inst:
                    print "=" * 80
                    print inst
                    print "Runtime error: forward_solve:"
                    print "  solve_vec_eqn( " + str(eqn) + ", " + str(eqn_unk) + " )"
                    print "=" * 80
                    raise
                if DEBUG:
                    print "given solution", sol
                if branching:
                    sol_unks.append(eqn_unk)
                else:
                    unknowns.remove(eqn_unk)
                solved.append(eqn)
                if branching:
                    if sol_dict[eqn_unk] is None:
                        sol_dict[eqn_unk] = [sol]
                    else:
                        sol_dict[eqn_unk].append(sol)
                else:
                    sol_dict[eqn_unk] = expand(sol)
            except Exception as inst:
                if DEBUG:
                    print "could not solve", eqn, "for", eqn_unk
                    print inst
        if len(solved) == 0 or len(unknowns) == 0:
            if DEBUG:
                print "Exiting forward_solve with"
                print "  solved:", solved
                print "  unknowns:", unknowns
            return sol_dict
        else:
            map(lambda x: unsolved.remove(x), solved)
            if branching:
                map(lambda x: unknowns.remove(x), sol_unks)

def get_solved (sol_dict):
    """Returns the solved variables of a solution dictionary"""
    return filter(lambda k: sol_dict[k] is not None, sol_dict)

def is_solved (sol_dict):
    """Returns if all variables in the solution dict are solved"""
    return reduce(lambda acc, k: acc and sol_dict[k] is not None, sol_dict,
                  True)

def update_sol_dict_unk_sol (sol_dict, unknowns, solved, curr_dict):
    """Upadates the solution dict, unknown list and solved list based on 
    given solution dict (curr_dict)"""
    newly_solved = get_solved(curr_dict)
    if len(newly_solved) == 0:
        return newly_solved
    if DEBUG:
        print "Updating newly_solved:", newly_solved
    sol_dict.update(curr_dict)
    map(lambda k: unknowns.remove(k), newly_solved)
    solved.extend(newly_solved)
    return newly_solved

def print_sols(sol, sol_dict):
    """Simple printer for solutions"""
    for k in sol:
        print "    " + str(k) + "=" + str(sol_dict[k])

def add_new_eqns (add_vars, all_eqns, sol_dict):
    """Substitutes solved values into equations and adds them to the list of 
    equations"""
    for knwn in add_vars:
        for eqn in all_eqns:
            if knwn in eqn:
                if DEBUG:
                    print "substituting:", knwn, "=", sol_dict[knwn], "in", eqn
                new_eqn = expand(eqn.subs(knwn, sol_dict[knwn]))
                if new_eqn == S(0): continue
                all_eqns.append(new_eqn)
                if DEBUG:
                    print "Added", new_eqn


def assump_solve(eqns, knowns, assumps=None):
    """An aggressive solver for list of eqns and given knowns.
    
    Similar to forward_solve, but will iteratively update equations based on given
    solutions by assuming an unknown is known. 
    
    >>> q, r, s = map(lambda x: Tensor(x, rank=1), 'qrs')
    >>> s_t = Transpose(s)
    >>> delta = Tensor('delta', rank=0)
    >>> eqn1 = r - s - q * delta
    >>> eqn2 = s_t * r
    >>> assump_solve([eqn1, eqn2], [s, q])
    {delta: -(T(s)*s)/(T(s)*q), r: delta*q + s}
    
    Should not raise any exceptions, but may return a solution dict with
    unsolved variables.
    """
    # See what we can solve first
    global DEBUG

    all_eqns = map(expand, eqns)
    ret_dict = {}
    unknowns = get_eqns_unk(eqns, knowns)
    solved = []

    if assumps is None:
        assumps = []

    num_x_explode = 1
    while True:
        if DEBUG:
            print "Entering iteration with ret_dict and all_eqns:"
            print ret_dict
            print all_eqns
            print unknowns
            print solved

        newly_solved = []

        # First solve without assumptions:
        curr_dict = forward_solve(all_eqns, knowns + solved)
        newly_solved = update_sol_dict_unk_sol(ret_dict, unknowns, solved, curr_dict)
        if DEBUG and len(newly_solved) > 0:
            print "Solved without assumptions:"
            print_sols(newly_solved, curr_dict)

        # Next try assuming some things are known then solve
        if len(newly_solved) == 0:
            ordered_assumps = [a for a in assumps if a in unknowns]
            ordered_assumps += [a for a in unknowns if a not in assumps]
            for unk in ordered_assumps:
            #assume unk is knw
                curr_dict = forward_solve(eqns, knowns + solved + [unk])
                newly_solved = update_sol_dict_unk_sol(ret_dict, unknowns, solved, curr_dict)
                if len(newly_solved) > 0:
                    if DEBUG:
                        print "Assuming " + str(unk) + " solved: "
                        print_sols(newly_solved, ret_dict)
                    break

        # If we didn't get any new solutions, we try to explode the space or we quit
        if len(newly_solved) == 0:
            if num_x_explode <= 0:
                if DEBUG:
                    print "Stopping because len(newly_solved) == 0, still don't know:", unknowns
                break
            num_x_explode -= 1
            if DEBUG:
                print "Exploding the space of equations by subing everything"
            add_new_eqns(filter(lambda k: ret_dict[k] is not None, ret_dict),
                         all_eqns, ret_dict)

        # Substitute new values into equations and add them to the set of eqns        
        add_new_eqns(newly_solved, all_eqns, ret_dict)
        # If we solved all unknowns stop
        if len(unknowns) == 0:
            if DEBUG:
                print "Stopping because len(unknowns) == 0"
            break

    return ret_dict

def build_assump_stack (eqns, knowns, levels= -1):
    unknowns = get_eqns_unk(eqns, knowns)
    sol_dict = forward_solve(eqns, knowns)
    solved = get_solved(sol_dict)

    if levels == -1: levels = len(unknowns)
    assump_stack = [ [var] for var in set(unknowns) - set(solved)]
    complete_assump = []
    level = 1
    while level < levels and assump_stack:
#        print "assump_stack:", assump_stack
        level_assumps = []
        for assump in assump_stack:
#            print "assump:", assump
            sol_dict = forward_solve(eqns, knowns + assump)
            solved = get_solved(sol_dict)
#            print "solved:", solved
            free_vars = set(unknowns) - set(solved) - set(assump)
#            print "free_vars:", free_vars
            if len(free_vars) > 0:
                for unk in free_vars:
                    level_assumps.append(assump + [unk])
            else:
                level_assumps.append(assump)
#        print "level_assumps:", level_assumps
        assump_stack = []
        for i in xrange(len(level_assumps)):
            if len(level_assumps[i]) < level:
                complete_assump.append(level_assumps[i])
            else:
                assump_stack.append(level_assumps[i])
        level += 1
    return complete_assump + assump_stack

def branching_assump_solve(eqns, knowns, levels= -1):
    """Returns all unique solutions discovered by assuming different unknowns
    and branching to see if different solutions occur.
    
    See also: assump_solve    
    """
    print "Building assumption stacks"
    assump_stack = build_assump_stack(eqns, knowns, levels)
    print "Got %d assumption stacks" % len(assump_stack)
    print "Solving for each assumption"
    sol_dicts = map(lambda assumps: assump_solve(eqns, knowns, assumps),
                    assump_stack)
    print "Done solving, filtering for unique sol_dicts"
    sol_dicts = filter(is_solved, sol_dicts)
    unique_dicts = []
    for sol_dict in sol_dicts:
        if not sol_dict in unique_dicts:
            unique_dicts.append(sol_dict)
    return unique_dicts


def backward_sub(eqns, knowns, unknowns=None, multiple_sols=False, sub_all=False):
    if unknowns is None:
        unknowns = []
    unknowns = unknowns + \
        [u for u in get_eqns_unk(eqns, knowns) if u not in unknowns]

    sol_dict = {}
    for unk in unknowns:
        if multiple_sols:
            sol_dict[unk] = set([])
        else:
            sol_dict[unk] = None

    all_eqns = copy(eqns)
    for n, unk in enumerate(unknowns):
        if DEBUG:
            print "Searching for unk:", unk
        for eqn in all_eqns:
            sol = None
#            print "eqn:", eqn, "eqn.atoms():", eqn.atoms(), "eqn.atoms().intersection(unknowns[n:1]):", eqn.atoms().intersection(unknowns[n:1])
            if  unk in eqn:
                try:
                    sol = solve_vec_eqn(eqn, unk)
                except RuntimeError as inst:
                    print "=" * 80
                    print inst
                    print "Caught Runtime error: backward_sub"
                    print "  solve_vec_eqn( " + str(eqn) + ", " + str(unk) + " )"
                    print "=" * 80
                except Exception as inst:
                    if DEBUG:
                        print "could not solve", eqn, "for", unk
                        print inst
                if sol is not None:
                    if multiple_sols:
                        sol_dict[unk].add(sol)
                    else:
                        sol_dict[unk] = sol
                        break
        if sol_dict[unk] is None or (multiple_sols and len(sol_dict[unk]) == 0):
            return (None, unk)
        else:
            new_eqns = []
            for eqn in all_eqns:
                if multiple_sols:
                    sols = sol_dict[unk]
                else:
                    sols = [sol_dict[unk]]
                new_eqns.extend(map(lambda sol: expand(eqn.subs(unk, sol)),
                                    sols))
            new_eqns = filter(lambda s: s != S(0), set(new_eqns))
            if sub_all:
                all_eqns = new_eqns
            else:
                all_eqns.extend(new_eqns)
    return (sol_dict, None)

def all_back_sub(eqns, knowns, levels= -1, multiple_sols=False, sub_all=True):
    unks = get_eqns_unk(eqns, knowns)
    ord_unk_iter = UpdatingPermutationIterator(unks,
                                       levels if levels != -1 else len(unks))
    sols = []
    print "Searching a possible %d orders" % len(list(ord_unk_iter))
    ord_unk_iter.reset()
    num_tested = 0
    for ord_unks in ord_unk_iter:
        print "Testing order:", ord_unks
        num_tested += 1
        sol_dict, failed_var = backward_sub(eqns, knowns, ord_unks,
                                            multiple_sols, sub_all)
#        print "  result:", sol_dict, failed_var
        if sol_dict is None:
            if failed_var in ord_unks:
                ord_unk_iter.bad_pos(ord_unks.index(failed_var))
        else:
            sols.append((sol_dict, ord_unks))
    print "Tested %d orders" % num_tested
    print "Filtering for unique solutions"
    uniq_sols = []
    for sol_dict, ord_unks in sols:
        if len(filter(lambda x: x[0] == sol_dict, uniq_sols)) == 0:
            uniq_sols.append((sol_dict, ord_unks))
    print "Found %d unique solutions" % len(uniq_sols)
    uniq_sols.sort(key=lambda s: sum([len(list(postorder_traversal(v))) \
                                      for k, v in s[0].iteritems()]))
    return uniq_sols
