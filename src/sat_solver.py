
from __future__ import division
from __future__ import print_function
from collections import deque

verbose = False



def general_solve(expression):
    expression = remove_redundancies(expression)
    instance = SATInstance(expression)

    assignments = solve(instance, "recursive_sat", verbose)
    count = 0
    for assignment in assignments:
        if verbose:
            print('Found satisfying assignment #{}:'.format(count))
            print(instance.assignment_to_string(assignment))
        count += 1

    if count == 0 and verbose:
        print('No satisfying assignment exists.')

    return count

#expression should have been determined to be horn by this point
def horn_solve(expression):
    expression = remove_redundancies(expression)
    instance = SATInstance(expression)

    result = assign_all_true(instance, verbose)

    if result == False and verbose:
        print('No satisfying assignment exists.')
    return result

def assign_all_true(expression, verbose):
    n = len(expression.variables)
    watchlist = setup_watchlist(expression)
    if not watchlist:
        return ()
    assignment = [None] * n
    return final_horn_check(expression, watchlist, assignment, 0, verbose)

def final_horn_check(instance, watchlist, assignment, d, verbose):
    n = len(instance.variables)
    state = [0] * n

    while True:
        if d == n:
            d -= 1
            break
        # Let's try assigning a value to v. Here would be the place to insert
        # heuristics of which value to try first.
        tried_something = False
        for a in [1]:
            if (state[d] >> a) & 1 == 0:
                if verbose:
                    print('Trying {} = {}'.format(instance.variables[d], a))
                tried_something = True
                # Set the bit indicating a has been tried for d
                state[d] |= 1 << a
                assignment[d] = a
                if not update_watchlist(instance, watchlist, d << 1 | a, assignment, verbose):
                    assignment[d] = None
                else:
                    d += 1
                    break

        if not tried_something:
            if d == 0:
                # Can't backtrack further. No solutions.
                return False
            else:
                # Backtrack
                state[d] = 0
                assignment[d] = None
                d -= 1
    return True

#expression should be in 2-clause format
def two_SAT_solve(expression):
    expression = remove_redundancies(expression)
    instance = SATInstance(expression)

    result = assign_all_true(instance, verbose)

    if result == False and verbose:
        print('No satisfying assignment exists.')
    return result

#expression should be in N-clause format
def N_SAT_solve(expression):
    expression = remove_redundancies(expression)
    instance = SATInstance(expression)

    result = assign_all_true(instance, verbose)

    if result == False and verbose:
        print('No satisfying assignment exists.')
    return result

def remove_redundancies(expression):
    newlist = list()
    added_sets = list() #set used to eliminate order. ['a','b'] == ['b','a']
    for i in expression:
        if set(i) not in added_sets:
            newlist.append(i)
            added_sets.append(set(i))
    return newlist

def solve(instance, alg, verbose):
    """
    Returns a generator that generates all the satisfying assignments for a
    given SAT instance, using algorithm given by alg.
    """
    n = len(instance.variables)
    watchlist = setup_watchlist(instance)
    if not watchlist:
        return ()
    assignment = [None] * n
    return iter_solve(instance, watchlist, assignment, 0, verbose)

def recur_solve(instance, watchlist, assignment, d, verbose):
    """
    Recursively solve SAT by assigning to variables d, d+1, ..., n-1. Assumes
    variables 0, ..., d-1 are assigned so far. A generator for all the
    satisfying assignments is returned.
    """
    if d == len(instance.variables):
        yield assignment
        return

    for a in [0, 1]:
        if verbose:
            print('Trying {} = {}'.format(instance.variables[d], a))
        assignment[d] = a
        if update_watchlist(instance, watchlist, (d << 1) | a, assignment, verbose):
            for a in recur_solve(instance, watchlist, assignment, d + 1, verbose):
                yield a

    assignment[d] = None

