

from optparse import OptionParser
import os
from cnf_types import CNF_Solver
import matplotlib.pyplot as plt






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
    
    '''
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
    '''
    
   
