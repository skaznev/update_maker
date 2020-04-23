import cx_Oracle as ora
from multiprocessing import Process
from multiprocessing import freeze_support
import datetime


db          = ''
user        = ''
ps          = ''
threads_cnt = 5
size        = 0
n           = 0
i_text      = r''''''
text        = r''''''
date        = r'''15.05.2018'''
path        = r'''C:\\Temp\\oracle\\'''
q           = 0
buff_size   = 2000000
delim       = '|'
sql_bal     = r'''select    party_name,
                            agr_num,
                            dpa_p_code,
                            issuer_name,
                            sha_sort_name,
                            sha_isin,
                            rda_p_code,
                            dpa_a_code,
                            rda_a_code,
                            sec_amount
                  from          
                  (select   rownum rn,
                            bal.party_name,
                            bal.agr_num,
                            bal.dpa_p_code,
                            bal.issuer_name,
                            bal.sha_sort_name,
                            bal.sha_isin,
                            bal.rda_p_code,
                            bal.dpa_a_code,
                            bal.rda_a_code,
                            bal.sec_amount
                        from 
                        v_tr_dt_report_oper_created cr,
                        V_TR_DT_REP_JROD_REST bal
                        where cr.report_id = bal.inq_id
                        and cr.report_date = :rep_date)
                    where mod(rn, :threads_cnt) = :mod'''

sql_oper      = r'''select                  op.party_name,
                                            op.agr_num,
                                            op.dpa_p_code,   
                                            op.value_date, 
                                            op.rda_p_code,
                                            op.dpa_a_code,
                                            op.rda_a_code,
                                            op.issuer_name,
                                            op.sha_sort_name,
                                            op.sha_code,
                                            op.rest_in,
                                            op.turn_deb,
                                            op.turn_cred,
                                            op.rest_out,
                                            op.c_dpa_p_code,
                                            op.memo,
                                            op.oper_type                       
                    from
                    v_tr_dt_report_oper_created cr,
                    V_TR_DT_REP_JROD op
                    where cr.report_id = op.inq_id
                    and cr.report_date = to_date(:rep_date, 'dd.mm.yyyy')
                    and mod(op.id, :threads_cnt) = :mod'''

def utf8len(s):
    return len(s.encode('ANSI'))

def check_report(date, cur):
    cur.execute('''select count(1) from v_tr_dt_report_oper_created
                    where report_date = to_date(:rep_date, 'dd.mm.yyyy')''', {'rep_date':date})
    result = cur.fetchone()[0]
    return result

def create_file(user, ps, db, sql, size, rep_date, threads_cnt, mod, path):
    print(datetime.datetime.now())
    user = user
    ps = ps
    db = db
    txt = ''
    ins_size = 0
    conn = ora.connect(user, ps, db)
    cur = conn.cursor()
    cur.execute(sql, {'rep_date':rep_date, 'threads_cnt':threads_cnt, 'mod':mod})
    while True:       
        i_txt = ''
        try:
            result = cur.fetchone()
            for item in result:
                i_txt += str(item) + delim                
            ins_size += utf8len(i_txt)
            if ins_size >= size:
                ins_size = utf8len(i_txt)
                with open( path + r'''.csv''' ,'a') as File:
                    File.write(txt)
                    txt = ''                
            txt += i_txt.replace('\n', '') + '\n'
        except Exception as e:
            with open( path + r'''.csv''' ,'a') as File:
                    File.write(txt)
            print(datetime.datetime.now())
            conn.close()
            return

def create_report (user, ps, db, date, if_nulls, user_id):

    conn = ora.connect(user, ps, db)
    cur = conn.cursor()
    
    res = cur.var(ora.NUMBER)
    msg = cur.var(ora.STRING)

    try:
        cur.callproc("tr_api_report.dt_report_operations_create", (date, if_nulls, user_id, res, msg))
        conn.commit()
    except Exception as e:
        conn.close()
        raise

    conn.close()    



