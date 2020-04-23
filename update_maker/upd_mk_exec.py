#Подключаем библиотеки
import os
import shutil
from tkinter import messagebox 
from tkinter import *
import tkinter.ttk as ttk

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
i_runmeSQL_ci       = ''    # Переменная с куском компиляции фондовых объектов

# Блок переменных с директориями
path                = ''    # Директория с объектами для патча.
path_build          = ''    # Директория с патчем.
path_stock_scripts  = ''    # Директория со стоковыми скриптами.

# Блок переменнх для написания RunMe.sql
i_start             = ''
i_end               = ''
i_palka             = ''
i_dog               = ''
i_n                 = ''
i_stock_script      = ''
i_start_sql         = ''
i_end_sql           = ''
i_start_bat         = ''
i_end_bat           = ''
i_start_sql_cus     = ''
i_stock_scripts_cus = ''
i_end_sql_cus       = ''
i_start_forms       = ''
i_user_id           = ''
i_form              = ''
i_menu              = ''
i_pll               = ''
i_comp_all          = ''

# Блок переменнх для написания RunMe.sql
i_start             = '\nprompt ==========                           начало '
i_end               = '\nprompt ==========                           конец '
i_palka             = ' ==========\n'
i_dog               = r'@@'
i_n                 = '\n'
i_stock_script      = r'''
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
i_start_sql         = r'''spool LOG_FUND.log
set define off
set serveroutput on size 1000000

select User||'@'||Global_Name||' '||To_Char (SysDate,'DD.MM.YYYY HH24:MI:SS') "Начало обновления" 
from Global_Name

/

prompt   Cостояние схемы до применения обновления:
select OBJECT_TYPE, substr( OBJECT_NAME, 1, 35 ) OBJECT_NAME, STATUS from user_objects where not status = 'VALID';
/
'''
i_end_sql           = r'''

spool off
exit;
/
'''

# Блок переменных для написания RunMe.bat
i_start_bat         = r'''cls
@echo ATTENTION!!!!!!!!
@echo Install update FUND !!!
@pause


@if -%1==- goto NoBase

@if -%2==- (set PasFund_db=FUND_DB)       else (set PasFund_db=%2)
@if -%3==- (set PasFund_dev=FUND_DEV)     else (set PasFund_dev=%3)
@if -%4==- (set PasFund_admin=FUND_ADMIN) else (set PasFund_admin=%4)
@if -%5==- (set PasCust=CUST)             else (set PasCust=%5)

@echo Обновление объектов схем FUND_DB и CUST:
plus80w fund_db/%PasFund_db%@%1 @runme.sql
plus80w cust/%PasCust%@%1 @runme_cust.sql
plus80w fund_db/%PasFund_db%@%1 @runme_ci.sql


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
i_end_bat = r'''
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

i_start_sql_cus = r'''spool LOG_CUST.log
set define off
set serveroutput on size 1000000

select User||'@'||Global_Name||' '||To_Char (SysDate,'DD.MM.YYYY HH24:MI:SS') "Начало обновления" 
from Global_Name
/

prompt   Cостояние схемы до применения обновления:
select OBJECT_TYPE, substr( OBJECT_NAME, 1, 35 ) OBJECT_NAME, STATUS from user_objects where not status = 'VALID';
prompt 

'''

i_stock_scripts_cus = r'''
prompt ==========                           начало cust_ci.sql ==========
@@cust_ci.sql
/
prompt ==========                           конец cust_ci.sql ==========

prompt ==========                           начало cr_ps.sql ==========
@@cr_ps.sql
/
prompt ==========                           конец cr_ps.sql ==========

prompt ==========                           начало cust_ci.sql ==========
@@cust_ci.sql
/
prompt ==========                           конец cust_ci.sql ==========

prompt  состояние схемы после применения обновления:
select OBJECT_TYPE, substr( OBJECT_NAME, 1, 35 ) OBJECT_NAME, STATUS from user_objects where not status = 'VALID';

'''

i_end_sql_cus = r'''

