#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os, sys, datetime
#reload(sys)
#sys.setdefaultencoding('utf8')
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from prometheus_client import start_http_server, Summary, Gauge
import cx_Oracle
import time
import random
from multiprocessing import Process, current_process, Lock
from getpass import getpass

username = ""
password = ""
database = ""

class clsBufQuik(object):
    def calc(self):
        start_http_server(8000)
        print(username,password,database)
        connection = cx_Oracle.connect(username, password, database)
        g1  = Gauge('BUFF_QUIK_FX', 'Ошибки в V_TR_BUFF_QUIK_FX')
        g2  = Gauge('BUFF_QUIK', 'Ошибки в V_TR_BUFF_QUIK')
        g3  = Gauge('BUFF_QUIK_ORDER_FX', 'Ошибки в V_TR_BUFF_QUIK_ORDER_FX')
        g4  = Gauge('BUFF_QUIK_ORDER', 'Ошибки в V_TR_BUFF_QUIK_ORDER')
        while True:
            cursor = connection.cursor()
            #BUFF_QUIK_FX
            for row1, in cursor.execute("""select count ( 1 )
                                             from V_TR_BUFF_QUIK_FX
                                            where buff_status = 'E'
                                              and insert_date_time > trunc ( sysdate )"""):
                g1.set(row1)
            #BUFF_QUIK
            for row2, in cursor.execute("""select count ( 1 )
                                             from V_TR_BUFF_QUIK
                                            where buff_status = 'E'
                                              and insert_date_time > trunc ( sysdate )"""):
                g2.set(row2)
            #BUFF_QUIK_ORDER_FX
            for row3, in cursor.execute("""select count ( 1 )
                                             from V_TR_BUFF_QUIK_ORDER_FX
                                            where buff_status = 'E'
                                              and insert_date_time > trunc ( sysdate )"""):
                g3.set(row3)
            #BUFF_QUIK_ORDER
            for row4, in cursor.execute("""select count ( 1 )
                                             from V_TR_BUFF_QUIK_ORDER
                                            where buff_status = 'E'
                                              and insert_date_time > trunc ( sysdate )"""):
                g4.set(row4)
            time.sleep(30)

