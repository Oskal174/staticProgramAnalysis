import sys
import json
import time
from code_trace.get_trace import get_trace_main
from find_pattern.check_pattern import check_pattern_main
from functional_objects.functional_objects import functional_objects_main
from functional_information_control.functional_information_control import fic_main
from functional_management_control.functional_management_control import fmc_main


def print_help():
    print 'Usage: python main.py <action> <args>'
    print 'Actions:'
    print 'code_trace (ct) - find trace code execution'
    print 'find_pattern (fp) - find pattern in source code'
    print 'show_functional_objects (sfo <arg>) - show all functional objects in project or write its to file'
    print '\t <arg>:'
    print '\t \'\' - print list to console'
    print '\t <file_name> - print list to file'
    print 'functional_management_control (fmc) - make functional management control'
    print 'functional_information_control (fic) - make functional information control'


def read_config():
    with open('config.json') as config_file:    
		return json.load(config_file)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_help()
        exit()

    start_time = time.clock()
    config = read_config()

    if sys.argv[1] == 'help' or sys.argv[1] == 'h':
        print_help()
    elif sys.argv[1] == 'code_trace' or sys.argv[1] == 'ct':
        get_trace_main(config)
    elif sys.argv[1] == 'find_pattern' or sys.argv[1] == 'fp':
        check_pattern_main(config)
    elif sys.argv[1] == 'show_functional_objects' or sys.argv[1] == 'sfo':
        file = ''
        if len(sys.argv) == 3:
            file = sys.argv[2]
        functional_objects_main(config, 'get_all', file)
    elif sys.argv[1] == 'functional_management_control' or sys.argv[1] == 'fmc':
        fmc_main(config)
    elif sys.argv[1] == 'functional_information_control' or sys.argv[1] == 'fic':
        fic_main(config)
    else:
        print_help()
    
    print 'time = ', time.clock() - start_time, 'seconds'