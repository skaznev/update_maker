-- 
-- $delimiter = ;
-- $threads = 3
-- $columns = дата|пидата
/*Описание скрипта / запроса*/

/*
-- PL/SQL START
declare
    inq_id NUMBER := 1;
    
begin
    TR_API.EXEC();
    :python_inq := inq_id;
    COMMIT;
end;
-- PL/SQL END
*/

select * from tr_api_log 
where mod(nums, :threads_cnt) = :mod
and :python_inq = :python_inq
