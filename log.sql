select 'Всего записей обработано: ', count(*) from ext_api_log WHERE key_name = :code_run
union all
select 'Успешно обработано: ', count(*) from ext_api_log WHERE key_name = :code_run and result_code = '0'
union all
select 'Ошибки: ', count(*) from ext_api_log WHERE key_name = :code_run and not result_code = '0'