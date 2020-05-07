
    #---------- ПОДКЛЮЧАЕМ БИБЛИОТЕКИ ----------

import cx_Oracle as ora
from multiprocessing import Process
import datetime
import os

    #---------- КОНЕЦ: ПОДКЛЮЧАЕМ БИБЛИОТЕКИ ----------

    #---------- ОБЪЯВЛЯЕМ ПЕРЕМЕННЫЕ ----------

db              = ''        # база
user            = ''        # пользователь
ps              = ''        # пароль
threads_cnt     = 5         # количетсво потоков
date_to         = r''''''   # дата с которой селектим
date_from       = r''''''   # дата по которую селектим
buff_size       = 2000000   # размер буфера, который держим в памяти (байт)
delim           = '|'       # разделитель в файле
i_log_id        = r'PRS_EXT_EXECUTOR.1'
sql_log_small   = r'''select * from ext_api_log WHERE key_name = :code_run'''
sql_log_full    = r'''select * from ext_api_log WHERE key_name = :code_run'''
full_logs_path  = 'logs'

try:
    with open('log.sql', 'r') as file:
        sql_log_small = file.read()                                    # Читаем с файла, вдруг че поменяют.
except:
    print('Не найден файл c логом log.sql.')

try:
    with open('log_to_file.sql', 'r') as file:
        sql_log_full = file.read()                                    # Читаем с файла, вдруг че поменяют.
except:
    print('Не найден файл c логом log_to_file.sql.')

    #---------- КОНЕЦ: ОБЪЯВЛЯЕМ ПЕРЕМЕННЫЕ ----------

    #---------- БЛОК ВСПОМОГАТЕЛЬНЫХ ФУНКЦИЙ ----------

    #---------- ФУНКЦИЯ ПОДСЧЕТА ДЛИНЫ СТРОКИ ----------

def utf8len(s):
    return len(s.encode('ANSI'))

    #---------- КОНЕЦ: ФУНКЦИЯ ПОДСЧЕТА ДЛИНЫ СТРОКИ ----------

def execute_oracle (user, ps, db, sql, threads_cnt, mod):
    print(datetime.datetime.now())

    conn = ora.connect(user, ps, db)
    cur = conn.cursor()
    if threads_cnt == 1:
        cur.execute(sql)
    else:
        cur.execute(sql, {'threads_cnt':threads_cnt, 'mod':mod})


    #---------- ФУНКЦИЯ ДОПИСЫВАНИЯ В ФАЙЛ ----------

def create_file(user, ps, db, sql, size, date_from, date_to, threads_cnt, mod, path, delimiter):
    print(datetime.datetime.now())
    txt = ''
    ins_size = 0

    conn = ora.connect(user, ps, db)
    cur = conn.cursor()
    if threads_cnt == 1:
        cur.execute(sql)
    else:
        cur.execute(sql, {'threads_cnt':threads_cnt, 'mod':mod})
    
    while True:       
        i_txt = ''
        try:

            result = cur.fetchone()
            for item in result:
                i_txt += str(item) + delimiter                
            ins_size += utf8len(i_txt)
            if ins_size >= size:
                ins_size = utf8len(i_txt)
                with open(path, 'a') as File:
                    File.write(txt)
                    txt = ''                
            txt += i_txt.replace('\n', '') + '\n'

        except Exception as e:
            with open(path, 'a') as File:
                    File.write(txt)
            print(datetime.datetime.now())
            conn.close()
            return

    #---------- КОНЕЦ: ФУНКЦИЯ ДОПИСЫВАНИЯ В ФАЙЛ ----------

    #---------- ФУНКЦИЯ РАСКИДЫВАЮЩАЯ ЗАДАЧУ ПО ПОТОКАМ ----------

def start_script(user, ps, db, sql, threads_cnt):
    threads = []

    for i in range(threads_cnt):
        thread = Process(target=execute_oracle, args=(user, ps, db, sql, threads_cnt, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def start_select(user, ps, db, sql, buff_size, threads_cnt, path, delimiter):
    threads = []

    for i in range(threads_cnt):
        thread = Process(target=create_file, args=(user, ps, db, sql, buff_size, threads_cnt, i, path, delimiter))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    #---------- КОНЕЦ: ФУНКЦИЯ РАСКИДЫВАЮЩАЯ ЗАДАЧУ ПО ПОТОКАМ ----------

    #---------- ФУНКЦИЯ СЧИТАЙ ЛОГИ ----------

def read_log (user, ps, db, CODE, sql_name):
    global sql_log_small
    global sql_log_full
    global delim
    conn = ora.connect(user, ps, db)
    cur = conn.cursor()

    # Замутим сначала коротких логов для морды
    log = ''
    cur.execute(sql_log_small, {'code_run':CODE})
    logs = cur.fetchall()
    for rec in logs:
        for item in rec:
            log += str(item)
        log += '\n'

    # А теперь полные логи считаем в файл
    log_full = ''
    cur.execute(sql_log_full, {'code_run':CODE})
    logs = cur.fetchall()
    for rec in logs:
        for item in rec:
            log_full += str(item) + delim
        log_full += '\n'
    with open(os.path.join(os.getcwd(), full_logs_path) + r'\\' + sql_name + '_' + CODE + r'''.txt''' ,'w', encoding= 'Windows-1251') as File:
        File.write(log_full)

    conn.close()
    return log

    #---------- КОНЕЦ: ФУНКЦИЯ СЧИТАЙ ЛОГИ ----------

    #---------- КОНЕЦ: БЛОК ВСПОМОГАТЕЛЬНЫХ ФУНКЦИЙ ----------

    #---------- ГЛАВНАЯ ФУНКЦИЯ!!!!!!!!!! ----------

def execute(USER, PASSWORD, DB, WHAT, PATH, SQL_NAME, SQL, THREADS_CNT, DELIMITER, COLUMNS, CODE_RUN):

    global buff_size
    global threads_cnt
    global columns
    global sql
    
    user        = USER
    ps          = PASSWORD
    db          = DB
    what        = WHAT
    path        = PATH
    threads_cnt = int(THREADS_CNT)
    sql         = SQL
    delimiter   = DELIMITER
    columns     = COLUMNS.replace(delim,delimiter)
    code_run    = CODE_RUN
    sql_name    = SQL_NAME
    logs        =''
    
    if what == 'Выполнить':
        start_script(user, ps, db, sql, threads_cnt)
        logs = read_log(user, ps, db, code_run, sql_name)

    elif WHAT == 'Выгрузить':
        with open(path, 'w') as File_prev:
            File_prev.write(columns)
        File = open(path, 'a')
        start_select(user, ps, db, sql, buff_size, threads_cnt, path, delimiter)

    return logs
    #---------- КОНЕЦ: ГЛАВНАЯ ФУНКЦИЯ!!!!!!!!!! ----------
