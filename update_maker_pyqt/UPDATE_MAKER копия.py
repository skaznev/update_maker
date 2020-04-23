#Подключаем библоиотеки
import os
import shutil
# import culture

# Обьявляем переменные --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if_tr_tool_metadata = False # Переменная которая говрит, что в патче меняется TR_TOOL_METADATA.
i_metadata          = ''    # Переменная в которую начитываем исполняемый кусок с метадатой.
i_script            = ''    # Переменная в которую начитываем исполняемый кусок со скриптами.
i_forms_bat         = ''    # Переменная в которую начитываем исполняемый кусок с формами
path                = ''    # Директория с патчем.
path_stock_script   = ''    # Директория со стоковыми скриптами

# Блок переменнх для написания RunMe.sql
i_start             = '\nprompt ==========                           начало '
i_end               = '\nprompt ==========                           конец '
i_palka             = ' ==========\n'
i_dog               = '@@'
i_n                 = '\n'
i_stock_script      = '''
prompt ==========                           начало fnd_ci.sql ==========
@@fnd_ci.sql
/
prompt ==========                           конец fnd_ci.sql ==========

prompt ==========                           начало fnd_2usr.sql ==========
@@fnd_2usr.sql
/
prompt ==========                           конец fnd_2usr.sql ==========

prompt ==========                           начало fnd_2adm.sql ==========
@@fnd_2adm.sql
/
prompt ==========                           конец fnd_2adm.sql ==========

prompt ==========                           начало fnd_ci.sql ==========
@@fnd_ci.sql
/
prompt ==========                           конец fnd_ci.sql ==========

prompt  состояние схемы после применения обновления:
select OBJECT_TYPE, substr( OBJECT_NAME, 1, 35 ) OBJECT_NAME, STATUS from user_objects where not status = 'VALID';
/

'''
i_start_sql         = '''
spool LOG.log
set define off
set serveroutput on size 1000000

select User||'@'||Global_Name||' '||To_Char (SysDate,'DD.MM.YYYY HH24:MI:SS') "Начало обновления"
from Global_Name

/

prompt   Cостояние схемы до применения обновления:
select OBJECT_TYPE, substr( OBJECT_NAME, 1, 35 ) OBJECT_NAME, STATUS from user_objects where not status = 'VALID';
/
'''
i_end_sql           = '''

spool off
exit;
/
'''

# Блок переменных для написания RunMe.bat
i_start_bat         = '''
cls
@echo Командный файл для обновления АБС "Фонд"
@echo Обновление должно быть распаковано в директорию %\fund\temp\
@echo Клиентская часть компилируется под стандартными пользователями (fund_dev и fund_admin), которые должны быть заведены в системе.

@echo Параметры запуска: RunMe.bat basename [PasswordFund_db PasswordFund_dev PasswordFund_admin PasswordCust]
@echo где basename - имя базы(параметр обязательный), остальные параметры необходимо вводить только в том случае,
@echo если пароли стандартных пользователей отличны от паролей по умолчанию
@echo Для продолжения нажмите пробел, для завершения работы ctrl-c
@pause

@if -%1==- goto NoBase

@if -%2==- (set PasFund_db=FUND_DB)       else (set PasFund_db=%2)
@if -%3==- (set PasFund_dev=FUND_DEV)     else (set PasFund_dev=%3)
@if -%4==- (set PasFund_admin=FUND_ADMIN) else (set PasFund_admin=%4)
@if -%5==- (set PasCust=CUST)             else (set PasCust=%5)

@echo Обновление объектов схемы FUND_DB:
plus80w fund_db/%PasFund_db%@%1 @runme.sql


@echo.
@echo Проверьте состояние серверной части,
@echo и, если все в порядке, нажмите пробел для обновления клиентской части
@pause

cd ..
@del FundErr.log

xcopy temp\*.fmb forms\*.fmb /y /f     2>temp\FundErr.log
xcopy temp\*.bat forms\*.bat /y /f     2>>temp\FundErr.log





@(for /F  %%i in (temp\FundErr.log) do set error=%%i)
@if not -%error%==- (@echo. & @echo. & @echo ВО ВРЕМЯ КОПИРОВАНИЯ ФАЙЛОВ ПРОИЗОШЛА ОШИБКА: & type temp\FundErr.log & @echo ПОПРОБУЙТЕ ВЫПОЛНИТЬ КОПИРОВАНИЕ ВРУЧНУЮ & @pause) else (@del temp\FundErr.log)





cd forms\n
'''
i_end_bat ='''
del *.err

cd ..
cd temp
del *.sql
del *.pll
del *.fmb
del *.mmb
del *.bat
cd ..

xcopy temp\*.log 2Basa\*.log /y /f


goto :eof


:NoBase
@echo HE ЗАДАН ОБЯЗАТЕЛЬНЫЙ ПАРАМЕТР - ИМЯ БАЗЫ! УСТАНОВКА ОБНОВЛЕНИЯ ПРЕРВАНА
'''

