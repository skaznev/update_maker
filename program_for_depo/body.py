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
i_FATCA_ASSET           = r'''
declare    
    v_clob           CLOB;
    v_main_xml       XMLTYPE;
    v_client_xml     XMLTYPE;
    v_total_xml      XMLTYPE;
    v_rep_date       DATE                                                       := :v_rep_date;
    v_sec_isin       VARCHAR2(30)                                               := :v_sec_isin;
    v_msg            VARCHAR2(10000);
    v_doc_ref        VARCHAR2(30)                                               := :v_doc_ref;
    v_request_no     VARCHAR2(30)                                               := :v_request_no;
    v_pay_rep_date   DATE                                                       := :v_pay_rep_date; 
    v_last_rep_date  DATE                                                       := :v_last_rep_date;
    r_sec            V_TR_DICT_SEC%rowtype;
    v_depo_acc       VARCHAR2(20);
    
    CONST_LINE_BREAK                CONSTANT CHAR(2)         := chr(13)||chr(10);
    CONST_XML_HEADER                CONSTANT VARCHAR2(60)    := '<?xml version="1.0" encoding="utf-8"?>'||CONST_LINE_BREAK; -- IXXI-3503

    CONST_SPBEX_PARTY_ID            CONSTANT NUMBER          := TR_GET.SPBEX_PARTY_ID;
    CONST_SPBEX_MFB_PARTY_ID        CONSTANT NUMBER          := TR_GET.ARTEFACT( 'SPBEX_MFB_PARTY_ID' );
    
    CONST_BOOL_TRUE                 CONSTANT NUMBER          := TR_GET.BOOL_TRUE;
    CONST_BOOL_FALSE                CONSTANT NUMBER          := TR_GET.BOOL_FALSE;
    
    CONST_DATE_MASK                 CONSTANT VARCHAR2(10)    := 'YYYY-MM-DD';
    CONST_TIME_MASK                 CONSTANT VARCHAR2(10)    := TR_W.GET_TIME_MASK;
    
    CONST_ACC_TYPE_ASSET            CONSTANT NUMBER          := TR_GET.ACC_TYPE_ASSET; --IXXI-3568
    CONST_ACC_INTERNAL_SDT          CONSTANT NUMBER          := TR_MAJOR.GET_ID( 'ACC_INTERNAL_TYPE_ID', 'SDT' ); --IXXI-3568
    CONST_SUB_TYPE_DOC_W8           CONSTANT NUMBER          := TR_MAJOR.GET_ID( 'PARTY_PROPERTY_DOC', 'SUB_TYPE_ID', 'W8BEN' );

BEGIN


    DBMS_LOB.CREATETEMPORARY( v_clob, TRUE );

    if v_sec_isin is null
    then
        v_msg := 'Недостаточно данных для формирования ответа: не задан ISIN ценной бумаги. ';

    else
        r_sec := TR_GET_DICT_SEC.GET_SEC_4CODE_ISIN
                     ( i_code_isin => v_sec_isin
                     , o_msg       => v_msg
                     ) ;

    end if;

    if v_rep_date is null
    then
        v_msg := v_msg || 'Недостаточно данных для формирования ответа: не задана дата отчета. ';

    end if;

    if not v_msg is null
    then
        TR_ERROR.SYS_RAISE_ERROR( v_msg );

    end if;

    -- ДАННЫЕ ПО ВЫПЛАТАМ
    select xmlagg(xmlelement("CLIENT"
                            , xmlattributes
                                  ('TKBNM'          as "BrokerCode"
                                  , CT.client_code  as "ClientCode"
                                  , ''              as "ExtIdentificationCode"
                                  , CT.tax_rate     as "TaxRate"
                                  )
                            , xmlagg( xmlelement ("ASSET"
                                                 , xmlattributes
                                                       ( CT.sec_amount    as "Qty"
                                                       , CT.amount        as "IncomeAmount"
                                                       , ''               as "NoPaymentInfo"
                                                         --> IXXI-5658
                                                       , CT.ccy_code_iso  as "PaymentCurrency"
                                                       , CT.tax_rate_deal as "AppliedTaxRate"
                                                         --< IXXI-5658
                                                       )
                                                 )
                                    )
                            )
                  )  cli
     into v_client_xml
     from (-->> IXXI-3695
           select ( select ref_code
                      from V_TR_SEC_AGR_EXCH_CODE
                     where agr_id    = DD.agr_id
                       and exch_id   = CONST_SPBEX_PARTY_ID
                  )  client_code
                , ( select TR_W_REPORT_FATCA_PAYMENT.F_GET_TAX_RATE
                               ( DD.party_id
                               , v_rep_date
                               , D.sec_id
                               )
                      from dual )  tax_rate
                , to_char ( DD.sec_amount, 'FM99999999990.00999999' )  sec_amount
                , to_char ( DD.amount    , 'FM99999999990.00999999' )  amount
                  --> IXXI-5658
                , CCY.code_iso                                         ccy_code_iso
                , to_char ( nvl( D.tax_rate, 0 )                    )  tax_rate_deal
                  --< IXXI-5658
            from V_TR_DEAL_CAT_SEC_DIVIDEND      D
               , V_TR_DEAL_CAT_SEC_DIVIDEND_DET  DD
               , V_TR_DICT_CCY                   CCY           -- IXXI-5658
           where D.sec_id              = r_sec.id
             and DD.master_id          = D.ticket_id
             --> IXXI-5658
             and CCY.id                = D.ccy_id
             and D.value_date          = v_rep_date
             and D.corp_action_type_id = TR_GET.CORP_ACTION_TYPE_DVCA

             --< IXXI-5658
           )  CT
    group
       by client_code, tax_rate;


    -- СБОР ФИНАЛЬНОГО XML
    select xmlelement
               ( "RTS_DOC"
               , xmlattributes
                     ( 'http://www.w3.org/2001/XMLSchema-instance' as "xmlns:xsi"
                     , 'payment_report.xsd'                        as "xsi:noNamespaceSchemaLocation"
                     )
               , xmlelement
                     ( "DOC_REQUISITES"
                     , xmlattributes
                           ( to_char( sysdate, CONST_DATE_MASK ) as "DOC_DATE"
                           , to_char( sysdate, CONST_TIME_MASK ) as "DOC_TIME"
                           , tr_rule.exec_seq('INQ')                            as "DOC_NO"
                           , 'FATCA_ASSET'                       as "DOC_TYPE_ID"
                           , 'TKBNM'                             as "SENDER_ID" -- IXXI-3503
                           , ''                                  as "SENDER_NAME"
                           , 'MFBIM'                             as "RECEIVER_ID"
                           , ''                                  as "REMARKS"
                           )
                     )
               , xmlelement
                     ( "FATCA_ASSET"
                     , xmlelement
                           ( "DOC_INFO"
                           , xmlattributes
                                 ( v_doc_ref        as "DOC_REFERENCE"
                                 , 'PAYMENT_REPORT' as "DOC_SUBTYPE"   --IXXI-3737
                                 , v_request_no     as "REQUEST_NO"
                                 )
                           )
                     , xmlelement
                           ( "REPORT_DATE"
                           , xmlattributes
                                 ( to_char( v_last_rep_date, CONST_DATE_MASK )  as "LastReportDate"
                                 , to_char( v_rep_date, CONST_DATE_MASK ) as "ReportDate"
                                 , to_char( v_pay_rep_date, CONST_DATE_MASK )  as "PaymentDate" -- IXXI-3503
                                 )
                           , xmlelement
                                 ( "SECURITY"
                                 , xmlattributes
                                       ( v_sec_isin as "IssueISIN"
                                       )
                                 , v_client_xml
                                 , v_total_xml
                                 )
                           )
                     )
               )
      into v_main_xml
      from dual;

    TR_STANDARD.PROC_REG('TR_UTIL_AGR_CLOSED.GET_XML Окончание формирования v_main_xml ');

    :v_clob := CONST_XML_HEADER || v_main_xml.getClobVal();

end;
'''


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
    
    sql_text = i_FATCA_ASSET

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
        clob = cur.var(cx_Oracle.CLOB)
        try:
            a = cur.execute(sql_text, {'v_rep_date':rep_date, 'v_sec_isin':isin, 'v_doc_ref':doc_ref, 'v_request_no':request_no, 'v_pay_rep_date':pay_rep_date, 'v_last_rep_date':last_rep_date, 'v_clob':clob})
            with open(PATH_OUT + '/' + isin + rep_date_str + '_' + str(numb) + '.xml', 'w') as file:
                    file.writelines(str(clob.getvalue()))
        except Exception as e:
            print('Бумага с ISIN ' + isin + ' не обработана')
            print(e)
            continue
        numb += 1
