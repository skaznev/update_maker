#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os, sys, datetime
#reload(sys)
#sys.setdefaultencoding('utf8')
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from prometheus_client      import start_http_server, Summary, Gauge
from multiprocessing        import Process, current_process, Lock
from getpass                import getpass
import cx_Oracle
import time

i_port          = 'port='       # Тег по которому определяем папки с портами
i_exit          = 'exit.txt'
i_type          = 'type='       # Тег по которому определяем тип метрики
i_labels        = 'labels='     # Тег по которому определяем колонки метрики
i_sleep         = 'sleep='      # Тег по которому поределяем время сна
i_set           = 'set.txt'     # Название файла с параметрами на порт
i_type_gauge    = 'gauge'       # Тег для определения типа метрики
i_type_collect  = 'collector'   # Тег для определения типа метрики


def checkPingDb (connection):
    try:
        return connection.ping() is None
    except:
        return False

class gauges(object):
    def calc(self, username, password, database, port, sleep, metrics):

        start_http_server(port)
        
        g = []
        gaug = None
        for metric in metrics:
            try:
                gaug = Gauge(metric[0],metric[0])
                g.append(gaug)
            except Exception as e:
                print(e)

        connection = cx_Oracle.connect(username, password, database)

        while True:
            if checkPingDb(connection):
                cursor = connection.cursor()
                for i, metric in enumerate(metrics):
                    try:
                        for row, in cursor.execute(metric[1]):
                            g[i].set(row)
                    except:
                        print('Возникла ошибка на этапе выполнения SQL запроса:\n' + str(metric[1]))
            else:
                try:
                    connection = cx_Oracle.connect(username, password, database)
                except Exception as e:
                    print(e)
                    time.sleep(sleep)
                    continue
            time.sleep(sleep)                        


class clscollectors(object):
    def __init__(self, connection, username, password, database, port, sleep, metrics, labels):
        self.connection = connection
        self.username = username
        self.password = password
        self.database = database
        self.port       = port
        self.sleep      = sleep
        self.metrics    = metrics
        self.labels     = labels

    def collect(self):
      
        for metric in self.metrics:
            c = GaugeMetricFamily(metric[0], metric[0], labels=self.labels)
            if checkPingDb(self.connection):
                cursor = self.connection.cursor()
                try:                
                    cursor.execute(metric[1])
                    for rec in cursor:
                        c.add_metric(rec[:-1], rec[-1])
                except:
                    print('Возникла ошибка на этапе выполнения SQL запроса:\n' + str(metric[1]))
            else:
                try:
                    self.connection = cx_Oracle.connect(self.username, self.password, self.database)
                except Exception as e:
                    print(e)
                    return
        yield c

class collectors(object):
    def calc(self, username, password, database, port, sleep, metrics, labels):
        start_http_server(port)
        connection = cx_Oracle.connect(username, password, database)
        coll = clscollectors(connection, username, password, database, port, sleep, metrics, labels)
        REGISTRY.register(coll)
        while True:
                clscollectors(connection, username, password, database, port, sleep, metrics, labels)
                time.sleep(sleep)

           

class clsGetAllMetrics(object):
    def run(self, username, password, database, port, sleep, metrics, types, labels):
        if types == i_type_gauge:
            gauges().calc(username, password, database, port, sleep, metrics)
        if types == i_type_collect:
            collectors().calc(username, password, database, port, sleep, metrics, labels)

if __name__ == '__main__':
    
    username    = input('Введите логин: ')
    password    = getpass('Введите пароль: ')
    database    = input('Введите базу: ')
    types       = ''            # тип метрики
    labels      = []            # лейблы для метрики типа "кастом коллектор"
    sleep       = 60            # тайм-аут между опросами базы
    procs       = []            # Процессы сбора данных

    for i in os.walk(os.getcwd()):
        if i_port in i[0]:
            print(i[0])
            metrics = []
            for item in i[2]:
                with open(os.path.join(i[0],item),'r') as file:
                    if item == i_set:
                        for line in file:
                            if line[:len(i_sleep)] == i_sleep:
                                sleep = int(line[len(i_sleep):])
                            elif line[:len(i_type)] == i_type:
                                types = line[len(i_type):].rstrip()
                            elif line[:len(i_labels)] == i_labels:
                                labels = line[len(i_labels):].rstrip().split(';')
                    else:
                        metrics.append([item[0:-4],file.read()])

            proc = Process(target=clsGetAllMetrics().run, name = i[0][-4:], args=(username, password, database, int(i[0][-4:]), sleep, metrics, types, labels))
            procs.append(proc)
            proc.start()
    for proc in procs:
        proc.join()
