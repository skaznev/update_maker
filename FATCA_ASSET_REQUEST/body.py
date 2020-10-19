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
doc_subtype_path        = 'FATCA_ASSET//DOC_INFO'
doc_subtype_atr         = 'DOC_SUBTYPE'

file_pref_asset         = 'ASSET_REPORT_TKBNM_'
file_pref_payment       = 'PAYMENT_REPORT_TKBNM_'
file_pref_planned_asset = 'PLANNED_ASSET_REPORT_TKBNM_'


with open(r'sql/asset.sql', 'r', encoding='UTF-8') as file:
    sql_asset_text = file.read()

with open(r'sql/payment.sql', 'r', encoding='UTF-8') as file:
    sql_payment_text = file.read()

with open(r'sql/planned_asset.sql', 'r', encoding='UTF-8') as file:
    sql_planned_asset_text = file.read()

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


def execute (FILE_TYPE, PATH_IN, PATH_OUT, USER, PASSWORD, DATABASE):
    
    global doc_subtype_path
    global doc_subtype_atr
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
    file_pref = ''
    
    user = USER
    ps   = PASSWORD
    db   = DATABASE
    file_type = FILE_TYPE

    conn = cx_Oracle.connect(user, ps, db)
    cur = conn.cursor()

    files = os.listdir(PATH_IN)
    
    cnt_success = 0
    cnt_error = 0
    error_msg = ''
    msg = ''
    for fle in files:
        fileXml = open(os.path.join(PATH_IN, fle))
        file = et.ElementTree(file = fileXml)
        root = file.getroot()
        doc_subtype = getValueXml(doc_subtype_path, doc_subtype_atr)
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
            if file_type == 'FATCA_ASSET_PAYMENT_REQUEST' and doc_subtype == 'PAYMENT_REQUEST':
                file_pref = file_pref_payment
                cur.execute(sql_payment_text, {'v_rep_date':rep_date, 'v_sec_isin':isin, 'v_doc_ref':doc_ref, 'v_request_no':request_no, 'v_pay_rep_date':pay_rep_date, 'v_last_rep_date':last_rep_date, 'v_clob':clob})
            if file_type == 'FATCA_ASSET_REQUEST' and doc_subtype == 'ASSET_REQUEST':
                file_pref = file_pref_asset
                cur.execute(sql_asset_text, {'v_rep_date':rep_date, 'v_sec_isin':isin, 'v_doc_ref':doc_ref, 'v_request_no':request_no, 'v_pay_rep_date':pay_rep_date, 'v_last_rep_date':last_rep_date, 'v_clob':clob})    
            if file_type == 'PLANNED_ASSET_REQUEST' and doc_subtype == 'PLANNED_ASSET_REQUEST':
                file_pref = file_pref_planned_asset
                cur.execute(sql_planned_asset_text, {'v_rep_date':rep_date, 'v_sec_isin':isin, 'v_doc_ref':doc_ref, 'v_request_no':request_no, 'v_pay_rep_date':pay_rep_date, 'v_last_rep_date':last_rep_date, 'v_clob':clob})
            with open(PATH_OUT + '/' + file_pref + isin + '_' + date_now_str + '.xml', 'w') as file:
                file.writelines(str(clob.getvalue()))
            cnt_success += 1
        except Exception as e:
            print('Бумага с ISIN ' + isin + ' не обработана')
            print(e)
            error_msg += 'Бумага с ISIN ' + isin + ' не обработана\n'
            error_msg += str(e) + '\n'
            cnt_error += 1
            continue

    msg = 'Обработано ' + str(cnt_success) + ' из ' + str(cnt_success+cnt_error) + ' файлов.\n' + error_msg

    return msg
        
