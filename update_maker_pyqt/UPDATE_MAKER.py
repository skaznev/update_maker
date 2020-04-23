#Подключаем библоиотеки
import os
import shutil

# Обьявляем переменные --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if_tr_tool_metadata = False # Переменная которая говрит, что в патче меняется TR_TOOL_METADATA.
if_cust             = False # Переменная которая говрит, что в патче меняется Cust.
i_metadata          = ''    # Переменная в которую начитываем исполняемый кусок с метадатой.
i_table             = ''    # Переменная в которую начитываем исполняемый кусок с изменением таблиц.
i_script            = ''    # Переменная в которую начитываем исполняемый кусок со скриптами.
i_script_cust       = ''    # Переменная в которую начитываем исполняемый кусок со скриптами для CUST.
i_sql_cus           = ''    # Переменнав в которую начитываем исполняемый кусок для депозитария.
i_forms_bat         = ''    # Переменная в которую начитываем исполняемый кусок с формами.
i_forms_bat_cus     = ''    # Переменная в которую начитываем исполняемый кусок с формами для CUST.
i_runmeSQL          = ''    # Переменная в которую начитываем исполняемый кусок с объектами FUND.
path                = ''    # Директория с объектами для патча.
path_build          = ''    # Директория с патчем.
path_stock_script   = ''    # Директория со стоковыми скриптами.

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
i_start_sql         = '''spool LOG_FUND.log
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
i_start_bat         = '''cls
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

@echo Обновление объектов схем FUND_DB и CUST:
plus80w fund_db/%PasFund_db%@%1 @runme.sql
plus80w cust/%PasCust%@%1 @runme_cust.sql


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





cd forms
@echo Формы Фонда:
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

i_start_sql_cus = '''spool LOG_CUST.log
set define off
set serveroutput on size 1000000

select User||'@'||Global_Name||' '||To_Char (SysDate,'DD.MM.YYYY HH24:MI:SS') "Начало обновления" 
from Global_Name
/

prompt   Cостояние схемы до применения обновления:
select OBJECT_TYPE, substr( OBJECT_NAME, 1, 35 ) OBJECT_NAME, STATUS from user_objects where not status = 'VALID';
prompt 

'''

i_stock_scripts_cus = '''
prompt ==========                           начало cust_ci.sql ==========
@@cust_ci.sql
/
prompt ==========                           конец cust_ci.sql ==========

prompt ==========                           начало cr_ps.sql ==========
@@cr_ps.sql
/
prompt ==========                           конец cr_ps.sql ==========


prompt  состояние схемы после применения обновления:
select OBJECT_TYPE, substr( OBJECT_NAME, 1, 35 ) OBJECT_NAME, STATUS from user_objects where not status = 'VALID';

'''

i_end_sql_cus = '''

spool off
exit;
/
'''

i_start_forms = 'start /min /wait IFCMP60 module='
i_user_id     = '   userid=fund_dev/%PasFund_dev%@%1 module_type='
i_form        = 'FORM'
i_menu        = 'MENU'
i_pll         = 'LIBRARY'
i_comp_all    = ' compile_all=YES\n'


# Конец объявления переменных----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

path_stock_scripts  = '''X:\Инверсия\ФОНД\Скрипты'''

path = input('Введите директорию: ') 
path_build = path + '\\PATH'

print ('Константы и переменные инициализированы')

print ('Инициализация каталогов')
# Чекаем каталоги
shutil.rmtree(path_build, ignore_errors=True) # В винде куча всяких ошибок при работе с каталогами, лучше всего отрабатывает такая связка. Удаляем папку с игнором ошибок, а затем создаем.
os.makedirs(path_build)

print ('Каталоги созданы')

print ('Копирование файлов...')
# Копируем файлы
shutil.rmtree(path_build, ignore_errors=True) # Ну не хочет винда без лишней зачистки.
shutil.copytree(path , path_build)
shutil.rmtree(path_build + '\\CUST', ignore_errors=True) # Ленивый код: накопировали всего, а лишнее теперь удаляем.

print ('Файлы скопированы')

print ('Считывание файлов в массив...')
# Начитываем список файлов из директории
files = os.listdir(path)
if os.path.isdir(path + "\\CUST"):
    files_cus = os.listdir(path + "\\CUST")
    if_cust = True

print ('Файлы считаны')

# Формируем тело RunMe.sql -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Делаем шапку
runmeSQL = i_start_sql