spool off
exit;
/
'''

i_start_forms = r'start /min /wait IFCMP60 module='
i_user_id     = r'   userid=fund_dev/%PasFund_dev%@%1 module_type='
i_form        = r'FORM'
i_menu        = r'MENU'
i_pll         = r'LIBRARY'
i_comp_all    = ' compile_all=YES\n'


# Конец объявления переменных----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




def exec (PATH, PATH_BUILD, PATH_STOCK_SCRIPTS):
    
    global if_tr_tool_metadata
    global if_cust            
    global i_metadata         
    global i_table            
    global i_script           
    global i_script_cust      
    global i_sql_cus          
    global i_forms_bat        
    global i_forms_bat_cus    
    global i_runmeSQL         
    global i_runmeSQL_ci      
    global path               
    global path_build         
    global path_stock_scripts 
    global i_start            
    global i_end              
    global i_palka            
    global i_dog              
    global i_n                
    global i_stock_script     
    global i_start_sql        
    global i_end_sql          
    global i_start_bat        
    global i_end_bat          
    global i_start_sql_cus    
    global i_stock_scripts_cus
    global i_end_sql_cus      
    global i_start_forms      
    global i_user_id          
    global i_form             
    global i_menu             
    global i_pll              
    global i_comp_all         

    '''root = Tk()
    pb = ttk.Progressbar(root, mode="determinate" , )
    pb.pack()
    pb['maximum'] = 15
    pb['value'] += 1
    Button(root, text="Quit", command=root.quit).pack()
    '''
    # Читаем пути:

    try:
        path = os.path.abspath(PATH)
        path_build = os.path.abspath(PATH_BUILD)
        path_stock_scripts = os.path.abspath(PATH_STOCK_SCRIPTS)
    except:
        messagebox.showinfo ('ERROR!!!', '''ОБНОВЛЕНИЕ ЗАПАКОВАНО С ОШИБКОЙ ОБРАБОТКИ КАТАЛОГОВ!!!!!!''')
    #  pb['value'] += 1
    print ('Константы и переменные инициализированы')

    print ('Инициализация каталогов')
    # Чекаем каталоги
    try:
        shutil.rmtree(path_build, ignore_errors=True) # В винде куча всяких ошибок при работе с каталогами, лучше всего отрабатывает такая связка. Удаляем папку с игнором ошибок, а затем создаем.
        os.makedirs(path_build)
    except:
        messagebox.showinfo ('ERROR!!!', '''ОБНОВЛЕНИЕ ЗАПАКОВАНО С ОШИБКОЙ ОБРАБОТКИ КАТАЛОГОВ!!!!!!''')
    # pb['value'] += 1
    print ('Каталоги созданы')

    print ('Копирование файлов...')
    # Копируем файлы
    try:
        shutil.rmtree(path_build, ignore_errors=True) # Ну не хочет винда без лишней зачистки.
        shutil.copytree(path , path_build)
        shutil.rmtree(os.path.join(path_build , 'CUST') , ignore_errors=True) # Ленивый код: накопировали всего, а лишнее теперь удаляем.
    except:
        messagebox.showinfo ('ERROR!!!', '''ОБНОВЛЕНИЕ ЗАПАКОВАНО С ОШИБКОЙ ОБРАБОТКИ КАТАЛОГОВ!!!!!!''')
    #  pb['value'] += 1
    print ('Файлы скопированы')
    
    print ('Считывание файлов в массив...')
    # Начитываем список файлов из директории
    try:
        files = os.listdir(path)
        if os.path.isdir(os.path.join(path_build , 'CUST')):
            files_cus = os.listdir(os.path.join(path_build , 'CUST'))
            if_cust = True
    except:
        messagebox.showinfo ('ERROR!!!', '''ОБНОВЛЕНИЕ ЗАПАКОВАНО С ОШИБКОЙ НАЧИТКИ ФАЙЛОВ!!!!!!''')
    # pb['value'] += 1
    print ('Файлы считаны')

    # Формируем тело RunMe.sql -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Делаем шапку
    runmeSQL = i_start_sql
    # pb['value'] += 1
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
    # pb['value'] += 1
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
    #  pb['value'] += 1
    # Компилим объекты и раздаем паблик синонимы
    runmeSQL = runmeSQL + i_table + i_runmeSQL + i_stock_script
    # pb['value'] += 1
    # Прольем метадату
    runmeSQL = runmeSQL + i_metadata
    # pb['value'] += 1
    # Раз в обновлении менялась TR_TOOL_METADATA, тогда вставим блок с метадатой
    if if_tr_tool_metadata is True:
        runmeSQL = runmeSQL + i_start + 'METADATA' + i_palka + '''begin TR_TOOL_METADATA.EXECUTE_ALL; end;''' + i_n + '/' + i_end + 'METADATA' + i_palka + i_n + '/'
    # pb['value'] += 1
    # Прольем скрипты
    runmeSQL = runmeSQL + i_script
    #pb['value'] += 1
    # Формируем конец файла runmeSQL
    runmeSQL = runmeSQL + i_end_sql
    # pb['value'] += 1
    # Формируем файл с компиляцией фондовой части
    i_runmeSQL_ci = '''@@fnd_ci.sql
    exit;
    /
    '''
    #pb['value'] += 1

    # Сформировали тело RunMe.sql ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Формируем тело RunMe_cust.sql
    runmeCUS = i_start_sql_cus + i_sql_cus + i_stock_scripts_cus + '''\\''' + i_script_cust + i_end_sql_cus

    # Формируем тело RunMe.bat
    runmeBAT = i_start_bat + i_forms_bat + '\n@echo Формы Cust:\n' + i_forms_bat_cus + i_end_bat

    #pb['value'] += 1

    # Работа с файлами! -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Зальем себе в патч стоковые скрипты
    try:
        shutil.copy( os.path.join(path_stock_scripts , 'fnd_ci.sql'), path_build)
        shutil.copy( os.path.join(path_stock_scripts , 'fnd_2adm.sql') , path_build)
        shutil.copy( os.path.join(path_stock_scripts , 'fnd_2usr.sql') , path_build)
        shutil.copy( os.path.join(path_stock_scripts , 'cr_ps.sql') , path_build)
        shutil.copy( os.path.join(path_stock_scripts , 'cust_ci.sql') , path_build)
    except:
        messagebox.showinfo ('ERROR!!!', '''ОБНОВЛЕНИЕ ЗАПАКОВАНО С ОШИБКОЙ КОПИРОВАНИЯ ФАЙЛОВ СТОКОВЫХ СКРИПТОВ!!!!!!''')
    print ('Создание файлов...')

    # Создаем файлы RunMe
    try:
        runme_sql = open(os.path.join(path_build , 'RunMe.sql') , "w", encoding = "windows-1251")
        runme_cus = open(os.path.join(path_build , 'RunMe_Cust.sql'), "w", encoding = "windows-1251")
        runme_bat = open(os.path.join(path_build , 'RunMe.bat'), "w", encoding = "windows-1251")
        runme_ci  = open(os.path.join(path_build , 'RunMe_ci.sql'), "w", encoding = "windows-1251")
        runme_cus.write(runmeCUS)
        runme_sql.write(runmeSQL)
        runme_bat.write(runmeBAT)
        runme_ci.write(i_runmeSQL_ci)
        runme_cus.close()
        runme_ci.close()
        runme_sql.close()
        runme_bat.close()
    except:
        messagebox.showinfo ('ERROR!!!', '''ОБНОВЛЕНИЕ ЗАПАКОВАНО С ОШИБКОЙ СОЗДАНИЯ ФАЙЛОВ RUNME!!!!!!''')
    #pb['value'] += 1
    print ('------- Конец служебной информации -------')
    print ('Обновление запаковано в '  + path_build + ' !!!\n')
    #input('Нажмите клавишу Enter для выхода...') 
    #root.mainloop()


