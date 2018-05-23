import sys
import json
from code_trace.get_trace import get_trace_main
from find_pattern.check_pattern import check_pattern_main


def print_help():
    print 'Usage: python main.py <action>'
    print 'Actions:'
    print 'code_trace (ct) - find trace code execution'
    print 'find_pattern (fp) - find pattern in source code'


def read_config():
    with open('config.json') as config_file:    
		return json.load(config_file)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_help()
        exit()

    if sys.argv[1] == 'help' or sys.argv[1] == 'h':
        print_help()
    elif sys.argv[1] == 'code_trace' or sys.argv[1] == 'ct':
        config = read_config()
        get_trace_main(config)
    elif sys.argv[1] == 'find_pattern' or sys.argv[1] == 'fp':
        config = read_config()
        check_pattern_main(config)
    else:
        print_help()