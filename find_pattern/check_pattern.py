# -*- coding: utf-8 -*-
# Main query
# MATCH (n) WHERE n.isCFGNode="True" AND n.code CONTAINS 'PATTERN' RETURN n.code, n.location;

import os
import sys


def check_pattern_main(config):
	INTERPRETER = config["general"]["interpreter_path"]
	DATABASE_PATH = config["general"]["database_path"]
	CQL_FOLDER = config["general"]["cql_path"]

	patterns = config["find_pattern"]["patterns"]
	
	open(r'find_pattern\find-pattern.cqlres', 'w').close() # clean file
	for pattern in patterns:
		query = 'MATCH (n) WHERE n.isCFGNode=\'True\' AND n.code CONTAINS \'' + pattern + '\' RETURN n.code, n.location;'
		os.system('echo pattern: ' + pattern + ' >> ' + r'find_pattern\find-pattern.cqlres')
		os.system(INTERPRETER + ' -path ' + DATABASE_PATH + ' -c \"' + query + '\" >> ' + r'find_pattern\find-pattern.cqlres')
		#print INTERPRETER + ' -path ' + DATABASE_PATH + ' -c \"' + query + '\" >> ' + r'find_pattern\find-pattern.cqlres'

	# parse result
	print '===================================================================================================='
	result_file = open(r'find_pattern\find-pattern.cqlres')
	for line in result_file:
		if line.find(' ms') != -1 or line.find(' row') != -1:
			continue
		
		#if line.find('pattern:') != 1:
			#print '===================================================================================================='
		
		print line
	result_file.close()
	print '===================================================================================================='