def iter_solve(instance, watchlist, assignment, d, verbose): 
    """
    Iteratively solve SAT by assigning to variables d, d+1, ..., n-1. Assumes
    variables 0, ..., d-1 are assigned so far. A generator for the first found
    assignment is returned
    """

    # The state list wil keep track of what values for which variables
    # we have tried so far. A value of 0 means nothing has been tried yet,
    # a value of 1 means False has been tried but not True, 2 means True but
    # not False, and 3 means both have been tried.
    n = len(instance.variables)
    state = [0] * n

    while True:
        if d == n:
            yield assignment
            d -= 1
            break
        # Let's try assigning a value to v. Here would be the place to insert
        # heuristics of which value to try first.
        tried_something = False
        for a in [0, 1]:
            if (state[d] >> a) & 1 == 0:
                if verbose:
                    print('Trying {} = {}'.format(instance.variables[d], a))
                tried_something = True
                # Set the bit indicating a has been tried for d
                state[d] |= 1 << a
                assignment[d] = a
                if not update_watchlist(instance, watchlist, d << 1 | a, assignment, verbose):
                    assignment[d] = None
                else:
                    d += 1
                    break

        if not tried_something:
            if d == 0:
                # Can't backtrack further. No solutions.
                return
            else:
                # Backtrack
                state[d] = 0
                assignment[d] = None
                d -= 1

def dump_watchlist(instance, watchlist):
    print('Current watchlist:')
    for l, w in enumerate(watchlist):
        literal_string = instance.literal_to_string(l)
        clauses_string = ', '.join(instance.clause_to_string(c) for c in w)
        print('{}: {}'.format(literal_string, clauses_string))

def setup_watchlist(instance):
    watchlist = [deque() for __ in range(2 * len(instance.variables))]
    for clause in instance.clauses:
        # Make the clause watch its first literal
        watchlist[clause[0]].append(clause)
    return watchlist


def update_watchlist(instance, watchlist, false_literal, assignment, verbose):
    """
    Updates the watch list after literal 'false_literal' was just assigned
    False, by making any clause watching false_literal watch something else.
    Returns False it is impossible to do so, meaning a clause is contradicted
    by the current assignment.
    """
    while watchlist[false_literal]:
        clause = watchlist[false_literal][0]
        found_alternative = False
        for alternative in clause:
            v = alternative >> 1
            a = alternative & 1
            if assignment[v] is None or assignment[v] == a ^ 1:
                found_alternative = True
                del watchlist[false_literal][0]
                watchlist[alternative].append(clause)
                break

        if not found_alternative:
            if verbose:
                dump_watchlist(instance, watchlist)
                print('Current assignment: {}'.format(
                      instance.assignment_to_string(assignment)))
                print('Clause {} contradicted.'.format(
                      instance.clause_to_string(clause)))
            return False
    return True

class SATInstance(object):
    def parse_and_add_clause(self, single_clause):
        clause = []
        for literal in single_clause:
            negated = 1 if literal.startswith('!') else 0
            variable = literal[negated:]
            if variable not in self.variable_table:
                self.variable_table[variable] = len(self.variables)
                self.variables.append(variable)
            encoded_literal = self.variable_table[variable] << 1 | negated
            clause.append(encoded_literal)
        self.clauses.append(tuple(set(clause)))

    def __init__(self, expression):
        self.variables = []
        self.variable_table = dict()
        self.clauses = []
        for clause in expression:
            self.parse_and_add_clause(clause)

    def literal_to_string(self, literal):
        s = '!' if literal & 1 else ''
        return s + self.variables[literal >> 1]

    def clause_to_string(self, clause):
        return ' '.join(self.literal_to_string(l) for l in clause)

    def assignment_to_string(self, assignment, brief=False, starting_with=''):
        literals = []
        for a, v in ((a, v) for a, v in zip(assignment, self.variables)
                     if v.startswith(starting_with)):
            if a == 0 and not brief:
                literals.append('!' + v)
            elif a:
                literals.append(v)
        return ' '.join(literals)
