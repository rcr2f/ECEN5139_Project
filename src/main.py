

from optparse import OptionParser
import os
from cnf_types import CNF_Solver
import matplotlib.pyplot as plt
import operator





#get user input file for CNF expressions

#run generic sat solver on each

#run optimized sat solver on each

#compare results in pretty matplotlib
def get_input_arguments():
    parser = OptionParser()
    parser.add_option("-f", dest="cnf_file", default='cnf_expressions.txt', help="CNF expressions file")
    (options, args) = parser.parse_args()
    return vars(options)

if __name__ == '__main__':
    options = get_input_arguments()

    cnf_file = options["cnf_file"]
    solver = CNF_Solver(cnf_file)
    solver.general_solve_all()
    solver.optimized_solve_all()
    
    plt.plot(solver.timing_results)
    plt.title('General SAT results: overall time')
    plt.ylabel('General Solve Time')
    plt.xlabel('CNF Expressions')
    plt.show()

    plt.plot(solver.num_literals, solver.timing_results, 'ro')
    plt.title('General SAT results: Literals in expression')
    plt.ylabel('General Solve Time')
    plt.xlabel('Number of literals (a, b, c,...)')
    plt.show()

    plt.plot(solver.num_clauses, solver.timing_results, 'bo')
    plt.title('General SAT results: Clauses in expression')
    plt.ylabel('General Solve Time')
    plt.xlabel('Number of clauses per expression')
    plt.show()

    horn_times = solver.get_new_list(solver.horn_results, solver.horns)
    general_times_1 = solver.get_new_list(solver.timing_results, solver.horns)
    two_times = solver.get_new_list(solver.two_results, solver.twos)
    general_times_2 = solver.get_new_list(solver.timing_results, solver.twos) 
    N_times = solver.get_new_list(solver.N_results, solver.Ns)
    general_times_3 = solver.get_new_list(solver.timing_results, solver.Ns)

    horn_difference = map(operator.sub, general_times_1, horn_times)
    two_difference = map(operator.sub, general_times_2, two_times)
    N_difference = map(operator.sub, general_times_3, N_times)

    plt.plot(horn_difference,  'bo')
    plt.title('Horn Solve results')
    plt.ylabel('Difference in Solve Time')
    plt.xlabel('Expression')
    plt.show()

    plt.plot(two_difference,  'bo')
    plt.title('2-SAT results')
    plt.ylabel('Difference in Solve Time')
    plt.xlabel('Expression')
    plt.show()

    plt.plot(N_difference,  'bo')
    plt.title('N-SAT Results')
    plt.ylabel('Difference in Solve Time')
    plt.xlabel('Expression')
    plt.show()

    
   
