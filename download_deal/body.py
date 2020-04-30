
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
buff_size   = 2000000   # размер буфера, который держим в памяти
delim       = ';'       # разделитель в файле

    #---------- КОНЕЦ: ОБЪЯВЛЯЕМ ПЕРЕМЕННЫЕ ----------

    #---------- ЧИТАЕМ ФАЙЛЫ С КОНФИГОМ ----------

with open( 'columns.sql' ,'r') as file:
    columns = file.read()

with open( 'SELECT MOEX_STCKS.sql' ,'r') as file:
    sql_moex_stcks = file.read()

with open( 'SELECT SPBEX_STCKS.sql' ,'r') as file:
    sql_spbex_stcks = file.read()

    #---------- КОНЕЦ: ЧИТАЕМ ФАЙЛЫ С КОНФИГОМ ----------


    #---------- БЛОК ВСПОМОГАТЕЛЬНЫХ ФУНКЦИЙ ----------

    #---------- ФУНКЦИЯ ПОДСЧЕТА ДЛИНЫ СТРОКИ ----------

def utf8len(s):
    return len(s.encode('ANSI'))

    #---------- КОНЕЦ: ФУНКЦИЯ ПОДСЧЕТА ДЛИНЫ СТРОКИ ----------

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

def start(user, ps, db, sql, buff_size, date_from, date_to, type_date, threads_cnt, path):
    threads = []

    for i in range(threads_cnt):
        thread = Process(target=create_file, args=(user, ps, db, sql, buff_size, date_from, date_to, threads_cnt, i, path, ))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    #---------- КОНЕЦ: ФУНКЦИЯ РАСКИДЫВАЮЩАЯ ЗАДАЧУ ПО ПОТОКАМ ----------

    #---------- КОНЕЦ: БЛОК ВСПОМОГАТЕЛЬНЫХ ФУНКЦИЙ ----------

    #---------- ГЛАВНАЯ ФУНКЦИЯ!!!!!!!!!! ----------

def execute(USER, PASSWORD, DB, DATE_FROM, DATE_TO, TYPE_DATE, WHAT, PATH):

    global buff_size
    global threads_cnt
    global columns
    global sql_moex_stcks
    global sql_spbex_stcks
    
    user        = USER
    ps          = PASSWORD
    db          = DB
    date_from   = DATE_FROM
    date_to     = DATE_TO
    type_date   = TYPE_DATE
    
    if type_date == 'Дата торгов':
        sql_moex_stcks  = sql_moex_stcks.replace('$date$','DIL.trade_date_time')
        sql_spbex_stcks = sql_spbex_stcks.replace('$date$','DIL.trade_date_time')
    else:
        sql_moex_stcks  = sql_moex_stcks.replace('$date$','DIL.clear_value_date_time')
        sql_spbex_stcks = sql_spbex_stcks.replace('$date$','DIL.clear_value_date_time')
    
    if WHAT == 'ФР ММВБ':
        path = os.path.join(PATH, date_from.replace('.', '-') +' TradeSec MOEX1')
        
        with open(path + r'''.csv''' ,'w') as File_prev:
            File_prev.write(columns)
        
        File = open(path + r'''.csv''' ,'a')
        
        start(user, ps, db, sql_moex_stcks, buff_size, date_from, date_to, type_date, threads_cnt, path)

    elif WHAT == 'ФР СПБ':
        path = os.path.join(PATH, date_from.replace('.', '-') +' TradeSec SPB1')
        
        with open(path + r'''.csv''' ,'w') as File_prev:
            File_prev.write(columns)
        File = open( path + r'''.csv''' ,'a')
        
        start(sql_spbex_stcks, buff_size, date_from, date_to, type_date, threads_cnt, path)

    elif WHAT == 'Всё':
        path_moex   = os.path.join(PATH, date_from.replace('.', '-') +' TradeSec MOEX1')
        path_spbex  = os.path.join(PATH, date_from.replace('.', '-') +' TradeSec SPB1')
        
        with open(path_moex + r'''.csv''' ,'w') as File_prev:
            File_prev.write(columns)
        with open(path_spbex + r'''.csv''' ,'w') as File_prev:
            File_prev.write(columns)
        
        File = open(path_moex + r'''.csv''' ,'a')
        File = open(path_spbex + r'''.csv''' ,'a')

        start(user, ps, db, sql_moex_stcks, buff_size, date_from, date_to, type_date, threads_cnt, path_moex)
        start(user, ps, db, sql_spbex_stcks, buff_size, date_from , date_to, type_date, threads_cnt, path_spbex)

    #---------- КОНЕЦ: ГЛАВНАЯ ФУНКЦИЯ!!!!!!!!!! ----------