class clsDealStatus(object):
    def calc(self):
        start_http_server(8001)
        connection = cx_Oracle.connect(username, password, database)
        g5   = Gauge('DEAL_NOT_CLS_VAL_OWN'           , 'Количество сделок не в конечном статусе (клиентские валюта биржевые)')
        g6   = Gauge('DEAL_NOT_CLS_REPO_MRKT_OWN'     , 'Количество сделок не в конечном статусе (клиентские РЕПО биржевые)')
        g7   = Gauge('DEAL_NOT_CLS_REPO_MRKT_DIL'     , 'Количество сделок не в конечном статусе (дилерские РЕПО биржевые)')
        g8   = Gauge('DEAL_NOT_CLS_FOND_OWN_MB'       , 'Количество сделок не в конечном статусе (клиентские фондовые биржевые МОС-БИРЖА)')
        g9   = Gauge('DEAL_NOT_CLS_FOND_OWN_SB'       , 'Количество сделок не в конечном статусе (клиентские фондовые биржевые СП-БИРЖА)')
        g10  = Gauge('DEAL_NOT_CLS_FOND_DIL'          , 'Количество сделок не в конечном статусе (дилерские фондовые биржевые)')
        g11  = Gauge('DEAL_DRAFT_NOT_MRKT_OWN'        , 'Количество сделок в статусе ЧЕРНОВИК (клиентские ВНЕбиржевые)')
        g12  = Gauge('DEAL_DRAFT_NOT_MRKT_DIL'        , 'Количество сделок в статусе ЧЕРНОВИК (дилерские ВНЕбиржевые)')
        g13  = Gauge('DEAL_NOT_CLS_REPO_NOT_MRKT_OWN' , 'Количество сделок не в конечном статусе (клиентские РЕПО ВНЕбиржевые)')
        g14  = Gauge('DEAL_NOT_CLS_REPO_NOT_MRKT_DIL' , 'Количество сделок не в конечном статусе (дилерские РЕПО ВНЕбиржевые)')
        while True:
            cursor = connection.cursor()
            #deal_not_cls_val_own   клиентская валюта биржевая
            for row5, in cursor.execute("""select count ( 1 )
                                             from V_TR_DEAL_CAT_EXCH   DEAL
                                             join V_TR_DICT_SEC_AGR    AGR  on AGR.id = DEAL.agr_id
                                            where DEAL.status_type_id  != 219 --TR_GET.STATUS_CLOSE
                                              and DEAL.trade_date_time >  SYSDATE -1 
                                              and AGR.agreement_type   in ( 1263  -- TR_GET.AGREEMENT_BROKER
                                                                          , 2027  -- TR_GET.AGREEMENT_HANDL
                                                                          )"""):
                g5.set(row5)
            #deal_not_cls_repo_mrkt_own  клиентские репо биржевые
            for row6, in cursor.execute("""select count(1)  res
                                     from V_TR_DEAL_CAT_SEC_REPO  DEAL
                                     join V_TR_DICT_SEC_AGR       AGR on AGR.id = DEAL.agreement_id
                                    where DEAL.sub_type            = 82--TR_GET.BOOL_FALSE
                                      and AGR.agr_type_id in ( 1263  -- TR_GET.AGREEMENT_BROKER
                                                             , 2027  -- TR_GET.AGREEMENT_HANDL
                                                             )
                                      and AGR.tf_master_pfl_id    is null
                                      and DEAL.back_office_id      = 1644 -- TR_GET.BO_SEC_EXCH_REPO
                                      and DEAL.trade_date         >= trunc(sysdate) - 2
                                      and not DEAL.status_type_id  = 219  -- TR_GET.STATUS_CLOSE """):
                g6.set(row6)
            #deal_not_cls_repo_mrkt_dil  дилерские репо биржевые
            for row7, in cursor.execute("""select count(1)  res
                                     from V_TR_DEAL_CAT_SEC_REPO  DEAL
                                     join V_TR_DICT_SEC_AGR       AGR on AGR.id = DEAL.agreement_id
                                    where     DEAL.sub_type            = 82--TR_GET.BOOL_FALSE
                                      and not AGR.agr_type_id in ( 1263  -- TR_GET.AGREEMENT_BROKER
                                                                 , 2027  -- TR_GET.AGREEMENT_HANDL
                                                                 )
                                      and AGR.tf_master_pfl_id     is null
                                      and     DEAL.back_office_id      = 1644 -- TR_GET.BO_SEC_EXCH_REPO
                                      and     DEAL.trade_date         >= trunc(sysdate) - 2
                                      and not DEAL.status_type_id      = 219  -- TR_GET.STATUS_CLOSE"""):
                g7.set(row7)
            #deal_not_cls_fond_own_mb  клиентские фондовые биржевые МосБиржа
            for row8, in cursor.execute("""select count(1)
                                     from V_TR_DEAL_CAT_SEC DEAL
                                     join V_TR_DICT_SEC_AGR AGR on AGR.id = DEAL.agreement_id
                                    where AGR.agr_type_id in ( 1263  -- TR_GET.AGREEMENT_BROKER
                                                             , 2027  -- TR_GET.AGREEMENT_HANDL
                                                             )
                                      and AGR.tf_master_pfl_id     is null
                                      and DEAL.back_office_id      = 52
                                      and DEAL.sub_type            is null
                                      and DEAL.trade_date         >= trunc(sysdate) - 2
                                      and not DEAL.status_type_id  = 219  -- TR_GET.STATUS_CLOSE
                                      and DEAL.exch_id             = 176511"""):
                g8.set(row8)
            #deal_not_cls_fond_own_sb  клиентские фондовые биржевые СПБиржа
            for row9, in cursor.execute("""select count(1)
                                     from V_TR_DEAL_CAT_SEC DEAL
                                     join V_TR_DICT_SEC_AGR AGR on AGR.id = DEAL.agreement_id
                                    where AGR.agr_type_id in ( 1263  -- TR_GET.AGREEMENT_BROKER
                                                             , 2027  -- TR_GET.AGREEMENT_HANDL
                                                             )
                                      and AGR.tf_master_pfl_id     is null
                                      and DEAL.back_office_id      = 52
                                      and DEAL.sub_type            is null
                                      and DEAL.trade_date         >= trunc(sysdate) - 2
                                      and not DEAL.status_type_id  = 219  -- TR_GET.STATUS_CLOSE
                                      and DEAL.exch_id             = 365741"""):
                g9.set(row9)
            #deal_not_cls_fond_dil  дилерские фондовые биржевые
            for row10, in cursor.execute("""select count(1)
                                     from V_TR_DEAL_CAT_SEC DEAL
                                    where     DEAL.back_office_id  = 52
                                      and     DEAL.sub_type       is null
                                      and     DEAL.trade_date     >= trunc(sysdate) - 2
                                      and not DEAL.status_type_id  = 219  -- TR_GET.STATUS_CLOSE
                                      and     agr_id4not_nostro    = 0"""):
                g10.set(row10)
            #deal_draft_not_mrkt_own  клиентские фондовые внебиржевые
            for row11, in cursor.execute("""select count(1)
                                     from V_TR_DEAL_CAT_SEC DEAL
                                     join V_TR_DICT_SEC_AGR AGR on AGR.id = DEAL.agreement_id
                                    where AGR.agr_type_id in ( 1263  -- TR_GET.AGREEMENT_BROKER
                                                             , 2027  -- TR_GET.AGREEMENT_HANDL
                                                             )
                                      and AGR.tf_master_pfl_id    is null
                                      and DEAL.back_office_id      = 53
                                      and DEAL.sub_type           is null
                                      and DEAL.trade_date         >= TRUNC(SYSDATE) - 2
                                      and DEAL.status_type_id      = 211 --TR_GET.STATUS_DRAFT"""):
                g11.set(row11)
            #deal_draft_not_mrkt_dil  дилерские фондовые внебиржевые
            for row12, in cursor.execute("""select count(1)
                                     from V_TR_DEAL_CAT_SEC DEAL
                                    where DEAL.back_office_id   = 53
                                      and DEAL.sub_type        is null
                                      and DEAL.trade_date      >= TRUNC(SYSDATE) - 2
                                      and DEAL.status_type_id   = 211 --TR_GET.STATUS_DRAFT
                                      and agr_id4not_nostro     = 0"""):
                g12.set(row12)
            #deal_not_cls_repo_not_mrkt_own  клиентские репо ВНЕбиржевые
            for row13, in cursor.execute("""select count(1)
                                     from V_TR_DEAL_CAT_SEC_REPO DEAL
                                     join V_TR_DICT_SEC_AGR AGR on AGR.id = DEAL.agreement_id
                                    where AGR.agr_type_id in ( 1263  -- TR_GET.AGREEMENT_BROKER
                                                             , 2027  -- TR_GET.AGREEMENT_HANDL
                                                             )
                                      and AGR.tf_master_pfl_id     is null
                                      and DEAL.back_office_id      = 1959
                                      and DEAL.sub_type            is null
                                      and DEAL.trade_date          >= TRUNC(SYSDATE) - 2
                                      and not DEAL.status_type_id  = 219  -- TR_GET.STATUS_CLOSE"""):
                g13.set(row13)
            #deal_not_cls_repo_not_mrkt_dil  клиентские репо ВНЕбиржевые
            for row14, in cursor.execute("""select count(1)
                                     from V_TR_DEAL_CAT_SEC_REPO DEAL
                                     join V_TR_DICT_SEC_AGR AGR on AGR.id = DEAL.agreement_id
                                    where not AGR.agr_type_id in ( 1263  -- TR_GET.AGREEMENT_BROKER
                                                                 , 2027  -- TR_GET.AGREEMENT_HANDL
                                                                 )
                                      and AGR.tf_master_pfl_id     is null
                                      and DEAL.back_office_id      = 1959
                                      and DEAL.sub_type            is null
                                      and DEAL.trade_date          >= TRUNC(SYSDATE) - 2
                                      and not DEAL.status_type_id  = 219  -- TR_GET.STATUS_CLOSE"""):
                g14.set(row14)
            time.sleep(300)

