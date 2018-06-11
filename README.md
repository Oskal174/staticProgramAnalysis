staticProgramAnalysis - программа статического анализа проектов по исходному коду
=====================

Описание проектов, инструментов анализа и проектов.

Конфигурационный файл
-----------------------------------

Конфигурационный файл в формате json разделен на несколько секций и предназначен для управления настройками проекта. По умолчанию проект запускается с конфигурационным файлом **config.json**, находящимся в корне проекта.

В секции ***"general"*** находятся общие настройки проекта. 
- "root_path" описывает путь до директории с этим проектом в операционной системе;
- "interpreter_path" описывает путь до интерпретатора СУБД neo4j, позволяющего исполнять запросы с базе данных;
- "database_path" описывает путь до директории в которой находится результат работы инструмента статического анализа Joern.

В секции ***"code_trace"*** находятся настройки модуля поиска трассы исполнения кода.
- "code_1" начальная точка трассы;
- "code_2" конечная точка трассы;
- "functional_object_trace" флаг означающий поиск путей исполнения функциональных объектов (1-искать, 0-простая трасса).

В секции ***"functional_management_control"*** находятся настройки модуля, отвечающего за контроль функциональных объектов по управлению.
- "main_object" исследуемый объект;
- "secondary_object" второстепенный объект.

В секции ***"functional_information_control"*** находятся настройки модуля, отвечающего за контроль функциональных объекто по информации.
- "main_object" исследуемый объект;
- "secondary_object" второстепенный объект.

В секции ***"find_pattern"*** находятся настройки модуля поиска вхождения определенных конструкции в исходном тексте
- "patterns" массив описывающий конструкции для поиска

### Пример конфигурационного файла

    {
        "general" : {
            "root_path"         : "D:\\homework\\staticProgramAnalysis\\src\\staticProgramAnalysis",
            "interpreter_path"  : "D:\\homework\\staticProgramAnalysis\\tools\\neo4j-community-2.3.12\\bin\\Neo4jShell.bat",
            "database_path"     : "D:\\homework\\staticProgramAnalysis\\neo4j-db\\GraphAlgorithms-joern"
        },
    
        "code_trace" : {
            "code_1" : "ifstream file ( \\\"graphFile\\\" ) ;",
            "code_2" : "file . close ( )",
            "functional_object_trace"           : 1,
            "functional_management_control"     : 0,
            "functional_information_control"    : 0
        },
    
        "find_pattern" : {
            "patterns" : [
                "ifstream file ( \\\"graphFile\\\" ) ;",
                "file . close ( )",
                "file"
            ]
        }
    }