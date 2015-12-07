#random cnf clause generator

import random
import os


alpha = ['a','b','c','d', 'e', 'f', 'g', 'h', 'i','j','k','l','m','n','o','p','q','r','s','t','u']



num_cnf =  input("Number of cnf expressions to generate: ")
max_clause_len =  input("Max literals per clause: ")
min_clause_len =  input("Min literals per clause: ")

max_num_clauses  =  input("Max number of clauses per expression: ")
min_num_clauses = input("Min number of clauses per expression: ")

likelihood_horn = input("Percent chance of being horn: ")
likelihood_same_len_clauses = input("Percent chance of being 2 or N: ")
if(max_clause_len > 20): max_clause_len = 20 #add more characters to alpha if you want longer clauses

filename  =  "cnf_expressions"
path = os.path.join(filename) + ".txt"
output_file = open(path, 'w')

for i in range(num_cnf):
	expression = ""
	clauses = random.randint(min_num_clauses,max_num_clauses)
	horn_chance = random.randint(0,100)
	horn = False
	same = False
	if horn_chance <= likelihood_horn:
		horn = True
	same_len = random.randint(0,100)
	if same_len <= likelihood_same_len_clauses:
		same = True
		length = random.randint(min_clause_len,max_clause_len)

	for j in range(clauses):
		if not same: 
			length = random.randint(min_clause_len,max_clause_len)
		if horn:
			positive = random.randint(0, length-1)

		expression += "("
		clause = ""
		for k in range(length):
			literal = alpha[random.randint(0, max_clause_len-1)]
			while literal in clause:
				literal = alpha[random.randint(0, max_clause_len-1)]
			if horn:
				if k != positive:
					clause += '!'
			else:
				if (random.randint(0,1) == 0):
					clause += '!'
			clause += literal
			if (k != length - 1):
				clause += ' v '
		expression += clause+')'
		if (j != clauses- 1):
			expression += ' ^ '
	output_file.write(expression + '\n')

output_file.close()

