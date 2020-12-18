# FAQ
# Сборка в exe производиться в cmd командой pyinstaller -F UPDATE_MAKER.py
# Если собираем приложуху с интерфейсом, то добавляем вконце -w например: pyinstaller -F UPDATE_MAKER.py -w

# Подключаем библиотеки
import tkinter            as tk  # Модуль графического интерфейса. Что б не писать длиннное название при обращении к ней, придумали кликуху.
import tkinter.filedialog as fd  # Модуль с диалогами вида "Сохранить как" "Открыть файл" и так далее. tkinter особенный и при обычном импорте из него вытаскиваются только стоковые функции, а остальные надо доставать вот так вот ручками.
from tkinter import messagebox   # Высплывающие окна
import tkinter.ttk        as ttk # комбобоксы и прочее
import upd_mk_exec        as um  # Наш самописный модуль с логикой запаковки файлов в обновление
import subprocess         as sp  # Модуль работы с процессами (командная строка по сути)
import cx_Oracle                 #
import os



# Обьявляем необходимые переменные:
i_window            = tk.Tk()              # Переменная, которая содержит в себе всё окно (по сути это просто такой объект из модуля tkiner)
path                = ''                   # Директория.
path_stock          = r'''X:\Инверсия\ФОНД\U\FUND_DB\TEST'''
path_build_stock    = r'''C:\Temp\update_maker'''
path_stock_scripts  = r'''\\fs-inversiya\inversiya$\инверсия\ФОНД\Скрипты'''
path_backup         = r'''C:\Temp\update_maker\backup'''
i_path              = tk.Entry(width = 50) # Текстовое окно (на форме) с выбранной директорией.
i_base              = tk.Entry(width = 10) # Текстовое окно (на форме) с базой.
i_label_dir         = tk.Label(text = 'Директория с обновлением:')
i_label_base        = tk.Label(text = 'Обновляемая база:')
i_label_var         = tk.Label(text = 'Что сделать')
i_combobox_base     = ttk.Combobox(i_window)
i_combobox_var      = ttk.Combobox(i_window)
i_comb_var_pak      = 'Запаковать'
i_comb_var_inst     = 'Запаковать и установить'
env_path            = os.environ["PATH"].replace(r'X:\orant\bin;', '')  

try:
    with open('set.txt', 'r') as file:
        os.environ["PATH"] = file.read()  + env_path                                  # Выставляем переменную окружения, что б cx_oracle не ругался
except:
    os.environ["PATH"] = env_path
    print('Не найден файл настроек set.txt. PATH: ' + os.environ["PATH"] )

# установим заголовок для окна:

i_window.title('Программа запаковки обновлений ПО "ФОНД"') # логично что для этого просто нужно использовать соответсвующий метод title который в качестве параметра приводит название окна.
i_combobox_base['values'] = ('XXI_PRE', 'XXI_TEST')
i_combobox_var['values'] = (i_comb_var_pak, i_comb_var_inst)
i_combobox_var.state(['readonly'])
i_combobox_var.set('Запаковать')


def open_dir (): # Объявляем функцию выбора директории.
    path = fd.askdirectory( initialdir = path_stock ) # Внутри функции просто вызов метода с диалогом, из которого считаем директорию.
    i_path.delete(0 , tk.END)
    i_path.insert(0 , path)

def upd_maker ():
    try:
        os.environ["PATH"] = os.environ["PATH"].replace(r'X:\orant\bin;', '')
        global path_build_stock
        global path_backup
        path_build = path_build_stock
        crossing = um.exec(PATH = i_path.get(), PATH_BUILD = path_build, PATH_STOCK_SCRIPTS = path_stock_scripts , BASE = i_combobox_base.get(), PATH_STOCK = path_stock, PATH_BACKUP = path_backup)
        if not crossing == '':
            messagebox.showinfo('Info', 'Были пересечения с другими версиями на тесте (!!!): ' + crossing)
        if i_combobox_base.get().upper() in ['XXI_TEST','XXI_PRE']:
            messagebox.showinfo('Info', 'Бэкап объектов: ' + path_backup)
        if (i_combobox_var.get() == i_comb_var_inst) and not ('РАСХОЖДЕНИЕ!' in crossing):
            os.environ["PATH"] = os.environ["PATH"] + r'X:\orant\bin;' 
            s = sp.Popen( path_build + r'''\\RunMe.bat ''' + i_combobox_base.get() , cwd = path_build, creationflags=sp.CREATE_NEW_CONSOLE)
            s.communicate ()
        else:
            messagebox.showinfo('Info', 'Обновление запаковано в ' + path_build)
    except Exception as e:
        messagebox.showinfo('ERROR!!!', '''ОБНОВЛЕНИЕ НЕ ЗАПАКОВАНО!!!\nПроизошла ошибка в процедуре запаковки:\n''' + str(e) )
    finally:
        path_build = ''

# Замутим кнопки:
i_button_open  = tk.Button(text = "Open", command = open_dir) # Объявили перменную которая является кнопкой. Сразу придумали ей текст и комманду которую она вызывает при нажатии (в нашем случае это функция выбора директории)
i_button_start = tk.Button(text = "Start", command = upd_maker)


# Раскидаем виджеты по форме (слева на право сверху вниз):
i_label_dir.grid    (row = 0, column = 0, sticky = tk.W) # Вызываем метод grid который задает расположение виджетов. Тупо сетка. Параметр sticky говорит о том, что элемент надо прилепить к какой то конкретной стороне ячейки (если параметр не задать, то виджет будет расположен по умолчанию в центр указанной на гриде ячейки, а это не очень красиво.
i_path.grid         (row = 0, column = 1)
i_label_base.grid   (row = 1, column = 0, sticky = tk.W)
i_combobox_base.grid(row = 1, column = 1, sticky = tk.W)
i_button_open.grid  (row = 0, column = 2)
i_label_var.grid    (row = 5, column = 0, sticky = tk.W)
i_combobox_var.grid (row = 5, column = 1, sticky = tk.W)
i_button_start.grid (row = 5, column = 2)

# Запускаем обработку всего что выше написали, что б наконец наше окно ожило
i_window.mainloop()