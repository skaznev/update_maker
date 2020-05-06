-- Дата расчетов|Дата расчетов (dd.mm.yyyy)|Дата поставки
-- $delimiter = "|"
-- $threads = 3
/*Описание скрипта / запроса*/
select * from tr_api_log 
where van = '1'
