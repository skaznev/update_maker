
    #---------- ПОДКЛЮЧАЕМ БИБЛИОТЕКИ ----------

import cx_Oracle as ora
from multiprocessing import Process
import datetime
import os

    #---------- КОНЕЦ: ПОДКЛЮЧАЕМ БИБЛИОТЕКИ ----------

    #---------- ОБЪЯВЛЯЕМ ПЕРЕМЕННЫЕ ----------

db          = ''        # база
user        = ''        # пользователь
ps          = ''        # пароль
threads_cnt = 5         # количетсво потоков
date_to     = r''''''   # дата с которой селектим
date_from   = r''''''   # дата по которую селектим
buff_size   = 2000000   # размер буфера, который держим в памяти (байт)
delim       = '|'       # разделитель в файле

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


    #---------- ФУНКЦИЯ ДОПИСЫВАНИЯ В ФАЙЛ ----------

def create_file(user, ps, db, sql, size, date_from, date_to, threads_cnt, mod, path):
    print(datetime.datetime.now())
    txt = ''
    ins_size = 0

    conn = ora.connect(user, ps, db)
    cur = conn.cursor()
    cur.execute(sql, {'date_from':date_from, 'date_to':date_to, 'threads_cnt':threads_cnt, 'mod':mod})
    
    while True:       
        i_txt = ''
        try:

            result = cur.fetchone()
            for item in result:
                i_txt += str(item) + delim                
            ins_size += utf8len(i_txt)
            if ins_size >= size:
                ins_size = utf8len(i_txt)
                with open(path + r'''.csv''' ,'a') as File:
                    File.write(txt)
                    txt = ''                
            txt += i_txt.replace('\n', '') + '\n'

        except Exception as e:
            with open(path + r'''.csv''' ,'a') as File:
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

    #---------- КОНЕЦ: ФУНКЦИЯ РАСКИДЫВАЮЩАЯ ЗАДАЧУ ПО ПОТОКАМ ----------

    #---------- КОНЕЦ: БЛОК ВСПОМОГАТЕЛЬНЫХ ФУНКЦИЙ ----------

    #---------- ГЛАВНАЯ ФУНКЦИЯ!!!!!!!!!! ----------

def execute(USER, PASSWORD, DB, WHAT, PATH, SQL, THREADS_CNT, DELIMITER, ):

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

    print(USER, PASSWORD, DB, WHAT, PATH, THREADS_CNT, SQL, DELIMITER)
    
    if what == 'Выполнить':
        start_script(user, ps, db, sql, threads_cnt)

    # elif WHAT == 'Выгрузить':
    #     path = os.path.join(PATH, date_from.replace('.', '-') +' TradeSec SPB1')
        
    #     with open(path + r'''.csv''' ,'w') as File_prev:
    #         File_prev.write(columns)
    #     File = open( path + r'''.csv''' ,'a')
        
    #     start(sql_spbex_stcks, buff_size, date_from, date_to, type_date, threads_cnt, path)


    #---------- КОНЕЦ: ГЛАВНАЯ ФУНКЦИЯ!!!!!!!!!! ----------
