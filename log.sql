select '����� ������� ����������: ', count(*) from ext_api_log WHERE key_name = :code_run
union all
select '������� ����������: ', count(*) from ext_api_log WHERE key_name = :code_run and result_code = '0'
union all
select '������: ', count(*) from ext_api_log WHERE key_name = :code_run and not result_code = '0'