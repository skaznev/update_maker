-- ����� ���� ����������
-- $delimiter = "|"
-- $threads = 1
/*
������ ������������ ��� �������� ������������� ������� � ������ ����. ����� ������� �������������� �� ���������� ��������������� � $PARAM.
� ������� ������������ ������� �������� $P1 = "����� ���� ����������"
*/
 
DECLARE
    -->> ������. ���������� ��� �����������
    rlog       ext_api_log%rowtype;
    rlog_key   VARCHAR2(30);
    --<<
    r_agr_num  V_TR_DEAL_CAT_AGR_INVEST%rowtype;
    old_value  VARCHAR2(50);
 
BEGIN
    DBMS_OUTPUT.DISABLE;
 
    TR_ADMIN.SET_AS_FUND_APPLICATION;
    -->> ������. ������������ ����� � ���������� ��� �����������
    rlog_key := $P0;
    rlog.dest := 'PRS_EXT_EXECUTOR.1';
    rlog.key_name := rlog_key; --�� ���� ���� ������ �����.
    --<< �����. ������������ ����� � ���������� ��� �����������
     
    for rec
    in  ( select *
            from V_TR_DEAL_CAT_AGR_INVEST
           where ticket_id in
 
(
$PARAM
)
             and value_date  is not null
        )
    loop
        begin
            r_agr_num := rec;
            old_value := r_agr_num.expect_date;
             
            r_agr_num.expect_date := to_date ($P1, 'DD.MM.YYYY' ); -- r_agr_num.expect_date + 1;
 
            TR_DEAL_AGR_INVEST.DATA_UPD
                ( ior_agr_invest => r_agr_num
                ) ;
 
            TR_RULE.COMM;
             
            -->> ������. ����������� ��������� �������
            rlog.params := rec.ticket_id || ' ����� ���� ����������: ' || r_agr_num.expect_date ||' ������ ���� ����������:' || old_value;
            rlog.result_code := 0;         -- �����
            ext_api_log_log(rlog);
            --<< �����. ����������� ��������� �������
 
        exception
            when OTHERS
            then
                -->> ������. ����������� ������
                rlog.result_code := sqlcode;
                rlog.result_desc := dbms_utility.format_error_backtrace;
                ext_api_log_log(rlog);
                --<< �����. ����������� ������
                TR_RULE.ROLL;
 
        end;
 
    end loop;
 
    TR_ADMIN.DROP_AS_FUND_APPLICATION;

EXCEPTION
   WHEN OTHERS
   THEN
       -->> ������. ����������� ������
       rlog.result_code := sqlcode;
       rlog.result_desc := dbms_utility.format_error_backtrace;
       ext_api_log_log(rlog);
       --<< �����. ����������� ������
       TR_ADMIN.DROP_AS_FUND_APPLICATION;
       TR_RULE.ROLL;
 
END;