import cx_Oracle as ora
from multiprocessing import Process
import datetime

db          = ''
user        = ''
ps          = ''
threads_cnt = 1
size        = 0
n           = 0
i_text      = r''''''
text        = r''''''
path        = r'''C:\\Temp\\oracle\\report'''
file_name   = 0
q           = 0
delim       = ';'
sql         = r'''
select * from 
(select rownum rn
, pay.ticket_id
from v_tr_pay_cat pay
join v_tr_acc_cat acc on acc.id = pay.acc_id
join v_tr_sec_agreement agr on agr.id = acc.agr_id
where pay.trn_type_id = 6693
and pay.value_date = '10.04.2020'
and agr.agreement_num in (select code from fund_db.tcs_fund_cl_code)
and not exists (
select 1 from v_tr_doc_cat doc
where doc.ticket_id = pay.ticket_id
and doc.entry_date = to_date('10.04.2020', 'dd.mm.yyyy')))
           where mod(rn, :threads_cnt) = :mod'''

# conn = ora.connect(user_dev, ps_dev, db)
# cur = conn.cursor()
# cur.execute(sql)
# cur.execute(sql, {threads_cnt:threads_cnt, mod:mod})

def utf8len(s):
    return len(s.encode('ANSI'))

def create_file(sql, threads_cnt, mod):
    txt = ''
    conn = ora.connect(user, ps, db)
    cur = conn.cursor()
    cur.execute(sql, {'threads_cnt':threads_cnt, 'mod':mod})
    while True:       
        i_txt = ''
        try:
            result = cur.fetchone()
            if result == None:
                with open( path + r'''.csv''' ,'a') as File:
                    File.write(txt)
                conn.close()
                return
        except Exception as e:
            with open( path + r'''.csv''' ,'a') as File:
                File.write(txt)
            conn.close()
            return
        for item in result:
            i_txt += str(item).replace('\n', ' ') + delim  
        txt += i_txt + '\n'

File_prev =  open( path + r'''.csv''' ,'w')


create_file(sql, threads_cnt, 0)

# if __name__ == "__main__":


#     threads = []
#     for i in range(threads_cnt):
#         thread = Process(target=create_file, args=(sql, threads_cnt, i,))
#         threads.append(thread)
#         thread.start()

#     for thread in threads:
#         thread.join()


# def wrt (size, mod, mod_all, file_pref, beg_text=''):
#     global lock
#     bl = True
#     i_txt = ''
#     txt = ''
#     ins_size = 0
#     while bl:
#         i_txt = ''
#         if beg_text != '':
#             ins_size += utf8len(beg_text)
#             txt = beg_text + '\n'
#             beg_text = '' 
#         result = cur.fetchone()
#         # try:
#         #     while lock == True:
#         #         print("thread #" + str(mod) + " waiting")
#         #     lock = True
#         #     print("locked by thread #" + str(mod))
#         #     result = cur.fetchone()
#         #     lock = False
#         #     print("unlocked by thread #" + str(mod))
#         # except Exception as e:
#         #     print(e.__class__)
#         #     print(e)
#         #     return
#         for item in result:
#             i_txt += str(item) + delim
#         ins_size += utf8len(i_txt)
#         if ins_size >= size:
#             with open( path + str(file_pref) + r'''.txt''' ,'w') as File:
#                 File.write(txt)
#             file_pref += mod_all
#             bl = False
#         txt += i_txt + '\n'
#     wrt(size, mod_all, file_pref, i_txt)


# while True:
#     result = cur.fetchmany(numRows=1)
#     if result == []:
#         break
#     for i in result:
#         for item in i:
#             i_text += str(item) + delim
#         size += utf8len(i_text)
#         if size > const:
#             file_name += 1
#             size = utf8len(i_text)
#             with open( path + str(file_name) + r'''.txt''' ,'w') as File:
#                 File.write(text)
#             text = ''
#         text += i_text + '\n'
#         i_text = ''
#         q = 0
#         n += 1
#         # print (n)

# cur.close()
# conn.close()
# print('end')