def start(user, ps, db, sql, buff_size, date, threads_cnt, path):

    threads = []
    for i in range(threads_cnt):
        thread = Process(target=create_file, args=(user, ps, db, sql, buff_size, date, threads_cnt, i, path, ))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def execute(USER, PASSWORD, DB, DATE, PATH, WHAT, ACTION, IF_NULLS, USER_ID, USER_STR):

    global sql
    global buff_size
    global threads_cnt

    user = USER
    ps   = PASSWORD
    db   = DB
    date = DATE
    if_nulls = IF_NULLS
    user_id = USER_ID
    user_str = USER_STR

    if ACTION == 'Сформировать и выгрузить' or ACTION == 'Сформировать':
        try:
            create_report(user, ps, db, date, if_nulls, user_id)
        except Exception as e:
            raise
    
    if ACTION == 'Сформировать и выгрузить' or ACTION == 'Выгрузить':
        if WHAT == 'Остатки':
            path = PATH + date.replace('.', '') +'_rest'
            with open( path + r'''.csv''' ,'w') as File_prev:
                File_prev.write('Наименование депонента|Номер договора депо|Номер счета депо|Наименование эмитента|Категория, вид ценной бумаги|Гос. рег. номер/ISIN|Раздел счета депо|Место хранения|Раздел места хранения|Количество ценных бумаг\n')
            File = open( path + r'''.csv''' ,'a')
            start(user, ps, db, sql_bal, buff_size, date, threads_cnt, path)
            File.write(user_str)

        elif WHAT == 'Операции':
            path = PATH + date.replace('.', '') + '_oper'
            with open( path + r'''.csv''' ,'w') as File_prev:
                File_prev.write('Наименование депонента|Номер договора депо|Номер счета депо|Дата операции|Раздел счета депо|Место хранения|Раздел места хранения|Наименование эмитента|Категория, вид ценной бумаги|Гос. рег. номер/ISIN|Входящий остаток, шт|Оборот по дебету|Оборот по кредиту|Исходящий остаток, шт|Корреспондирующий счет|Основание операции|Тип поручения\n')
            File = open( path + r'''.csv''' ,'a')
            start(user, ps, db, sql_oper, buff_size, date, threads_cnt, path)
            File.write(user_str)

        elif WHAT == 'Всё':
            threads_cnt = 3
            path_bal = PATH + date.replace('.', '') +'_rest'
            path_oper = PATH + date.replace('.', '') + '_oper'    
            with open( path_bal + r'''.csv''' ,'w') as File_prev:
                File_prev.write('Наименование депонента|Номер договора депо|Номер счета депо|Наименование эмитента|Категория, вид ценной бумаги|Гос. рег. номер/ISIN|Раздел счета депо|Место хранения|Раздел места хранения|Количество ценных бумаг\n')
            with open( path_oper + r'''.csv''' ,'w') as File_prev:
                File_prev.write('Наименование депонента|Номер договора депо|Номер счета депо|Дата операции|Раздел счета депо|Место хранения|Раздел места хранения|Наименование эмитента|Категория, вид ценной бумаги|Гос. рег. номер/ISIN|Входящий остаток, шт|Оборот по дебету|Оборот по кредиту|Исходящий остаток, шт|Корреспондирующий счет|Основание операции|Тип поручения\n')
            File_bal = open( path_bal + r'''.csv''' ,'a')
            File_oper = open( path_oper + r'''.csv''' ,'a')

            start(user, ps, db, sql_bal, buff_size, date, threads_cnt, path_bal)
            start(user, ps, db, sql_oper, buff_size, date, threads_cnt, path_oper)

            File_bal.write(user_str)
            File_oper.write(user_str)
    
# if __name__ == '__main__':
#                 freeze_support()
#                 execute(user, ps, db, date, path, 'Всё', 'Сформировать и выгрузить', 82, 361468, 'Huy')

