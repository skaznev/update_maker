-- Новая дата исполнения
-- $delimiter = "|"
-- $threads = 1
/*
Скрипт предназначен для переноса неисполненных выводов в другую дату. Отбор выводов осуществляется по переданным идентификаторам в $PARAM.
В скрипте предусмотрен входной параметр $P1 = "Новая дата исполнения"
*/
 
DECLARE
    -->> Начало. Перененные для логирования
    rlog       ext_api_log%rowtype;
    rlog_key   VARCHAR2(30);
    --<<
    r_agr_num  V_TR_DEAL_CAT_AGR_INVEST%rowtype;
    old_value  VARCHAR2(50);
 
BEGIN
    DBMS_OUTPUT.DISABLE;
 
    TR_ADMIN.SET_AS_FUND_APPLICATION;
    -->> Начало. Формирование ключа и назначения для логирования
    rlog_key := $P0;
    rlog.dest := 'PRS_EXT_EXECUTOR.1';
    rlog.key_name := rlog_key; --по нему ищем записи потом.
    --<< Конец. Формирование ключа и назначения для логирования
     
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
             
            -->> Начало. Логирование успешного запуска
            rlog.params := rec.ticket_id || ' Новая дата исполнения: ' || r_agr_num.expect_date ||' Старая дата исполнения:' || old_value;
            rlog.result_code := 0;         -- Успех
            ext_api_log_log(rlog);
            --<< Конец. Логирование успешного запуска
 
        exception
            when OTHERS
            then
                -->> Начало. Логирование ошибки
                rlog.result_code := sqlcode;
                rlog.result_desc := dbms_utility.format_error_backtrace;
                ext_api_log_log(rlog);
                --<< Конец. Логирование ошибки
                TR_RULE.ROLL;
 
        end;
 
    end loop;
 
    TR_ADMIN.DROP_AS_FUND_APPLICATION;

EXCEPTION
   WHEN OTHERS
   THEN
       -->> Начало. Логирование ошибки
       rlog.result_code := sqlcode;
       rlog.result_desc := dbms_utility.format_error_backtrace;
       ext_api_log_log(rlog);
       --<< Конец. Логирование ошибки
       TR_ADMIN.DROP_AS_FUND_APPLICATION;
       TR_RULE.ROLL;
 
END;