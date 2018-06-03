import os
from functional_object import functional_object


def functional_objects_main(config, mode = 'get_all', arg = ''):
    INTERPRETER = config["general"]["interpreter_path"]
    DATABASE_PATH = config["general"]["database_path"]
    ROOT_DIRECTORY = config["general"]["root_path"]

    if mode == 'get_all':
        return get_all_fo(INTERPRETER, DATABASE_PATH, ROOT_DIRECTORY, arg)
    elif mode == 'get_one':
        return get_one_fo(INTERPRETER, DATABASE_PATH, ROOT_DIRECTORY, arg)
    else:
        print 'Wrong mode in functional_objects_main...'


# return list of functional objects (more than one if "int a, b")
def get_one_fo(INTERPRETER, DATABASE_PATH, ROOT_DIRECTORY, fo_code):
    print 'Get one functional object... ',
    query = 'match (n) where n.code=\'' + fo_code + '\' AND n.type=\'IdentifierDeclStatement\' AND n.isCFGNode=\'True\' return n.code as functional_object, n.location as location, id(n) as id;'
    open(r'functional_objects\functional_objects-1.cqlres', 'w').close() # clear file
    os.system(INTERPRETER + ' -path ' + DATABASE_PATH + ' -c \"' + query + '\"' + r' >> functional_objects\functional_objects-1.cqlres')
    print 'done.'

    # parse file and get object 
    functional_objects_result = open(r'functional_objects\functional_objects-1.cqlres', 'r')
    
    for line in functional_objects_result:
        if line[0] == '|' and line.find('| functional_object') == -1:
            obj = parse_line_inf_obj(line)

    functional_objects_result.close()

    list_objects = [obj]
    # get symbol of functional object
    print 'Get symbol of functional object... ',
    open(r'functional_objects\functional_objects-2.cqlres', 'w').close() # clear file
    query = 'MATCH (n1)-[r:DEF]->(n2) WHERE id(n1)=' + obj.get_id() + ' RETURN n2.code;'
    os.system(INTERPRETER + ' -path ' + DATABASE_PATH + ' -c \"' + query + '\"' + r' >> functional_objects\functional_objects-2.cqlres')

    functional_objects_result = open(r'functional_objects\functional_objects-2.cqlres', 'r')
    list_object_index = 0
    is_one_io = False
    while (True):
        line = functional_objects_result.readline()
        if line == '':
            break

        if line[0] == '|' and line.find('n2.code') != -1:
            functional_objects_result.readline() # skip first '+----- delimiter
            symbols = []
            while (True):
                line = functional_objects_result.readline()
                if line.find('+---') != -1:
                    break
                if line[0] == '|' and line.find('n2.code') == -1:
                    symbol = line[line.find('\"')+1:line.rfind('\"')]
                    symbols.append(symbol)

            list_objects[list_object_index].set_symbol(symbols[0])
            for i in range(1, len(symbols)):
                new_object = functional_object(list_objects[list_object_index].get_code(), symbols[i], list_objects[list_object_index].get_location(), list_objects[list_object_index].get_id())
                list_objects.append(new_object)

            list_object_index += 1

    functional_objects_result.close()

    print 'done.'
    return list_objects


