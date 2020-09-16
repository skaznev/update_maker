import cx_Oracle
import datetime
import time
import xlrd
import xml.etree.cElementTree as et
import os

doc_no_path             = 'DOC_REQUISITES'
doc_no_atr              = 'DOC_NO'
request_no_path         = 'FATCA_ASSET//DOC_INFO'
request_no_atr          = 'REQUEST_NO'
report_date_path        = 'FATCA_ASSET//REPORT_DATE'
report_date_atr         = 'ReportDate'
payment_date_path       = 'FATCA_ASSET//REPORT_DATE'
payment_date_atr        = 'PaymentDate'
last_report_date_path   = 'FATCA_ASSET//REPORT_DATE'
last_report_date_atr    = 'LastReportDate'
isin_path               = 'FATCA_ASSET//REPORT_DATE//SECURITY'
isin_atr                = 'IssueISIN'

file_pref               = 'PAYMENT_REPORT_TKBNM_'

with open(r'sql.sql', 'r', encoding='UTF-8') as file:
    sql_text = file.read()

# sql_text = ''
# for i in a:
#     sql_text += i


def xl_date(xldate):
    return (
        datetime.datetime(1899, 12, 30)
        + datetime.timedelta(days=xldate)
        )

def getValueXml (valueList, attrib):   
    xmlPath = './' + valueList
    try:
        for child in root.iterfind(xmlPath):
            return child.attrib[attrib]
    except Exception as identifier:
        print(str(attrib) + ' не заполнен!')

def getDate (field, timemask):
    c = time.strptime(field, timemask)
    return datetime.date(c[0], c[1], c[2])


def execute (PATH_IN, PATH_OUT, USER, PASSWORD, DATABASE):
    
    global doc_no_path
    global doc_no_atr
    global request_no_path
    global request_no_atr
    global report_date_path
    global report_date_atr
    global payment_date_path
    global payment_date_atr
    global last_report_date_path
    global last_report_date_atr
    global isin_path
    global isin_atr
    global root
    
    user = USER
    ps   = PASSWORD
    db   = DATABASE

    conn = cx_Oracle.connect(user, ps, db)
    cur = conn.cursor()

    files = os.listdir(PATH_IN)
    
    numb = 0
    for fle in files:
        fileXml = open(os.path.join(PATH_IN, fle))
        file = et.ElementTree(file = fileXml)
        root = file.getroot()
        doc_ref = getValueXml(doc_no_path, doc_no_atr)
        rep_date_str = getValueXml(report_date_path, report_date_atr)
        rep_date = getDate(rep_date_str, '%Y-%m-%d')
        isin = getValueXml(isin_path, isin_atr)
        request_no = getValueXml(request_no_path, request_no_atr)
        pay_rep_date_str = getValueXml(payment_date_path, payment_date_atr)
        pay_rep_date = getDate(pay_rep_date_str, '%Y-%m-%d')
        last_rep_date_str = getValueXml(last_report_date_path, last_report_date_atr)
        last_rep_date = getDate(last_rep_date_str, '%Y-%m-%d')
        date_now_str = str(time.strftime('%Y%m%d'))
        clob = cur.var(cx_Oracle.CLOB)
        try:
            a = cur.execute(sql_text, {'v_rep_date':rep_date, 'v_sec_isin':isin, 'v_doc_ref':doc_ref, 'v_request_no':request_no, 'v_pay_rep_date':pay_rep_date, 'v_last_rep_date':last_rep_date, 'v_clob':clob})
            with open(PATH_OUT + '/' + file_pref + isin + '_' + date_now_str + '.xml', 'w') as file:
                    file.writelines(str(clob.getvalue()))
        except Exception as e:
            print('Бумага с ISIN ' + isin + ' не обработана')
            print(e)
            continue
        numb += 1
