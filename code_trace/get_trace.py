# -*- coding: utf-8 -*-
# Main query
# MATCH (n1 {code:"ifstream file ( \"graphFile\" ) ;", isCFGNode:"True"}) MATCH (n2 {code:"file . close ( )", isCFGNode:"True"}) 
# MATCH path = ( (n1)-[:FLOWS_TO*..]->(n2) ) 
# RETURN extract(n IN nodes(path) | [n.location, n.code]) AS codes, extract(n IN relationships(path) | n.flowLabel) AS flowLabels;
#
# Additional query
# 
# MATCH (n1)-[r:IS_AST_PARENT]->(n2) WHERE id(n2) = <id> RETURN n1.type; 

import os
import sys
from functional_objects.functional_objects import functional_objects_main


def parseFlowLabel(string):
	if string == "\"\"":
		return ''
	else:
		return string[1:-1]


def parseCode(string):
	if string.find(']]') != -1:
		return string[:-3]
	else:
		return string[:-2]


def parseLineNumber(string):
	if string == '': # is its EXIT node
		return 'null'

	parts = string.split(':')
	return parts[0] + ':' + parts[1]


# return [[string_number, string_number, ... ], [code, code, ...]]
def parseLine(line):
	string_numbers = []
	codes = []
	string_number = ""
	code = ""

	isString_number = False
	isCode = False
	for index in range(len(line)):
		if line[index-2] == ']' and line[index-1] == ',' and line[index] == '[':
			#print string_number
			#print code
			string_numbers.append(parseLineNumber(string_number))
			codes.append(parseCode(code))

			string_number = ""
			code = ""
			continue

		if line[index-1] == '[' and line[index] == '\"':
			isString_number = True
			isCode = False
			continue

		if line[index-1] == ',' and line[index] == '\"':
			isString_number = False
			isCode = True
			continue

		if isString_number == True:
			string_number += line[index]
			continue
		if isCode == True:
			code += line[index]
			continue

	#print string_number
	#print code
	string_numbers.append(parseLineNumber(string_number))
	codes.append(parseCode(code))

	#print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

	return [string_numbers, codes]


# return [flow_label, flow_label, ...]
def parseFlowlabels(line):
	flow_labels = []
	flow_label = ""
	for index in range(len(line)):
		if line[index] == ' ' or line[index] == '[' or line[index] == ']':
			continue
		if line[index] == ',':
			flow_labels.append(parseFlowLabel(flow_label))
			flow_label = ""
			continue

		flow_label += line[index]

	flow_labels.append(parseFlowLabel(flow_label))

	return flow_labels


def separate_id_from_code(code_string):
	code_string_id = '0'
	for i in range(len(code_string)-1, 0, -1):
		if code_string[i] == ',':
			code_string_id = code_string[i+1:]
			code_string = code_string[:i-1]
			break
	return (code_string, code_string_id)


def parse_statements(code_string_ids):
	statement_types_keys = []
	for key in code_string_ids.keys(): 
		if key == '<null>,EXIT':
			continue
		statement_types_keys.append(code_string_ids[key])

	#print statement_types_keys

	keys_index = 0
	statement_types = {}
	result_file = open(r'code_trace\control-flow-2.cqlres', 'r')
	for line in result_file:
		statement_type = ''

		index = line.find('Statement')
		if index != -1:
			start = line.find('|') + 3
			end = line[start:].find('|') + 1
			statement_type = line[start:end]
			#print 'statement type = ' + statement_type
			statement_types[statement_types_keys[keys_index]] = statement_type
			keys_index += 1

	result_file.close()

	return statement_types


def check_functional_object_trace(traces, functional_objects):
	print 'Start checking fucntional object traces... '
	print 'Number of object for check: ', len(functional_objects)
	print 'Symbols for check: ',
	for obj in functional_objects:
		print obj.get_symbol(), ' ',
	print ''

	filtered_traces = []
	for trace in traces:
		break_flag = False
		current_codes = trace[1]
		for i in range(1, len(current_codes)):
			current_code = current_codes[i]
			if break_flag:
				break
			
			for obj in functional_objects:
				# TODO: problem with matching (symbol = i, match with int etc...)
				if current_code.find(obj.get_symbol()) != -1:
					filtered_traces.append(trace)
					break_flag = True
					break

	print 'done.'
	return filtered_traces


def print_traces(traces, statement_types, code_string_ids):
	print '===================================================================================================='
	# format print
	k = 0
	for trace in traces:
		print 'Trace ' + str(k) + '\n'
		for i in range(len(trace[0])):
			if trace[1][i] == '<null>,EXIT':
				print 'EXIT'
				continue

			if i == len(trace[0])-1: # last string in trace
				print trace[0][i] + ' ' + trace[1][i]
			else:
				if trace[2][i] == '':
					print trace[0][i] + ' ' + trace[1][i] + ' -- ' + statement_types[code_string_ids[trace[1][i]]] + trace[2][i] + ' --> '
				else:
					print trace[0][i] + ' ' + trace[1][i] + ' -- ' + statement_types[code_string_ids[trace[1][i]]] + ':' + trace[2][i] + ' --> '

		k = k + 1
		print '===================================================================================================='



