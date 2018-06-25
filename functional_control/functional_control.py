import os
from functional_objects import functional_object
from code_trace.get_trace import get_trace_main
from code_trace.get_trace import print_traces
from functional_objects.functional_objects import functional_objects_main


def parse_trace(main_object, secondary_object, trace, param):
	if param == 'fmc':
		print 'Start parsing traces to functional management control...'	
	elif param == 'fic':
		print 'Start parsing traces to functional information control...'	
	#print 'trace = ', trace

	suitable_trace = [[], [], []]
	for i in range(len(trace[0])):
		current_code = trace[1][i]
		
		if (current_code.find(main_object.get_symbol_spaces()) != -1) and (current_code.find(secondary_object.get_symbol_spaces()) != -1):
			suitable_trace[0].append(trace[0][i])
			suitable_trace[1].append(trace[1][i])
			suitable_trace[2].append(trace[2][i])
	#print 'suitable trace = ', suitable_trace
	
	resutl_trace = [[], [], []]
	if param == 'fmc':
		for i in range(len(suitable_trace[0])):
			current_code = suitable_trace[1][i]

			# main obj at the right side by = -> secondObj = mainObj
			if current_code.find('=') != -1:
				parts = current_code.split('=')
				for j in range(1, len(parts)):
					#print 'parts = ', parts
					if (parts[j].find(main_object.get_symbol_spaces()) != -1) and (parts[0].find(secondary_object.get_symbol_spaces()) != -1):
						resutl_trace[0].append(suitable_trace[0][i])
						resutl_trace[1].append(suitable_trace[1][i])
						resutl_trace[2].append(suitable_trace[2][i])
				continue

			# main obj in the method call -> secondObj.method(mainObj)
			dot_index = current_code.find('.')
			open_bkt = current_code.find('(')
			close_bkt = current_code.find(')')
			main_obj_sym = current_code.find(main_object.get_symbol_spaces())
			secondary_obj_sym = current_code.find(secondary_object.get_symbol_spaces())
			
			#print open_bkt
			#print close_bkt
			#print main_obj_sym
			#print secondary_obj_sym

			if dot_index != -1:
				if open_bkt == -1 or close_bkt == -1 or main_obj_sym == -1 or secondary_obj_sym == -1:
					continue

				if open_bkt < main_obj_sym < close_bkt:
					resutl_trace[0].append(suitable_trace[0][i])
					resutl_trace[1].append(suitable_trace[1][i])
					resutl_trace[2].append(suitable_trace[2][i])
				continue
			
			# main obj in the constructor call -> secondObj so(mainObj)
			if open_bkt != -1 and close_bkt != -1:
				if main_obj_sym == -1 or secondary_obj_sym == -1:
					continue
				
				if open_bkt < main_obj_sym < close_bkt:
					resutl_trace[0].append(suitable_trace[0][i])
					resutl_trace[1].append(suitable_trace[1][i])
					resutl_trace[2].append(suitable_trace[2][i])
				continue

			# TODO: other operators (<<, >>, +, etc.) 

	elif param == 'fic':
		for i in range(len(suitable_trace[0])):
			current_code = suitable_trace[1][i]

			# main obj at the left side by = -> mainObj = secondaryObj
			if current_code.find('=') != -1:
				parts = current_code.split('=')
				for j in range(1, len(parts)):
					#print 'parts = ', parts
					if (parts[j].find(secondary_object.get_symbol_spaces()) != -1) and (parts[0].find(main_object.get_symbol_spaces()) != -1):
						resutl_trace[0].append(suitable_trace[0][i])
						resutl_trace[1].append(suitable_trace[1][i])
						resutl_trace[2].append(suitable_trace[2][i])
				continue

			# secondary obj in the method call -> mainObj.method(secondObj)
			dot_index = current_code.find('.')
			open_bkt = current_code.find('(')
			close_bkt = current_code.find(')')
			main_obj_sym = current_code.find(main_object.get_symbol_spaces())
			secondary_obj_sym = current_code.find(secondary_object.get_symbol_spaces())
			
			#print open_bkt
			#print close_bkt
			#print main_obj_sym
			#print secondary_obj_sym

			if dot_index != -1:
				if open_bkt == -1 or close_bkt == -1 or main_obj_sym == -1 or secondary_obj_sym == -1:
					continue

				if open_bkt < secondary_obj_sym < close_bkt:
					resutl_trace[0].append(suitable_trace[0][i])
					resutl_trace[1].append(suitable_trace[1][i])
					resutl_trace[2].append(suitable_trace[2][i])
				continue
			
			# second obj in the constructor call -> mainObj mo(secondObj)
			if open_bkt != -1 and close_bkt != -1:
				if main_obj_sym == -1 or secondary_obj_sym == -1:
					continue
				
				if open_bkt < secondary_obj_sym < close_bkt:
					resutl_trace[0].append(suitable_trace[0][i])
					resutl_trace[1].append(suitable_trace[1][i])
					resutl_trace[2].append(suitable_trace[2][i])
				continue

			# TODO: other operators (<<, >>, +, etc.)
	else:
		print 'wrong param'

	#print 'result trace = ', resutl_trace
	print 'done.'
	return resutl_trace


def fc_main(config, param):
	INTERPRETER = config["general"]["interpreter_path"]
	DATABASE_PATH = config["general"]["database_path"]
	CQL_FOLDER = config["general"]["root_path"] + "\\functional_management_control\\"

	if param == 'fmc':
		print 'Start processing of functional management control...'
		main_object_code = config["functional_management_control"]["main_object"]
		secondary_object_code = config["functional_management_control"]["secondary_object"]	
	elif param == 'fic':
		print 'Start processing of functional information control...'
		main_object_code = config["functional_information_control"]["main_object"]
		secondary_object_code = config["functional_information_control"]["secondary_object"]	
	else:
		print 'Wrong param, exiting...'
		return

	# get object by code
	list_main_objects = functional_objects_main(config, 'get_one', main_object_code)
	list_secondary_objects = functional_objects_main(config, 'get_one', secondary_object_code)

	print 'There is ', len(list_main_objects), ' main objects in project'
	for o in list_main_objects:
		print '\t', o

	print 'There is ', len(list_secondary_objects), ' secondary objects in project'
	for o in list_secondary_objects:
		print '\t', o

	# get trace for main object(s)
	result = get_trace_main(config, list_main_objects[0].get_code(), 'EXIT', 'service')
	traces = result['traces']
	statement_types = result['statement_types']
	code_string_ids = result['code_string_ids']
	# trace[0] - string number
	# trace[1] - code
	# trace[2] - True, False or ''
	

	# do management or information control
	results = [] # one trace <--> one result
	for trace in traces:
		result = parse_trace(list_main_objects[0], list_secondary_objects[0], trace, param)
		results.append(result)

	print_traces(traces, statement_types, code_string_ids)
	print 'Examples of interaction between objects'
	k = 0
	for res in results:
		print 'For trace ', str(k)
		if len(res[0]) == 0:
			print '\t No'
		for i in range(len(res[0])):
			print '\t', res[0][i], ' ', res[1][i]
		k += 1

	