import sys
import json
from code_trace.get_trace import get_trace_main
from find_pattern.check_pattern import check_pattern_main
from information_objects.information_objects import information_objects_main


def print_help():
    print 'Usage: python main.py <action> <args>'
    print 'Actions:'
    print 'code_trace (ct) - find trace code execution'
    print 'find_pattern (fp) - find pattern in source code'
    print 'show_information_objects (sio <arg>) - show all information objects in project or write its to file'
    print '\t <arg>:'
    print '\t \'\' - print list to console'
    print '\t <file_name> - print list to file'


def read_config():
    with open('config.json') as config_file:    
		return json.load(config_file)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_help()
        exit()

    config = read_config()

    if sys.argv[1] == 'help' or sys.argv[1] == 'h':
        print_help()
    elif sys.argv[1] == 'code_trace' or sys.argv[1] == 'ct':
        get_trace_main(config)
    elif sys.argv[1] == 'find_pattern' or sys.argv[1] == 'fp':
        check_pattern_main(config)
    elif sys.argv[1] == 'show_information_objects' or sys.argv[1] == 'sio':
        file = ''
        if len(sys.argv) == 3:
            file = sys.argv[2]
        information_objects_main(config, file)
    else:
        print_help()