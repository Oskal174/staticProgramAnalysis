import os
from functional_objects import functional_object
from code_trace.get_trace import get_trace_main
from code_trace.get_trace import print_traces


def fmc_main(config):
	INTERPRETER = config["general"]["interpreter_path"]
	DATABASE_PATH = config["general"]["database_path"]
	CQL_FOLDER = config["general"]["root_path"] + "\\functional_management_control\\"

	main_object_code = config["functional_management_control"]["main_object"]
	secondary_object_code = config["functional_management_control"]["secondary_object"]	

	print 'Start processing of functional management control...'
	print 'Main object = ', main_object_code
	print 'Secondary object = ', secondary_object_code

	# get trace
	result = get_trace_main(config, main_object_code, 'EXIT', 'service')
	traces = result['traces']
	statement_types = result['statement_types']
	code_string_ids = result['code_string_ids']
	# trace[0] - string number
	# trace[1] - code
	# trace[2] - True, False or ''
	print_traces(traces, statement_types, code_string_ids)

	# do management control
	