#---------- ПОДКЛЮЧАЕМ БИБЛИОТЕКИ ----------
import os
import sys
import time
import shutil
import subprocess
import cx_Oracle as oracle
try:
    from msvcrt import getch
    def getpass(prompt):
        """Replacement for getpass.getpass() which prints asterisks for each character typed"""
        print(prompt, end='', flush=True)
        buf = b''
        while True:
            ch = getch()
            if ch in {b'\n', b'\r', b'\r\n'}:
                print('')
                break
            elif ch == b'\x08': # Backspace
                buf = buf[:-1]
                print(f'\r{(len(prompt)+len(buf)+1)*" "}\r{prompt}{"*" * len(buf)}', end='', flush=True)
            elif ch == b'\x03': # Ctrl+C
                raise KeyboardInterrupt
            else:
                buf += ch
                print('*', end='', flush=True)
        return buf.decode(encoding='utf-8')
except ImportError:
    from getpass import getpass
#---------- КОНЕЦ ПОДКЛЮЧЕНИЯ БИБЛИОТЕК ----------


#---------- ОБЪЯВЛЯЕМ ПЕРЕМЕННЫЕ ----------
CONST_NEW_LINE    = '\n'
CONST_CONFIG_FILE = ''
CONST_BASE, CONST_LOGIN, CONST_FOLDER, CONST_PATH = 'base', 'login', 'folder', 'path'

parameter_dictionary = {}

if len ( sys.argv ) > 1:
    CONST_CONFIG_FILE = sys.argv[1]
else:
    CONST_CONFIG_FILE = 'config.txt'

# try:
#     with open('set.txt', 'r') as file:
#         os.environ["PATH"] = file.read()                    # Выставляем переменную окружения, что б cx_oracle не ругался
# except:
#     print('Не найден файл настроек set.txt. PATH: ' + os.environ["PATH"] )

try:
    with open ( file = CONST_CONFIG_FILE, mode = 'r' ) as file:
        for line in file:
            line_array = line.split ( sep = ' = ', maxsplit = 1 )
            parameter_dictionary [ line_array [ 0 ] ] = line_array [ 1 ].rstrip ( CONST_NEW_LINE )
except:
    print('Не найден файл настроек ' + CONST_CONFIG_FILE + '. PATH: ' + os.environ["PATH"] )

os.environ["PATH"] = parameter_dictionary [ CONST_PATH ]    # Выставляем переменную окружения, что б cx_oracle не ругался

path_app    = os.getcwd()                                   # Текущая директория
path        = parameter_dictionary [ CONST_FOLDER ]         # Директория с объектами для патча.
path_build  = os.path.join(path_app , 'objects')            # Директория с патчем.             

# db          = ''
# user_dev    = ''
# ps_dev      = ''

# if True:

#print(getpass('password:'))
conn = oracle.connect (
           parameter_dictionary [ CONST_LOGIN ],
           # input ( 'password:' ),
           # getpass.getpass('password:'),
           getpass('password:'),
           parameter_dictionary [ CONST_BASE ]
       )
cur  = conn.cursor()
# else: # Ещё один вариант создать коннект.
#     my_dsn  = oracle.makedsn ( "m1-db-tst30.tcsbank.ru", 1522, sid = "XXI_ENC" )
#     conn    = oracle.connect ( user = user_dev, password = ps_dev, dsn = my_dsn )
#     cur     = conn.cursor()

#---------- КОНЕЦ ОБЪЯВЛЕНИЯ ПЕРЕМЕННЫХ ----------


#---------- РАБОТАЕМ С КАТАЛОГАМИ (СОЗДАЕМ ДИРЕКТОРИЮ В КОТОРУЮ НАЧИТЫВАЕМ ОБЪЕКТЫ С БАЗЫ) ----------

shutil.rmtree(path_build, ignore_errors=True)
os.makedirs(path_build)

#---------- КОНЕЦ РАБОТЫ С ДИРЕКТОРИЯМИ ----------


#---------- ОБЪЯВЛЕНИЕ ФУНКЦИИ "МЕТНИСТЬ ПОСМОТРИ ЧТО С ЭТИМ ОБЪЕКТОМ" ----------

def push (type = '' , object = ''):

