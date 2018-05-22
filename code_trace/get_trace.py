# -*- coding: utf-8 -*-
# Main query
# MATCH (n1 {code:"ifstream file ( \"graphFile\" ) ;", isCFGNode:"True"}) MATCH (n2 {code:"file . close ( )", isCFGNode:"True"}) 
# MATCH path = ( (n1)-[:FLOWS_TO*..]-(n2) ) 
# RETURN extract(n IN nodes(path) | [n.location, n.code]) AS codes, extract(n IN relationships(path) | n.flowLabel) AS flowLabels;
#
# Additional query
# 
# MATCH (n1)-[r:IS_AST_PARENT]->(n2) WHERE id(n2) = <id> RETURN n1.type; 

import os
import sys


INTERPRETER = 'D:\\homework\\staticProgramAnalysis\\tools\\neo4j-community-2.3.12\\bin\\Neo4jShell.bat'
DATABASE_PATH = 'D:\\homework\\staticProgramAnalysis\\neo4j-db\\GraphAlgorithms-joern'
CQL_FOLDER = 'D:\\homework\\staticProgramAnalysis\\src\\staticProgramAnalysis\\code_trace\\'


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
		statement_types_keys.append(code_string_ids[key])

	#print statement_types_keys

	keys_index = 0
	statement_types = {}
	result_file = open('control-flow-res-2', 'r')
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


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print 'usage: python get_trace.py <code_1> <code_2>'
		exit()

	CODE_1 = sys.argv[1]
	CODE_2 = sys.argv[2]

	# preprocessing code_1 and code_2
	CODE_1 = 'ifstream file ( \\"graphFile\\" ) ;'
	CODE_2 = 'file . close ( )'

	# generate main query
	main_query_file = open('control-flow-1.cql', 'w')
	main_query_file.write('MATCH (n1 {code:"' + CODE_1 + '", isCFGNode:"True"}) MATCH (n2 {code:"' + CODE_2 + '", isCFGNode:"True"}) MATCH path = ( (n1)-[:FLOWS_TO*..]-(n2) ) RETURN extract(n IN nodes(path) | [n.location, n.code, id(n)]) AS codes, extract(n IN relationships(path) | n.flowLabel) AS flowLabels;')
	main_query_file.close()

	# main query
	os.system(INTERPRETER + ' -path ' + DATABASE_PATH + ' -file ' + CQL_FOLDER + 'control-flow-1.cql > control-flow-res-1')

	# parse main query results
	file = open('control-flow-res-1', 'r')
	
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

	# separate id from trace[1][i] - get dict code_string_ids[id] = code_string
	code_string_ids = {}
	for trace in traces:
		for i in range(len(trace[0])):
			separate_res = separate_id_from_code(trace[1][i])

			trace[1][i] = separate_res[0]
			code_string_id = separate_res[1]

			code_string_ids[trace[1][i]] = code_string_id

	#print code_string_ids

	# match type of statements (while, if, for) by id
	open('control-flow-res-2', 'w').close() # clean file
	for code_string, code_string_id in code_string_ids.items():
		#print code_string_id, code_string
		query = 'MATCH (n1)-[r:IS_AST_PARENT]->(n2) WHERE id(n2) = ' + code_string_id + ' RETURN n1.type;'
		os.system(INTERPRETER + ' -path ' + DATABASE_PATH + ' -c \"' + query + '\" >> control-flow-res-2')
		#print INTERPRETER + ' -path ' + DATABASE_PATH + ' -c \"' + query + '\" >> control-flow-res-2'
	# parse results in control-flow-res-2 file
	statement_types = parse_statements(code_string_ids)
	#print statement_types

	#for key, val in code_string_ids.items():
		#print key + ' <==> ' + statement_types[val]

	# print results
	print '===================================================================================================='
	# format print
	k = 0
	for trace in traces:
		print 'Trace ' + str(k) + '\n'
		for i in range(len(trace[0])):
			if i == len(trace[0])-1: # last string in trace
				print trace[0][i] + ' ' + trace[1][i]
			else:
				if trace[2][i] == '':
					print trace[0][i] + ' ' + trace[1][i] + ' -- ' + statement_types[code_string_ids[trace[1][i]]] + trace[2][i] + ' --> '
				else:
					print trace[0][i] + ' ' + trace[1][i] + ' -- ' + statement_types[code_string_ids[trace[1][i]]] + ':' + trace[2][i] + ' --> '

		k = k + 1
		print '===================================================================================================='