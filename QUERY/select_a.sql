-- 
-- $delimiter = ;
-- $threads = 3
-- $columns = дата|пидата
/*Описание скрипта / запроса*/
select * from tr_api_log 
where mod(nums, :threads_cnt) = :mod