i_start_forms = 'start /min /wait IFCMP60 module='
i_user_id     = '   userid=fund_dev/%PasFund_dev%@%1 module_type='
i_from        = 'FORM'
i_menu        = 'MENU'
i_pll         = 'LIBRARY'
i_comp_all    = ' compile_all=YES\n'


# Конец объявления переменных----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

path                = '''C:\cashe\objects'''
path_stock_scripts  = '''X:\Инверсия\ФОНД\Скрипты'''

path = input('Введите директорию: ')

# Начитываем список файлов из директории
files = os.listdir(path)


# Формируем тело RunMe.sql -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Делаем шапку
runmeSQL = i_start_sql

# Из списка объектов берём все пакеты, и из них делаем исполняемую строку
all_files = [_ for _ in files if ( _[-4:] in [".sql", ".SQL", ".Sql", ".fmb", ".FMB", ".MMB", ".mmb", ".PLL", ".pll" ])]
for file in all_files:
    if (file.upper()[-4:] in [".sql", ".SQL", ".Sql"]):
        if ("TR_TOOL_METADATA" not in file.upper() and "METADATA" in file.upper()):
            i_metadata  = i_metadata + i_start + file + i_palka  + i_dog + file + i_n + '/' + i_end + file + i_palka
        elif ("SCRIPT" in file.upper()):
            i_script  = i_script + i_start + file + i_palka  + i_dog + file + i_n + '/' + i_end + file + i_palka
        else:
            runmeSQL = runmeSQL + i_start + file + i_palka + i_dog + file + i_n + '/' + i_end + file + i_palka
            if "TR_TOOL_METADATA" in file.upper():
                if_tr_tool_metadata = True

# Компилим объекты и раздаем паблик синонимы
runmeSQL = runmeSQL + i_stock_script

# Прольем метадату
runmeSQL = runmeSQL + i_metadata

# Раз в обновлении менялась TR_TOOL_METADATA, тогда вставим блок с метадатой
if if_tr_tool_metadata is True:
    runmeSQL = runmeSQL + i_start + 'METADATA' + i_palka + '''begin TR_TOOL_METADATA.EXECUTE_ALL; end;''' + i_n + '/' + i_end + 'METADATA' + i_palka + i_n + '/'

# Прольем скрипты
runmeSQL = runmeSQL + i_script

# Формируем конец файла runmeSQL
runmeSQL = runmeSQL + i_end_sql

print (runmeSQL)

# Сформировали тело RunMe.sql ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Формируем тело RunMe.bat
runmeBAT = i_start_bat + i_forms_bat + i_end_bat


print (runmeBAT)

# Работа с файлами! -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Зальем себе в патч стоковые скрипты
shutil.copy( path_stock_scripts + '\\fnd_ci.sql', path)
shutil.copy( path_stock_scripts + '\\fnd_2adm.sql', path)
shutil.copy( path_stock_scripts + '\\fnd_2usr.sql', path)

# Создаем файлы RunMe
runme_sql = open(path + '\\RunMe.sql', "w", encoding = "windows-1251")
runme_bat = open(path + '\\RunMe.bat', "w", encoding = "windows-1251")
runme_sql.write(runmeSQL)
runme_bat.write(runmeBAT)
runme_sql.close()
runme_bat.close()

print ('------- Конец служебной информации -------')
print ('Обновление запаковано в '  + path + ' !!!\n')
input('Нажмите клавишу Enter для выхода...')