def get_all_fo(INTERPRETER, DATABASE_PATH, ROOT_DIRECTORY, output_file):
    print 'Get all functional objects... ',
    query = 'match (n) where n.type=\'IdentifierDeclStatement\' AND n.isCFGNode=\'True\' return n.code as functional_object, n.location as location, id(n) as id;'
    open(r'functional_objects\functional_objects-1.cqlres', 'w').close() # clear file
    #print INTERPRETER + ' -path ' + DATABASE_PATH + ' -c \"' + query + '\"' + r' >> functional_objects\functional_objects-1.cqlres'
    os.system(INTERPRETER + ' -path ' + DATABASE_PATH + ' -c \"' + query + '\"' + r' >> functional_objects\functional_objects-1.cqlres')

    # parse file and get list of objects
    functional_objects_result = open(r'functional_objects\functional_objects-1.cqlres', 'r')
    
    list_objects = []
    for line in functional_objects_result:
        new_object = -1
        if line[0] == '|' and line.find('| functional_object') == -1:
            new_object = parse_line_inf_obj(line)

        if new_object != -1:
            list_objects.append(new_object)

    functional_objects_result.close()
    print 'done. Found ' + str(len(list_objects)) + ' objects'

    # get all symbols of functional objects
    print 'Get symbols of functional objects ',
    open(r'functional_objects\functional_objects-2.cqlres', 'w').close() # clear file
    for obj in list_objects:
        query = 'MATCH (n1)-[r:DEF]->(n2) WHERE id(n1)=' + obj.get_id() + ' RETURN n2.code;'
        os.system(INTERPRETER + ' -path ' + DATABASE_PATH + ' -c \"' + query + '\"' + r' >> functional_objects\functional_objects-2.cqlres')
        print '.',

    # parse results
    functional_objects_result = open(r'functional_objects\functional_objects-2.cqlres', 'r')

    list_object_index = 0
    is_one_io = False
    while (True):
        line = functional_objects_result.readline()
        if line == '':
            break

        if line[0] == '|' and line.find('n2.code') != -1:
            functional_objects_result.readline() # skip first '+----- delimiter
            symbols = []
            while (True):
                line = functional_objects_result.readline()
                if line.find('+---') != -1:
                    break
                if line[0] == '|' and line.find('n2.code') == -1:
                    symbol = line[line.find('\"')+1:line.rfind('\"')]
                    symbols.append(symbol)

            list_objects[list_object_index].set_symbol(symbols[0])
            for i in range(1, len(symbols)):
                new_object = functional_object(list_objects[list_object_index].get_code(), symbols[i], list_objects[list_object_index].get_location(), list_objects[list_object_index].get_id())
                list_objects.append(new_object)

            list_object_index += 1

    functional_objects_result.close()
    print 'done'

    # show objects
    if output_file == '':
        print 'Result:'
        print '------------------------------------------------------------------'
        for obj in list_objects:
            print obj
        print '------------------------------------------------------------------'
    elif output_file == 'return_list_objects':
        return list_objects
    else:
        # write objects to output_file
        print 'Result in ' + output_file + ' file'
        write_io_to_file(list_objects, output_file)


def write_io_to_file(list_objects, output_file_name):
    out_file = open(output_file_name, 'w')
    for obj in list_objects:
        #out_file.write(obj.get_id() + " : " + obj.get_location() + " : " + obj.get_code() + ' -> ' + obj.get_symbol() + '\n')
        out_file.write(obj.get_str())
    out_file.close()


def parse_line_inf_obj(line):
    sub_lines = line.split('|')
    if len(sub_lines) != 5: # by example: int a |= 10; # TODO: test it
        code_start = line.find('\"')
        code_end = line.find('\"', code_start+1)
        code = line[code_start+1:code_end]

        location_start = line.find('\"', code_end+1)
        location_end = line.find('\"', location_start+1)
        location = line[location_start+1:location_end]

        id_start = line.find('|', location_end+1)
        id_end = line.find('|', id_start+1)
        id = ''
        for i in range(id_start, id_end):
            if line[i] != '|' and line[i] != ' ':
                id += line[i]

        return functional_object(code, 'default_symbol', location, id)

    # normal case
    code_start = sub_lines[1].find('\"')
    code_end = sub_lines[1].rfind('\"')
    code = sub_lines[1][code_start+1:code_end]

    location_start = sub_lines[2].find('\"')
    location_end = sub_lines[2].rfind('\"')
    location = sub_lines[2][location_start+1:location_end]

    id = ''
    for i in range(len(sub_lines[3])):
        if sub_lines[3][i] != '|' and sub_lines[3][i] != ' ':
            id += sub_lines[3][i]

    #print line
    #print line.split('|')
    return functional_object(code, 'default_symbol', location, id)


#------------------------------------------------------------------------------------------
# for tests
if __name__ == '__main__':
    io = functional_object(1, 2)
    print io.get_code()