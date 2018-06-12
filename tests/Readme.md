Результаты тестирования
=====================

Директория содержит результаты тестирования программы, далее идет описание каждого теста.

### Тест №1

Цель: проверить способность программы построить трассу исполнения участка кода, либо сообщить, что такой трассы не существует.

Последовательность действий оператора:
1.	В конфигурационном файле заполнить поля "code_1" и "code_2" в секции "code_trace".
2.	Запустить программу командой python main.py ct

Участок кода:
    
    ifstream file("graphFile");
    
    unsigned int n = 0;
    unsigned int oriented;
    file >> n >> oriented;

    G.resize(n);

    while (!file.eof()) {
        int a, b;
        file >> a;
        file >> b;

        G[a].push_back(b);
        if(oriented == 0) {
            G[b].push_back(a);
        }
    }

    file.close();

Параметры:

    "code_1" : "ifstream file ( "graphFile" ) ;"
    "code_2" : "file . close ( )"

Результаты тестирования:

    ========================================================================================
    Trace 0

    121:1 ifstream file ( "graphFile" ) ; -- CompoundStatement -->
    123:1 unsigned int n = 0 ; -- CompoundStatement -->
    124:1 unsigned int oriented ; -- CompoundStatement -->
    125:1 file >> n >> oriented -- CompoundStatement -->
    127:1 G . resize ( n ) -- CompoundStatement -->
    129:8 ! file . eof ( ) -- WhileStatement:False -->
    140:1 file . close ( )

    ========================================================================================
    Trace 1

    121:1 ifstream file ( "graphFile" ) ; -- CompoundStatement -->
    123:1 unsigned int n = 0 ; -- CompoundStatement -->
    124:1 unsigned int oriented ; -- CompoundStatement -->
    125:1 file >> n >> oriented -- CompoundStatement -->
    127:1 G . resize ( n ) -- CompoundStatement -->
    129:8 ! file . eof ( ) -- WhileStatement:True -->
    130:2 int a , b ; -- CompoundStatement -->
    131:2 file >> a -- CompoundStatement -->
    132:2 file >> b -- CompoundStatement -->
    134:2 G [ a ] . push_back ( b ) -- CompoundStatement -->
    135:5 oriented == 0 -- IfStatement:False -->
    129:8 ! file . eof ( ) -- WhileStatement:False -->
    140:1 file . close ( )

    ========================================================================================
    Trace 2

    121:1 ifstream file ( "graphFile" ) ; -- CompoundStatement -->
    123:1 unsigned int n = 0 ; -- CompoundStatement -->
    124:1 unsigned int oriented ; -- CompoundStatement -->
    125:1 file >> n >> oriented -- CompoundStatement -->
    127:1 G . resize ( n ) -- CompoundStatement -->
    129:8 ! file . eof ( ) -- WhileStatement:True -->
    130:2 int a , b ; -- CompoundStatement -->
    131:2 file >> a -- CompoundStatement -->
    132:2 file >> b -- CompoundStatement -->
    134:2 G [ a ] . push_back ( b ) -- CompoundStatement -->
    135:5 oriented == 0 -- IfStatement:True -->
    136:3 G [ b ] . push_back ( a ) -- CompoundStatement -->
    129:8 ! file . eof ( ) -- WhileStatement:False -->
    140:1 file . close ( )

    ========================================================================================
    time =  86.5544698447 seconds

Вывод: в результате работы программы были получены все возможные пути исполнения данного участка кода, включая все возможные результаты исполнения условных операторов. Эта возможность программы будет активно использоваться в дальнейшем.

### Тест №2

Цель: проверить способность программы получить список всех функциональных объектов проекта с указанием идентификатора объекта, места его создания, исходного кода создания и наименования самого объекта (идентификатор).

Последовательность действий оператора:

1.	Получить список функциональных объектов проекта, команда для запуска python main.py sfo functional_objects.txt.