#---------- РЕЖЕМ ИМЯ ОБЪЕКТА ЧТО Б СЧИТАТЬ ЕГО С БАЗЫ ----------    

    obj = object.upper()
    if type == 'PACKAGE_BODY':
        obj = obj[:obj.find(r'_B.SQL') ]
    else:
        obj = obj[:obj.find(r'.SQL') ]

#---------- КОНЕЦ ОБРЕЗАНИЯ ИМЕНИ ----------


#---------- ОБРАЩАЕМСЯ К БАЗЕ ----------

    print ('Обработка объекта: ' + type + ' ' + obj)
    clob = cur.callfunc("dbms_metadata.get_ddl", oracle.CLOB,(type, obj))
    text = clob.read()

#---------- КОНЕЦ ОБРАЩЕНИЯ К БАЗЕ ----------


#---------- СОХРАНЯЕМ ФАЙЛ И ЗАТЕМ ЧИТАЕМ ИЗ НЕГО ТЕКСТ ----------

    i_file  = open(os.path.join(path_build , object) ,  "w", encoding = "windows-1251")
    i_file.write(text)
    i_file.close()

    i_file  = open(os.path.join(path_build , object) ,  "r", encoding = "windows-1251")
    i_file_text1 = i_file.read().split('\n')
    i_file.close()

    i_file  = open(os.path.join(path , object) ,  "r", encoding = "windows-1251")
    i_file_text2 = i_file.read().split('\n')
    i_file.close()

#---------- КОНЕЦ РАБОТЫ С ФАЙЛОМ ----------


#---------- ДОСТАНЕМ СЕРДЦЕВИНЫ ОБЪЕКТОВ, ВДРУГ ОНИ СОВПАДАЮТ ----------
    
    i_file1 = body(i_file_text1, 3, 0)
    i_file2 = body(i_file_text2, 2, 0)

#---------- КОНЕЦ ДОСТАВАНИЯ СЕРДЦЕВИНЫ ----------


#---------- ЕСЛИ ФАЙЛЫ НЕ ИДЕНТИЧНЫ, ТО ВЫЗОВЕМ УТИЛИТУ СРАВНЕНИЯ ----------

    if not i_file1 == i_file2:
        print ('Состояние файла расходится с базой!')
        calling = 'WinMergePortable' + ' ' + os.path.join(path , object) + ' ' + os.path.join(path_build , object)
        #process = subprocess.Popen(calling)
        subprocess.Popen(calling)
        time.sleep(1)   # Иначе винмердж выпендривается что не может 2 программы одновременно открывать

#---------- КОНЕЦ БЛОКА СРАВНЕНИЯ ----------


#---------- КОНЕЦ ФУНКЦИИ "МЕТНИСЬ С ОБЪЕКТОМ" ----------


#---------- ФУНКЦИЯ ВОЗВРАЩАЮЩАЯ ТЕЛО ОБЪЕКТА ----------

def body (input_text , first , end):
    
    i_length = sum(1 for line in input_text)
    step = 0
    body_text = ''
    
    for line in input_text:
        step += 1
        if (step < first) or (step > (i_length - end)):
            continue
        elif ((i_length - 4) < step) and (r'---' in line):
            step = i_length
        else:
            body_text += line + '\n'
    
    return body_text

#---------- КОНЕЦ ФУНКЦИИ ВОЗВРАЩАЮЩЕЙ ТЕЛО ----------


#---------- ТЕЛО ПРОГРАММЫ - ЧИТАЕМ КАТАЛОГ И ДЕРГАЕМСЯ ПО ОБЪЕКТАМ ----------

# path = input('Введи директорию TCS:')

files = os.listdir ( path )
all_files = [f for f in files if ( f.upper()[-4:] in [".SQL"])]
for file in all_files:
    try:
        if (r'METADATA.SQL' == file.upper()) or (r'SCRIPT.SQL' == file.upper()) or (r'TABLE.SQL' == file.upper()):
            continue
        elif (r'_B.SQL' in file.upper()) or (r'TR_TOOL_METADATA_B.SQL' in file.upper()):
            push('PACKAGE_BODY', file)
        elif r'V_T' in file.upper():
            push('VIEW', file)
        else:
            push('PACKAGE_SPEC', file)
    except:
        print ('Произошла ошибка при обработке ' + file)
        continue
end = input('Обработка завершена')

#---------- КОНЕЦ ТЕЛА ПРОГРАММЫ ----------