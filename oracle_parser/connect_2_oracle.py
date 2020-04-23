import cx_Oracle as ora
from multiprocessing import Process
import datetime

db          = ''
user_dev    = ''
user_adm    = ''
ps_dev      = ''
ps_adm      = ''
threads_cnt = 8
size        = 0
n           = 0
i_text      = r''''''
text        = r''''''
path        = r'''C:\\Temp\\oracle\\'''
file_name   = 0
q           = 0
delim       = ';'
const       = 5000000
sql         = r'''select DEAL.ticket_id                                               id
             , case
               when AGR.agr_type_id in ( 1263 )
               then 'К'
               else 'C'
               end                                                                                                       own_deal               --> К/С;CNT
             , DEAL.short_ticket                                                                                         short_ticket           --> Номер сделки
             , DEAL.ref_ticket                                                                                           ref_ticket             --> Биржевой номер
             , TR_GET_DICT.SHORT_NAME( AGR.client_id )                                                                   client_name            --> Клиент
             , ( select tca from V_TR_DICT_SEC_TCA where id = DEAL.tca_id )                                              tca_name               --> ТКС
             , TR_GET_DICT.SHORT_NAME( DEAL.step_id )                                                                    step_name              --> Этап
             , SEC.sec                                                                                                   sec_name               --> Ценная бумага
             , SEC.code_isin                                                                                             code_isin              --> ISIN
             , DEAL.sec_amount                                                                                           sec_amount             --> Количество;NUM
             , DEAL.price                                                                                                price                  --> Цена;NUM=6
             , TR_GET_DICT.SHORT_NAME( DEAL.price_ccy_id )                                                               price_ccy              --> Валюта цены;CNT
             , DEAL.price_ccy_bal_amount                                                                                 price_ccy_bal_amount   --> Стоимость бумаг;NUM=2
             , TR_GET_DICT.SHORT_NAME( DEAL.clear_ccy_id )                                                               clear_ccy              --> Валюта расчетов;CNT
             , DEAL.clear_ccy_amount                                                                                     clear_ccy_amount       --> Сумма;NUM=2
             , DEAL.clear_ccy_aci                                                                                        clear_ccy_aci          --> Купонный доход;NUM=2
             , TR_GET_DICT.SHORT_NAME( DEAL.exch_id )                                                                    exch                   --> Торговая площадка
             , TR_FORMS.GET_SEC_OPER_LABEL( DEAL.SUB_TYPE, DEAL.TRAN )                                                   tran                   --> Направление
             , DEAL.trade_date_time                                                                                      trade_date             --> Дата торгов
             , DEAL.clear_value_date_time                                                                                clear_value_date       --> Дата расчетов
             , DEAL.sec_value_date_time                                                                                  sec_value_date         --> Дата поставки
             , AGR.agreement_num                                                                                         agreement_num          --> Портфель
             , TR_GET_DEAL.SHORT_TICKET( DEAL.oda_ticket_id )                                                            oda_short_ticket       --> Номер поручения
             , TR_GET_DICT.SHORT_NAME( decode( DEAL.back_office_id, 53, DEAL.cust_id, DEAL.rps_cust_id ) )   cust                   --> Контрагент
             , TR_GET_DICT.SHORT_NAME( DEAL.dealer_id )                                                                  dealer                 --> Расч.центр
             , TR_GET_DICT.SHORT_NAME( DEAL.depositary_id )                                                              depositary             --> Депозитарий
             , TR_GET_DEAL.SHORT_TICKET( DEAL.parent_ticket_id )                                                         parent_deal            --> Родительская сделка
          from V_TR_DEAL_CAT_SEC       DEAL
             , V_TR_SEC_AGREEMENT      AGR
             , V_TR_DICT_SEC           SEC
         where AGR.id            = DEAL.agreement_id
           and SEC.id            = DEAL.sec_id
           and not SEC.SEC_TYPE = 1314
           and DEAL.trade_date >=  to_date('01.01.2001', 'DD.MM.YYYY') and DEAL.trade_date <  to_date('07.02.2020', 'DD.MM.YYYY')
           and DEAL.sub_type is null
           and mod(DEAL.ticket_id, :threads_cnt) = :mod'''

# conn = ora.connect(user_dev, ps_dev, db)
# cur = conn.cursor()
# cur.execute(sql)
# cur.execute(sql, {threads_cnt:threads_cnt, mod:mod})

def utf8len(s):
    return len(s.encode('ANSI'))

def create_file(sql, size, threads_cnt, mod):
    file_pref = mod
    txt = ''
    ins_size = 0
    conn = ora.connect(user_dev, ps_dev, db)
    cur = conn.cursor()
    # cur.execute(sql)
    cur.execute(sql, {'threads_cnt':threads_cnt, 'mod':mod})
    while True:       
        i_txt = ''
        try:
            result = cur.fetchone()
        except Exception as e:
            conn.close()
            return
        for item in result:
            i_txt += str(item) + delim  
        ins_size += utf8len(i_txt)
        if ins_size >= size:
            ins_size = utf8len(i_txt)
            with open( path + str(file_pref) + r'''.txt''' ,'w') as File:
                File.write(txt)
                txt = ''                
            file_pref += threads_cnt
        txt += i_txt + '\n'

# create_file(sql, const, threads_cnt, 0)

if __name__ == "__main__":

    threads = []
    for i in range(threads_cnt):
        thread = Process(target=create_file, args=(sql, const, threads_cnt, i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


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