Результаты тестирования:

    41 : 34:2:632:650 : int x = prevTop [ i ] ; -> x
    121 : 22:3:396:411 : int v = G [ u ] [ j ] ; -> v
    161 : 19:2:321:338 : int u = Q . front ( ) ; -> u
    195 : 14:1:225:258 : vector < int > prevTop ( G . size ( ) , - 1 ) ; -> prevTop
    209 : 13:1:188:222 : vector < int > distance ( G . size ( ) , - 1 ) ; -> distance
    223 : 12:1:173:185 : queue < int > Q ; -> Q
    338 : 56:3:1023:1038 : int v = G [ u ] [ j ] ; -> v
    378 : 53:2:948:965 : int u = Q . front ( ) ; -> u
    412 : 48:1:852:885 : vector < int > prevTop ( G . size ( ) , - 1 ) ; -> prevTop
    426 : 47:1:815:849 : vector < int > distance ( G . size ( ) , - 1 ) ; -> distance
    440 : 46:1:800:812 : queue < int > Q ; -> Q
    528 : 87:5:1669:1684 : int v = G [ u ] [ j ] ; -> v
    568 : 84:4:1588:1605 : int u = Q . front ( ) ; -> u
    630 : 78:1:1417:1439 : unsigned int count = 0 ; -> count
    637 : 76:1:1380:1413 : vector < int > prevTop ( G . size ( ) , - 1 ) ; -> prevTop
    651 : 75:1:1343:1377 : vector < int > distance ( G . size ( ) , - 1 ) ; -> distance
    665 : 74:1:1328:1340 : queue < int > Q ; -> Q
    745 : 36:2:698:716 : int x = prevTop [ i ] ; -> x
    863 : 18:1:293:322 : vector < char > topColor ( n , 'w' ) ; -> topColor
    870 : 17:1:267:290 : vector < int > time ( n , - 1 ) ; -> time
    879 : 16:1:238:264 : vector < int > prevTop ( n , - 1 ) ; -> prevTop
    888 : 15:1:208:235 : vector < int > distance ( n , - 1 ) ; -> distance
    897 : 13:1:188:204 : int n = G . size ( ) ; -> n
    1003 : 60:2:1102:1121 : int u = G [ start ] [ i ] ; -> u
    1244 : 93:2:1679:1689 : int w = - 1 ; -> w
    1253 : 91:2:1652:1674 : int u = S . top ( ) . second ; -> u
    1267 : 90:2:1627:1648 : int v = S . top ( ) . first ; -> v
    1322 : 83:1:1475:1499 : stack < pair < int , int > > S ; -> S
    1425 : 124:1:2222:2248 : vector < char > color ( n , 'w' ) ; -> color
    1432 : 123:1:2196:2219 : vector < int > resultOrder ; -> resultOrder
    1436 : 122:1:2177:2193 : int n = G . size ( ) ; -> n
    1607 : 144:2:2677:2687 : int w = - 1 ; -> w
    1616 : 142:2:2650:2672 : int u = S . top ( ) . second ; -> u
    1630 : 141:2:2625:2646 : int v = S . top ( ) . first ; -> v
    1675 : 136:1:2524:2548 : stack < pair < int , int > > S ; -> S
    1849 : 172:1:3122:3142 : vector < int > count ( n ) ; -> count
    1854 : 170:1:3096:3118 : graphNotWeighted GT ( n ) ; -> GT
    1859 : 169:1:3077:3093 : int n = G . size ( ) ; -> n
    2038 : 207:2:3887:3897 : int w = - 1 ; -> w
    2047 : 205:2:3860:3882 : int u = S . top ( ) . second ; -> u
    2061 : 204:2:3835:3856 : int v = S . top ( ) . first ; -> v
    2163 : 191:1:3559:3579 : bool isEmpty = false ; -> isEmpty
    2170 : 189:1:3519:3555 : graphNotWeighted component ( G . size ( ) ) ; -> component
    2180 : 188:1:3492:3516 : stack < pair < int , int > > S ; -> S
    2277 : 239:1:4483:4509 : vector < char > color ( n , 'w' ) ; -> color
    2284 : 238:1:4430:4480 : vector < graphNotWeighted > strongConnectedComponents ; -> strongConnectedComponents
    2288 : 236:1:4385:4426 : graphNotWeighted GT = transposingGraph ( G ) ; -> GT
    2300 : 234:1:4342:4381 : vector < int > order = topologySortInit ( G ) ; -> order
    2312 : 232:1:4322:4338 : int n = G . size ( ) ; -> n
    2403 : 109:3:2540:2588 : unsigned int count = connectedComponentsCount ( G ) ; -> count
    2438 : 100:3:2340:2375 : bool result = isConnected ( G , start ) ; -> result
    2456 : 97:3:2308:2317 : int start ; -> start
    2509 : 87:3:2056:2096 : vector < int > result = topologySortInit ( G ) ; -> result
    2577: 77:3:1749:1815 : vector < graphNotWeighted > components = strongConnectedComponents ( G ) ; -> components
    2607 : 71:3:1655:1667 : bool recFlag ; -> recFlag
    2633 : 64:3:1540:1549 : int start ; -> start
    2732 : 40:2:900:913 : string action ; -> action
    2817 : 20:1:363:378 : string fileName ; -> fileName
    2827 : 17:1:269:287 : graphNotWeighted G ; -> G
    2908 : 130:2:2933:2941 : int a , b ; -> b
    2939 : 124:1:2845:2866 : unsigned int oriented ; -> oriented
    2943 : 123:1:2824:2842 : unsigned int n = 0 ; -> n
    2950 : 121:1:2794:2820 : ifstream file ( "graphFile" ) ; -> file
    2908 : 130:2:2933:2941 : int a , b ; -> a

    time =  396.105171529 seconds

