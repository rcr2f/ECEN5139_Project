#random cnf clause generator

import random
import os


alpha = ['a','b','c','d', 'e', 'f', 'g', 'h', 'i','j','k','l','m']



num_cnf =  input("Number of cnf expressions to generate: ")
max_clause_len =  input("Max clause length: ")
min_clause_len =  input("Min clause length: ")
max_num_clauses  =  input("Max number of clauses per expression: ")
if(max_clause_len > 12): max_clause_len = 12 #add more characters to alpha if you want longer clauses

filename  =  "cnf_expressions"
path = os.path.join(filename) + ".txt"
output_file = open(path, 'w')

for i in range(num_cnf):
	expression = ""
	clauses = random.randint(1,max_num_clauses)
	for j in range(clauses):
		length = random.randint(min_clause_len,max_clause_len)
		expression += "("
		for k in range(length):
			if (random.randint(0,1) == 0):
				expression += '!'
			expression += alpha[k]
			if (k != length - 1):
				expression += ' v '
		expression += ')'
		if (j != clauses- 1):
			expression += ' ^ '
	output_file.write(expression + '\n')

output_file.close()

