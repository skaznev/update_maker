
    #---------- ПОДКЛЮЧАЕМ БИБЛИОТЕКИ ----------

import cx_Oracle as ora
from multiprocessing import Process , Value , Lock
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
lenght_file     = 0
cut             = 1000000    # Кол-во строк для обрезки файла

# Определим заодно крутой многопроцессинговый счетчик отфетчиных строк
class Counter(object):
    def __init__(self, initval=0):
        self.val = Value('i', initval)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    def reset(self):
        with self.lock:
            self.val.value = 0

    def value(self):
        with self.lock:
            return self.val.value

try:
    with open('log.sql', 'r') as file:
        sql_log_small = file.read()                                   # Читаем с файла, вдруг че поменяют.
except:
    print('Не найден файл c логом log.sql.')

try:
    with open('log_to_file.sql', 'r') as file:
        sql_log_full = file.read()                                    # Читаем с файла, вдруг че поменяют.
except:
    print('Не найден файл c логом log_to_file.sql.')

    #---------- КОНЕЦ: ОБЪЯВЛЯЕМ ПЕРЕМЕННЫЕ ----------

    #---------- БЛОК ВСПОМОГАТЕЛЬНЫХ ФУНКЦИЙ ----------

    #---------- ФУНКЦИЯ ПЕРЕВОДА ЗНАЧЕНИЙ В НОРМАЛЬНЫЙ ВИД ----------

def nvl(a):
    if a is None:
        return ' '
    else:
        return(str(a))

    #---------- КОНЕЦ: ФУНКЦИЯ ПЕРЕВОДА ЗНАЧЕНИЙ В НОРМАЛЬНЫЙ ВИД ----------

    #---------- ФУНКЦИЯ ПОДСЧЕТА ДЛИНЫ СТРОКИ ----------

def utf8len(s):
    return len(s.encode('ANSI'))

    #---------- КОНЕЦ: ФУНКЦИЯ ПОДСЧЕТА ДЛИНЫ СТРОКИ ----------

#---------- ФУНКЦИЯ ЗАПУСК КОННЕКТА ----------

def execute_oracle (user, ps, db, sql, threads_cnt, mod):
    print(datetime.datetime.now())

    conn = ora.connect(user, ps, db)
    cur = conn.cursor()
    if threads_cnt == 1:
        cur.execute(sql)
    else:
        cur.execute(sql, {'threads_cnt':threads_cnt, 'mod':mod})

    #---------- КОНЕЦ: ФУНКЦИЯ ЗАПУСК КОННЕКТА ----------

    #---------- ФУНКЦИЯ ДОПИСЫВАНИЯ В ФАЙЛ ----------

def create_file(user, ps, db, sql, size, threads_cnt, mod, path, delimiter, V):
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
            lenght = len(result)
            
            # Пополним счетчик отфетчиных строк на +1
            V.increment() 

            for i,item in enumerate(result):
                i_txt += nvl(item) 
                if i <  (lenght - 1):
                    i_txt += delimiter                
            ins_size += utf8len(i_txt)
            if ins_size >= size:
                ins_size = utf8len(i_txt)
                try:
                    with open(path, 'a') as File:
                        File.write(txt)
                        txt = ''                
                except Exception as e:
                    print(e)        
            txt += i_txt.replace('\n', '') + '\n'

        except Exception as e:
            try:
                with open(path, 'a') as File:
                        File.write(txt)
            except Exception as e:
                print(e)               
            print(datetime.datetime.now())
            conn.close()
            return

    #---------- КОНЕЦ: ФУНКЦИЯ ДОПИСЫВАНИЯ В ФАЙЛ ----------

    #---------- ФУНКЦИИ РАСКИДЫВАЮЩЧЮ ЗАДАЧУ ПО ПОТОКАМ ----------

def start_script(user, ps, db, sql, threads_cnt):
    threads = []

    for i in range(threads_cnt):
        thread = Process(target=execute_oracle, args=(user, ps, db, sql, threads_cnt, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def start_select(user, ps, db, sql, buff_size, threads_cnt, path, delimiter, V):
    threads = []

    for i in range(threads_cnt):
        thread = Process(target=create_file, args=(user, ps, db, sql, buff_size, threads_cnt, i, path, delimiter, V))
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
            log += nvl(item)
        log += '\n'

    # А теперь полные логи считаем в файл
    log_full = ''
    cur.execute(sql_log_full, {'code_run':CODE})
    logs = cur.fetchall()
    for rec in logs:
        for item in rec:
            log_full += nvl(item) + delim
        log_full += '\n'
    with open(os.path.join(os.getcwd(), full_logs_path) + r'\\' + sql_name + '_' + CODE + r'''.txt''' ,'w', encoding= 'Windows-1251') as File:
        File.write(log_full)

    conn.close()
    return log

    #---------- КОНЕЦ: ФУНКЦИЯ СЧИТАЙ ЛОГИ ----------

    #---------- ФУНКЦИЯ ПОДСЧЕТА КОЛ-ВА СТРОК В ФРАКЦИИ ----------

def for_fract(x, y, z):
    global cut
    if x < y-1:
        return cut-1 # так как первая строка заголовок, а последняя пустая
    return z%cut

    #---------- КОНЕЦ: ФУНКЦИЯ КОЛ-ВА СТРОК В ФРАКЦИИ ----------

    #---------- КОНЕЦ: БЛОК ВСПОМОГАТЕЛЬНЫХ ФУНКЦИЙ ----------



    #---------- ГЛАВНАЯ ФУНКЦИЯ!!!!!!!!!! ----------



def execute(USER, PASSWORD, DB, WHAT, PATH, SQL_NAME, SQL, THREADS_CNT, DELIMITER, COLUMNS, CODE_RUN):

    global buff_size
    global threads_cnt
    global columns
    global sql
    global cut

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
    
    # Объявим счетчик строк
    v = Counter(0)
    
    if what == 'Выполнить':
        start_script(user, ps, db, sql, threads_cnt)
        logs = read_log(user, ps, db, code_run, sql_name)

    elif WHAT == 'Выгрузить':
        with open(path, 'w') as File_prev:
            File_prev.write(columns +'\n')
        
        File = open(path, 'a')
        start_select(user, ps, db, sql, buff_size, threads_cnt, path, delimiter, v)
        
        # кол-во строк в файле (отфетченные + 1 строка (заголовок))
        lenght_file = v.value()+1  

        # Если строк больше 1млн то дробим файл на части
        if lenght_file > cut:    
            with open(path, 'r', encoding= 'Windows-1251') as File_pre:
                if_1 = True
                # Посчитаем количество фракций на которые мы дробим файл
                fract_all = lenght_file//cut + 1
                # Распилим биг файл на много мелких
                for i in range(fract_all):     
                    fract = [next(File_pre) for x in range(for_fract(i, fract_all, lenght_file))]
                    with open(path[:-4] + '_' + str(i) + r'.csv', 'w', encoding= 'Windows-1251') as File_post:
                        # В первом файле и так есть шапка с колонками
                        if not if_1:
                            File_post.write(columns +'\n')
                        if_1= False
                        for f in fract:
                            File_post.write(f)
                        
    # Обнулим счетчик строк
    v.reset()
    
    return logs
    
    #---------- КОНЕЦ: ГЛАВНАЯ ФУНКЦИЯ!!!!!!!!!! ----------
