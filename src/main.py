

from optparse import OptionParser
import os
import sat_solver
import cnf_types






#get user input file for CNF expressions

#run generic sat solver on each

#run optimized sat solver on each

#compare results in pretty matplotlib
def get_input_arguments():
    parser = OptionParser()
    parser.add_option("-f", dest="cnf_file", default='cnf_expressions.txt', help="CNF expressions file")
    (options, args) = paerse.parse_args()
    return vars(options)

if __name__ == '__main__':
    options = get_input_arguments()

    cnf_file = options["cnf_file"]
    cnf_expressions = open(os.path.join(cnf_file), 'r')
    
    cnf_type_found = list()
    general_eval_time = list()
    optimized_eval_time = list()
    for expression in cnf_expression:
	
    
   
