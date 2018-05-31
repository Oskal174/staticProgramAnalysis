import os
from information_object import information_object


def information_objects_main(config, file = ''):
    INTERPRETER = config["general"]["interpreter_path"]
    DATABASE_PATH = config["general"]["database_path"]
    ROOT_DIRECTORY = config["general"]["root_path"]

    # it's only one option
    get_all_io(INTERPRETER, DATABASE_PATH, ROOT_DIRECTORY, file)


def get_all_io(INTERPRETER, DATABASE_PATH, ROOT_DIRECTORY, output_file):
    query = 'match (n) where n.type=\'IdentifierDeclStatement\' AND n.isCFGNode=\'True\' return n.code as information_object, n.location as location, id(n) as id;'
    open('information_objects\information_objects.cqlres', 'w').close() # clear file
    os.system(INTERPRETER + ' -path ' + DATABASE_PATH + ' -c \"' + query + '\" >> information_objects\information_objects.cqlres')

    # parse file and get list of objects
    information_objects_result = open('information_objects\information_objects.cqlres', 'r')
    
    list_objects = []
    for line in information_objects_result:
        information_object = -1
        if line[0] == '|' and line.find('| information_object') == -1:
            information_object = parse_line(line)

        if information_object != -1:
            list_objects.append(information_object)

    information_objects_result.close()

    # get all symbols of information objects
    open('information_objects\information_objects.cqlres', 'w').close() # clear file
    for obj in list_objects:
        query = 'MATCH (n1)-[r:DEF]->(n2) WHERE id(n1)=' + obj.get_id() + ' RETURN n2.code;'
        print query
        os.system(INTERPRETER + ' -path ' + DATABASE_PATH + ' -c \"' + query + '\" >> information_objects\information_objects.cqlres')

    # show objects
    if output_file == '':
        for information_object in list_objects:
            print information_object
    elif output_file == 'return_list_objects':
        return list_objects
    else:
        # write objects to output_file
        write_io_to_file(list_objects, output_file)


def write_io_to_file(list_objects, output_file_name):
    out_file = open(output_file_name, 'w')
    for information_object in list_objects:
        out_file.write(information_object.get_id() + " : " + information_object.get_location() + " : " + information_object.get_code() + '\n')
    out_file.close()


def parse_line(line):
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

        return information_object(code, 'default_symbol', location, id)

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
    return information_object(code, 'default_symbol', location, id)





# for tests
if __name__ == '__main__':
    io = information_object(1, 2)
    print io.get_code()