class clsJobCollector(object):
    def collect(self):
        connection = cx_Oracle.connect(username, password, database)
        c = GaugeMetricFamily('JOB_STATUS', 'Статусы JOB', labels=['job_name'])
        cursor = connection.cursor()
        cursor.execute("""select T.job_name                                    job_name
                               , decode( V.job , null, 0, decode ( V.broken, 'Y', -1 , 1)) status
                            from V_TR_SYS_DBA_JOBS   V
                               , V_TR_TYPE_JOB       T
                           where T.proc_name     = V.what(+)
                             and (        T.thread_id is null
                                   or not V.job       is null
                                 )""")
        for job_name, status, in cursor:
            c.add_metric([job_name], status)
        yield c
        connection.close()

class clsJobStatus(object):
    def calc(self):
        start_http_server(8002)
        connection = cx_Oracle.connect(username, password, database)
        REGISTRY.register(clsJobCollector())
        while True:
            clsJobCollector()
            time.sleep(150)

class clsImoCollector(object):
    def collect(self):
        connection = cx_Oracle.connect(username, password, database)
        c = GaugeMetricFamily('IMO_WAITING', 'Количество проводок в очереди', labels=['job_name', 'job_date'])
        cursor = connection.cursor()
        cursor.execute("""select rbt_id                                job_name
                               , to_char(rbt_date_time, 'dd.mm.yyyy')  job_date
                               , count ( 1 )                           cnt
                            from V_TR_RBT_OBJ
                           where rbt_id in ( 'RBT_DOC_EXP_IMO'
                                           , 'RBT_DOC_EXP_IMO_NOT_RUB'
                                           )
                           group 
                              by rbt_id
                               , rbt_date_time
                           order 
                              by rbt_id
                               , rbt_date_time""")
        for job_name, job_date, cnt, in cursor:
            c.add_metric([job_name, job_date,], cnt)
        yield c
        connection.close()

class clsImoStatus(object):
    def calc(self):
        start_http_server(8003)
        connection = cx_Oracle.connect(username, password, database)
        REGISTRY.register(clsImoCollector())
        while True:
            clsImoCollector()
            time.sleep(30)

class clsGetAllMetrics(object):
    def run(self, proc_name):
        if proc_name == 'BUFF_QUIK':
            clsBufQuik().calc()
        if proc_name == 'DEAL_STATUS':
            clsDealStatus().calc()
        if proc_name == 'JOB_STATUS':
            clsJobStatus().calc()
        if proc_name == 'IMO_WAITING':
            clsImoStatus().calc()

if __name__ == '__main__':

    services = ['BUFF_QUIK','DEAL_STATUS','JOB_STATUS','IMO_WAITING',]
    procs = []
    for service in services:
        proc = Process(target=clsGetAllMetrics().run, name = service, args=(service,))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()