# Из списка объектов берём все пакеты, и из них делаем исполняемую строку
all_files = [f for f in files if ( f.upper()[-4:] in [".SQL", ".FMB", ".MMB", ".PLL", ".BAT"])]
for file in all_files:
    if ((file.upper()[-4:] == ".BAT") or file.lower() in ["runme.bat", "runme_cust.sql", "runme.sql", "fnd_ci.sql", "fnd_2adm.sql", "fnd_2usr.sql"]):
        os.remove(path + '\\' + file)
    elif (file.upper()[-4:] in [".FMB", ".MMB", ".PLL"]):
        if (file.upper()[-4:] == ".FMB"):
            i_forms_bat = i_forms_bat + i_start_forms + file + i_user_id + i_form + i_comp_all
        if (file.upper()[-4:] == ".MMB"):
            i_forms_bat = i_forms_bat + i_start_forms + file + i_user_id + i_menu + i_comp_all
        if (file.upper()[-4:] == ".PLL"):
            i_forms_bat = i_forms_bat + i_start_forms + file + i_user_id + i_pll + i_comp_all
    elif ("table" in file.lower()):
          i_table = i_table + i_start + file + i_palka  + i_dog + file + i_n + '/' + i_end + file + i_palka
    elif (file.upper()[-4:] == ".SQL"):
        if ("TR_TOOL_METADATA" not in file.upper() and "METADATA" in file.upper()):
            i_metadata  = i_metadata + i_start + file + i_palka  + i_dog + file + i_n + '/' + i_end + file + i_palka
        elif ("SCRIPT" in file.upper()):
            i_script  = i_script + i_start + file + i_palka  + i_dog + file + i_n + '/' + i_end + file + i_palka
        else:
            i_runmeSQL = i_runmeSQL + i_start + file + i_palka + i_dog + file + i_n + '/' + i_end + file + i_palka
            if "TR_TOOL_METADATA" in file.upper():
                if_tr_tool_metadata = True

print ('Runme для Фонда создан')

if if_cust:
    all_files_cus = [f for f in files_cus if ( f.upper()[-4:] in [".SQL", ".FMB", ".MMB", ".PLL", ".BAT"])]
    for file in all_files_cus:
        if (file.upper()[-4:] == ".SQL"):
            if ("SCRIPT" in file.upper()):
                i_script_cust  = i_script_cust + i_start + file + i_palka  + i_dog + file + i_n + '/' + i_end + file + i_palka
            else:
                i_sql_cus = i_sql_cus + i_start + file + i_palka + i_dog + file + i_n + '/' + i_end + file + i_palka
        elif (file.upper()[-4:] in [".FMB", ".MMB", ".PLL"]):
            if (file.upper()[-4:] == ".FMB"):
                i_forms_bat_cus = i_forms_bat_cus + i_start_forms + file + i_user_id + i_form + i_comp_all
            if (file.upper()[-4:] == ".MMB"):
                i_forms_bat_cus = i_forms_bat_cus + i_start_forms + file + i_user_id + i_menu + i_comp_all
            if (file.upper()[-4:] == ".PLL"):
                i_forms_bat_cus = i_forms_bat_cus + i_start_forms + file + i_user_id + i_pll + i_comp_all
        shutil.copy( path + '\\CUST\\' + file, path_build)
    print ('Runme для Cust создан')

# Компилим объекты и раздаем паблик синонимы
runmeSQL = runmeSQL + i_table + i_runmeSQL + i_stock_script

# Прольем метадату
runmeSQL = runmeSQL + i_metadata

# Раз в обновлении менялась TR_TOOL_METADATA, тогда вставим блок с метадатой
if if_tr_tool_metadata is True:
    runmeSQL = runmeSQL + i_start + 'METADATA' + i_palka + '''begin TR_TOOL_METADATA.EXECUTE_ALL; end;''' + i_n + '/' + i_end + 'METADATA' + i_palka + i_n + '/'

# Прольем скрипты
runmeSQL = runmeSQL + i_script

# Формируем конец файла runmeSQL
runmeSQL = runmeSQL + i_end_sql

#print (runmeSQL)



# Сформировали тело RunMe.sql ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Формируем тело RunMe_cust.sql
runmeCUS = i_start_sql_cus + i_sql_cus + i_stock_scripts_cus + '''\\''' + i_script_cust + i_end_sql_cus

# Формируем тело RunMe.bat
runmeBAT = i_start_bat + i_forms_bat + '\n@echo Формы Cust:\n' + i_forms_bat_cus + i_end_bat


#print (runmeBAT)

# Работа с файлами! -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Зальем себе в патч стоковые скрипты
shutil.copy( path_stock_scripts + '\\fnd_ci.sql', path_build)
shutil.copy( path_stock_scripts + '\\fnd_2adm.sql', path_build)
shutil.copy( path_stock_scripts + '\\fnd_2usr.sql', path_build)
shutil.copy( path_stock_scripts + '\\cr_ps.sql', path_build)
shutil.copy( path_stock_scripts + '\\cust_ci.sql', path_build)

print ('Создание файлов...')

# Создаем файлы RunMe
runme_sql = open(path_build + '\\RunMe.sql', "w", encoding = "windows-1251")
runme_cus = open(path_build + '\\RunMe_Cust.sql', "w", encoding = "windows-1251")
runme_bat = open(path_build + '\\RunMe.bat', "w", encoding = "windows-1251")
runme_cus.write(runmeCUS)
runme_sql.write(runmeSQL)
runme_bat.write(runmeBAT)
runme_cus.close()
runme_sql.close()
runme_bat.close()

print ('------- Конец служебной информации -------')
print ('Обновление запаковано в '  + path_build + ' !!!\n')
input('Нажмите клавишу Enter для выхода...') 