def get_trace_main(config, args_code_1 = '', args_code_2 = '', mode = 'main'):
	INTERPRETER = config["general"]["interpreter_path"]
	DATABASE_PATH = config["general"]["database_path"]
	CQL_FOLDER = config["general"]["root_path"] + "\\code_trace\\"
	functional_object_trace = config["code_trace"]["functional_object_trace"]

	print 'Starting getting trace'
	if args_code_1 == '':
		CODE_1 = config["code_trace"]["code_1"]
	else:
		CODE_1 = args_code_1

	if args_code_2 == '':		
		CODE_2 = config["code_trace"]["code_2"]
	else:
		CODE_2 = args_code_2

	# TODO: preprocessing code_1 and code_2

	print 'CODE_1 = ', CODE_1
	print 'CODE_2 = ', CODE_2

	# generate main query
	main_query_file = open(r'code_trace\control-flow-1.cql', 'w')
	main_query_file.write('MATCH (n1 {code:"' + CODE_1 + '", isCFGNode:"True"}) MATCH (n2 {code:"' + CODE_2 + '", isCFGNode:"True"}) MATCH path = ( (n1)-[:FLOWS_TO*..]->(n2) ) RETURN extract(n IN nodes(path) | [n.location, n.code, id(n)]) AS codes, extract(n IN relationships(path) | n.flowLabel) AS flowLabels;')
	main_query_file.close()

	print 'Get all path... ',
	# main query
	#query = 'MATCH (n1 {code:"' + CODE_1 + '", isCFGNode:"True"}) MATCH (n2 {code:"' + CODE_2 + '", isCFGNode:"True"}) MATCH path = ( (n1)-[:FLOWS_TO*..]->(n2) ) RETURN extract(n IN nodes(path) | [n.location, n.code, id(n)]) AS codes, extract(n IN relationships(path) | n.flowLabel) AS flowLabels;'
	#os.system(INTERPRETER + ' -path ' + DATABASE_PATH + ' -c \"' + query + '\" > code_trace\control-flow-1.cqlres')
	os.system(INTERPRETER + ' -path ' + DATABASE_PATH + ' -file ' + CQL_FOLDER + 'control-flow-1.cql > ' + CQL_FOLDER + 'control-flow-1.cqlres')
	#print INTERPRETER + ' -path ' + DATABASE_PATH + ' -file ' + CQL_FOLDER + 'control-flow-1.cql > ' + CQL_FOLDER + 'control-flow-1.cqlres'

	# parse main query results
	file = open(r'code_trace\control-flow-1.cqlres', 'r')
	
	traces = []
	for line in file:
		if line.find('| [[') != -1:
			line = ' '.join(line.split())
			#print line
			
			line_parts = line.split('|')

			parse_result = parseLine(line_parts[1])
			string_numbers = parse_result[0]
			codes = parse_result[1]

			parse_result = parseFlowlabels(line_parts[2])
			flow_labels = parse_result

			#print len(string_numbers), len(codes), len(flow_labels)
			traces.append([string_numbers, codes, flow_labels])

	file.close()
	print 'done.'

	if len(traces) == 0:
		print "There is no trace between | " + CODE_1 + " | and | " + CODE_2 + " |"
		return

	# separate id from trace[1][i] - get dict code_string_ids[id] = code_string
	code_string_ids = {}
	for trace in traces:
		for i in range(len(trace[0])):
			separate_res = separate_id_from_code(trace[1][i])

			trace[1][i] = separate_res[0]
			code_string_id = separate_res[1]

			code_string_ids[trace[1][i]] = code_string_id

	#print code_string_ids

	print 'Get types of statements... ',
	# match type of statements (while, if, for) by id
	open(r'code_trace\control-flow-2.cqlres', 'w').close() # clean file
	for code_string, code_string_id in code_string_ids.items():
		#print code_string_id, code_string
		if code_string == '<null>,EXIT':
			continue
		
		query = 'MATCH (n1)-[r:IS_AST_PARENT]->(n2) WHERE id(n2) = ' + code_string_id + ' RETURN n1.type;'
		os.system(INTERPRETER + ' -path ' + DATABASE_PATH + ' -c \"' + query + '\" >> code_trace\control-flow-2.cqlres')
		#print INTERPRETER + ' -path ' + DATABASE_PATH + ' -c \"' + query + '\" >> code_trace\control-flow-2.cqlres'
	# parse results
	statement_types = parse_statements(code_string_ids)
	#print statement_types

	print 'done.'

	#for key, val in code_string_ids.items():
		#print key + ' <==> ' + statement_types[val]

	# check functional objects in paths and filter it
	if functional_object_trace == 1 and mode == 'main':
		functional_objects = functional_objects_main(config, 'get_one', CODE_1)
		traces = check_functional_object_trace(traces, functional_objects)
		if len(traces) == 0:
			print 'There is no trace with functional object(s):'
			for obj in functional_objects:
				print '\t', obj
			return

	# show results
	# trace[0] - string number
	# trace[1] - code
	# trace[2] - True, False or ''
	if mode == 'main':
		print_traces(traces, statement_types, code_string_ids)
	elif mode == 'service':
		# TODO: create class for containing trace
		return {'statement_types': statement_types, 'traces': traces, 'code_string_ids': code_string_ids}