

import random
import os

alpha = ['a','b','c','d']

print "Number of cnf expressions to generate:"
num_cnf = 100

print "Max clause length:"
max_clause_len = 4

print "Min clause length"
min_clause_len = 2

print "Max number of clauses per expression:"
max_num_clauses = 10

print "Filename to print to:"
filename = "cnf_expressions.txt"
path = os.path.join(filename)
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

