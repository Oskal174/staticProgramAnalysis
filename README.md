** Конфигурационный файл config.json

В секции "general" находятся общие настройки проекта. 
- "root_path" описывает путь до директории с этим проектом в операционной системе
- "interpreter_path" описывает путь до интерпретатора СУБД neo4j, позволяющего исполнять запросы с базе данных
- "database_path" описывает путь до директории в которой находится результат работы инструмента статического анализа Joern

В секции "code_trace" находятся настройки модуля поиска трассы исполнения кода
- "code_1" начальная точка трассы
- "code_2" конечная точка трассы
- "information_object_trace" флаг означающий поиск путей исполнения информационных объектов (1-искать, 0-простая трасса)

В секции "find_pattern" находятся настройки модуля поиска вхождения определенных конструкции в исходном тексте
- "patterns" массив описывающий конструкции для поиска

** Правила экранирования специальных символов в конфигурационном файле

ifstream file ( \\\"graphFile\\\" ) ;

** Пример конфигурационного файла
{
    "general" : {
        "root_path"         : "D:\\homework\\staticProgramAnalysis\\src\\staticProgramAnalysis",
        "interpreter_path"  : "D:\\homework\\staticProgramAnalysis\\tools\\neo4j-community-2.3.12\\bin\\Neo4jShell.bat",
        "database_path"     : "D:\\homework\\staticProgramAnalysis\\neo4j-db\\GraphAlgorithms-joern"
    },

    "code_trace" : {
        "code_1" : "ifstream file ( \\\"graphFile\\\" ) ;",
        "code_2" : "file . close ( )",
        "information_object_trace" : 1
    },

    "find_pattern" : {
        "patterns" : [
            "ifstream file ( \\\"graphFile\\\" ) ;",
            "file . close ( )",
            "file"
        ]
    }
}