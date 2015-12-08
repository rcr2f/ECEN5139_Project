

from sat_solver import general_solve, horn_solve, two_SAT_solve, N_SAT_solve
import datetime
import os
#Horn solve
#2 sat solve
#n solve
#general solve

cnf = ['general', 'horn', 'two', 'N']

class CNF_Solver():

    def __init__(self, cnf_file):
        #parse string
        self.cnf_file = open(os.path.join(cnf_file), 'r')
        self.expressions = list() #[expression][clause][sign and literal]
        self.expression_types = list()
        self.num_literals = list()
        self.num_clauses = list()
        for line in self.cnf_file:
            #print line
            expression, num_literals = self.parse_cnf(line)
            self.expressions.append(expression)
            self.num_clauses.append(len(expression))
            self.num_literals.append(num_literals)
            self.expression_types.append(self.determine_type(expression))
        self.horn_results = [0]*len(self.expressions)
        self.two_results = [0]*len(self.expressions)
        self.N_results = [0]*len(self.expressions)
        self.SAT_result = list() #NOTE: No actual results stored here. it's just a 1 if an assigment was found, else 0
        self.timing_results = list()
        self.horns = list()
        self.twos = list()
        self.Ns = list()
        
        
    	
        
        #for cnf in self.expressions:
            #print cnf

        self.cnf_file.close()

    def parse_cnf(self, line):
        clauses = ((line.translate(None,'(')).translate(None,')')).strip().split("^")
        parsed_expression = list()
        literals = set()
        for clause in clauses:
            literal_set = set(clause.translate(None,' ').split("v"))
            parsed_expression.append(literal_set)
            for literal in literal_set:
                if literal.translate(None, '!') not in literals:
                    literals.add(literal.translate(None, '!'))
        return parsed_expression, len(literals)

    def determine_type(self, expression):
        types = cnf[0]
        horn = True
        lengths = set()
        for clause in expression:
            count = 0
            lengths.add(len(clause))
            for literal in clause:
                if '!' not in literal:
                    count += 1
            if count > 1:
                horn = False
        if horn:
            types += cnf[1]
        if len(lengths) > 1:
            print types
            return types
        elif 2 in lengths:
            types += cnf[2]
        else:
            types += cnf[3]
        print types
        return types


    def general_solve_all(self):

        for expression in self.expressions:
            #print expression
            begin_time = datetime.datetime.now()
            result = self.general_SAT_solve(expression)
            self.SAT_result.append(result)
            #print result
            time = (datetime.datetime.now()-begin_time).total_seconds()
            #print time
            self.timing_results.append(time)
            

    def general_SAT_solve(self, expression):
        return general_solve(expression)

    def get_new_list(self, ori_list, indexes):
        new_list = list()
        for i in indexes:
            new_list.append(ori_list[i])
        return new_list

    def optimized_solve_all(self):
        for index, expression in enumerate(self.expressions):
            if 'horn' in self.expression_types[index]:
                self.solve_horn(index)
            if 'two' in self.expression_types[index]:
                self.solve_two_SAT(index)
            elif 'N' in self.expression_types[index]:
                self.solve_N_SAT(index)
        return

    def solve_horn(self, index):
        self.horns.append(index)
        begin_time = datetime.datetime.now()
        #computation
        horn_solve(self.expressions[index])
        self.horn_results[index] = ((datetime.datetime.now()-begin_time).total_seconds())
        return

    def solve_two_SAT(self, index):
        self.twos.append(index)
        begin_time = datetime.datetime.now()
        #computation
        two_SAT_solve(self.expressions[index])
        self.two_results[index] = ((datetime.datetime.now()-begin_time).total_seconds())
        return

    def solve_N_SAT(self, index):
        self.Ns.append(index)
        begin_time = datetime.datetime.now()
        #computation
        N_SAT_solve(self.expressions[index])
        self.N_results[index] = ((datetime.datetime.now()-begin_time).total_seconds())
        return
	
