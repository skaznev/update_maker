-- 
-- $delimiter = ;
-- $threads = 3
-- $columns = ����|������
/*�������� ������� / �������*/
select * from tr_api_log 
where mod(nums, :threads_cnt) = :mod