Вывод: Результат исполнения будет находиться в файле functional_objects.txt, указанном последним аргументом в команде вызова. В этом файле находится полный перечень всех функциональных объектов, готовых к использованию в других вызовах программы.

### Тест №3

Цель: проверить способность программы сформировать перечень маршрутов исполнения функциональных объектов.

Последовательность действий оператора:

1.	Получить список функциональных объектов проекта, команда для запуска python main.py sfo functional_objects.txt.
2.	В конфигурационном файле заполнить поля “code_1” и “code_2” в секции “code_trace”. В поле “code_1” необходимо указать исследуемый объект.
3.	Запустить программу командой python main.py ct

Участок кода:

    ifstream file("graphFile");

    unsigned int test = 123;
    unsigned int n = 0;
    unsigned int oriented;
    file >> n >> oriented;

    G.resize(n);

    while (!file.eof()) {
        int a, b;
        file >> a;
        file >> b;

        G[a].push_back(b);
        if(oriented == 0) {
            G[b].push_back(a);
        }
    }

    file.close();

Параметры запуска:

    "code_1" : "ifstream file ( "graphFile" ) ;"
    "code_2" : "file . close ( )"
    "functional_object_trace" : 1

Результат тестирования:

    get_trace_main start
    CODE_1 =  ifstream file ( \"graphFile\" ) ;
    CODE_2 =  file . close ( )	
    Get all path...  done.
    Get types of statements...  done.
    Get one functional object...  done.
    Get symbol of functional object...  done.
    Start checking fucntional object traces...
    Number of object for check:  1
    Symbols for check:  file
    done.
    ==================================================================================================
    Trace 0
    121:1 ifstream file ( "graphFile" ) ; -- CompoundStatement -->
    123:1 unsigned int test = 123 ; -- CompoundStatement -->
    124:1 unsigned int n = 0 ; -- CompoundStatement -->
    125:1 unsigned int oriented ; -- CompoundStatement -->
    126:1 file >> n >> oriented -- CompoundStatement -->
    128:1 G . resize ( n ) -- CompoundStatement -->
    130:8 ! file . eof ( ) -- WhileStatement:False -->
    141:1 file . close ( )
    ==================================================================================================
    Trace 1
    121:1 ifstream file ( "graphFile" ) ; -- CompoundStatement -->
    123:1 unsigned int test = 123 ; -- CompoundStatement -->
    124:1 unsigned int n = 0 ; -- CompoundStatement -->
    125:1 unsigned int oriented ; -- CompoundStatement -->
    126:1 file >> n >> oriented -- CompoundStatement -->
    128:1 G . resize ( n ) -- CompoundStatement -->
    130:8 ! file . eof ( ) -- WhileStatement:True -->
    131:2 int a , b ; -- CompoundStatement -->
    132:2 file >> a -- CompoundStatement -->
    133:2 file >> b -- CompoundStatement -->
    135:2 G [ a ] . push_back ( b ) -- CompoundStatement -->
    136:5 oriented == 0 -- IfStatement:False -->
    130:8 ! file . eof ( ) -- WhileStatement:False -->
    141:1 file . close ( )
    ==================================================================================================
    Trace 2
    121:1 ifstream file ( "graphFile" ) ; -- CompoundStatement -->
    123:1 unsigned int test = 123 ; -- CompoundStatement -->
    124:1 unsigned int n = 0 ; -- CompoundStatement -->
    125:1 unsigned int oriented ; -- CompoundStatement -->
    126:1 file >> n >> oriented -- CompoundStatement -->
    128:1 G . resize ( n ) -- CompoundStatement -->
    130:8 ! file . eof ( ) -- WhileStatement:True -->
    131:2 int a , b ; -- CompoundStatement -->
    132:2 file >> a -- CompoundStatement -->
    133:2 file >> b -- CompoundStatement -->
    135:2 G [ a ] . push_back ( b ) -- CompoundStatement -->
    136:5 oriented == 0 -- IfStatement:True -->
    137:3 G [ b ] . push_back ( a ) -- CompoundStatement -->
    130:8 ! file . eof ( ) -- WhileStatement:False -->
    141:1 file . close ( )
    ==================================================================================================
    time =  100.567015306 seconds

Параметры запуска:

    "code_1" : "unsigned int test = 123 ;"
    "code_2" : "file . close ( )"
    "functional_object_trace" : 1

Результат тестирования:

    get_trace_main start
    CODE_1 =  unsigned int test = 123 ;
    CODE_2 =  file . close ( )
    Get all path...  done.
    Get types of statements...  done.
    Get one functional object...  done.
    Get symbol of functional object...  done.
    Start checking fucntional object traces...
    Number of object for check:  1
    Symbols for check:  test
    done.
    There is no trace with functional object(s):
        2950 : 123:1:2824:2847 : unsigned int test = 123 ; -> test

Вывод: программа корректно возвращает результатом либо все маршруты исполнения исследуемого функционального объекта, либо сообщает о том что таких маршрутов не существует.
