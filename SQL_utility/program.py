
    #---------- ПОДКЛЮЧАЕМ БИБЛИОТЕКИ ----------

import sys                          # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore # Виджеты для экранной формы
import Ui_design                    # Это наш конвертированный файл дизайна
import body                         # Собственно наш файл со всей логикой
import cx_Oracle                    # Конкретно тут не нужен, но если его притягивать только в модуле (body), то выеживается pyinstaller
import multiprocessing              # Нужно для торможения лишних окон из-за мультипроцессинга в модуле с логикой
import os                           # Выставляю через него переменные окружения
import datetime                     # Нужно для генерации ключа

    #---------- КОНЕЦ ПОДКЛЮЧЕНИЯ БИБЛИОТЕК ----------

    
    #---------- ОБЪЯВЛЯЕМ ПЕРЕМЕННЫЕ ----------

path_select     = os.path.join(os.getcwd(), 'QUERY')   # Директория с селектами
path_script     = os.path.join(os.getcwd(), 'SCRIPT')  # Директория со скриптами
dict_sql        = dict()                               # Справочник SQL инструкций (скрипты и селекты). Структура записи: название файла, [тип(селект/скрипт), текст инструкции]
type_select     = 'Выгрузить'
type_script     = 'Выполнить'
i_param_delim   = r'|'
i_param_log     = r'$P0'
i_param_basic   = r'$P'
i_param_add     = r'$PARAM'
i_param_date_1  = r'$D1'
i_param_date_2  = r'$D2'
i_delimiter     = r'-- $delimiter = '
i_threads_cnt   = r'-- $threads = '
i_columns       = r'-- $columns = '


try:
    with open('set.txt', 'r') as file:
        os.environ["PATH"] = file.read()                                    # Выставляем переменную окружения, что б cx_oracle не ругался
except:
    gg = os.environ["PATH"]
    os.environ["PATH"] = gg.replace(r'X:\orant\bin;', '')
    print('Не найден файл настроек set.txt. PATH: ' + os.environ["PATH"] )

try:
    sql_files_select = os.listdir(path_select)                              # Читаем директорию с файлами с селектами
    select = [f for f in sql_files_select if ( f.upper()[-4:] == ".SQL")]   # Отбираем оттуда SQL файлы
    for item in select:
        with open(os.path.join(path_select, item), 'r', encoding= 'Windows-1251') as file:
            dict_sql[item] = [type_select, file.read()]                     # Наполняем справочник селектами
    
    sql_files_script = os.listdir(path_script)                              # Читаем директорию с файлами со скриптами
    script = [f for f in sql_files_script if ( f.upper()[-4:] == ".SQL")]   # Отбираем оттуда SQL файлы
    for item in script:
        with open(os.path.join(path_script, item), 'r', encoding= 'Windows-1251') as file:
            dict_sql[item] = [type_script, file.read()]                     # Наполняем справочник скриптами
except Exception as e:
    print('Ошибка чтения SQL инструкций: ' + str(e))

    #---------- КОНЕЦ ОБЪЯВЛЕНИЯ ПЕРЕМЕННЫХ ----------


    #---------- ОПИСЫВАЕМ КЛАСС "ПРИЛОЖЕНИЕ" ----------

class application(QtWidgets.QMainWindow, Ui_design.Ui_MainWindow):

    #---------- ФУНКЦИЯ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    

    def __init__(self):
       
        super().__init__()                                                  # Это здесь нужно для доступа к переменным, методам и т.д. в файле design.py
        self.setupUi(self)                                                  # Это нужно для инициализации нашего дизайна
        self.date_from.setDate(QtCore.QDate.currentDate().addDays(-1))      # Ставим дату "вчера"
        self.date_to.setDate(QtCore.QDate.currentDate())
        self.date_from.dateChanged.connect(self.set_date)
        self.button_open.clicked.connect(self.browse_folder)                # Выполнить функцию browse_folder  при нажатии кнопки button_open        
        self.button_start.clicked.connect(self.start)
        self.table_param_basic.setSortingEnabled(False)                     # Отключаем сортировку в таблице основных парамтеров
        self.combo_why.currentTextChanged.connect(self.refresh)
        self.combo_sql.currentTextChanged.connect(self.refresh_param)
        self.refresh()

        # Установить подсказки для заголовков
        self.table_param_basic.horizontalHeaderItem(0).setToolTip("Все входные параметры выбраного скрипта")
        self.table_param_basic.horizontalHeaderItem(1).setToolTip("Значения, передаваемые скрипту")
    
    #---------- КОНЕЦ ФУНКЦИИ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    

    #---------- ФУНКЦИЯ "ПЕРЕСЧИТАЙ ПРАВУЮ ДАТУ" ----------    

    def set_date(self):
        self.date_to.setDate(self.date_from.date().addDays(1))

    #---------- КОНЕЦ: ФУНКЦИЯ "ПЕРЕСЧИТАЙ ПРАВУЮ ДАТУ" ----------    
 
    #---------- ФУНКЦИЯ "Выбор файла для экспорта" ----------    

    def browse_folder(self):
        directory = QtWidgets.QFileDialog.getSaveFileName(self,'Выбор файла для экспорта', filter = 'CSV (*.csv)',initialFilter = 'CSV (*.csv)') 
        if directory:                                                       # не продолжать выполнение, если пользователь не выбрал директорию
            self.line_path.clear()                                          # На случай, если в списке уже есть элементы
            self.line_path.setText(directory[0])        

    #---------- ФУНКЦИЯ "ПЕРЕЧИТАЙ ПОЛЯ" ----------   

    def refresh(self):
        self.combo_sql.clear()
        for i in dict_sql:
            if dict_sql[i][0] == self.combo_why.currentText():
                self.combo_sql.addItem(i[:-4], i)                           # Наполняем комбобокс со скриптами списком значений
        if self.combo_why.currentText() == 'Выполнить':
            self.line_path.setEnabled(False)
            self.button_open.setEnabled(False)
        else:
            self.line_path.setEnabled(True)
            self.button_open.setEnabled(True)

    #---------- КОНЕЦ: ФУНКЦИЯ "ПЕРЕЧИТАЙ ПОЛЯ" ----------   

    #---------- ФУНКЦИЯ "ПЕРЕЧИТАЙ ПОЛЯ С ПАРАМЕТРАМИ" ----------   

    def refresh_param(self):
        if self.combo_sql.currentData():                                                # Выполняем только если заполнено поле (так как стоит триггер на смену значения)
            line_param = dict_sql[self.combo_sql.currentData()][1].split('\n')[0][3:]   # Берем первую строку из файла и читаем с третьей позиции("-- ")
            self.add_basic_param(line_param)

    def add_basic_param(self, text):
        list_param = text.split(i_param_delim)
        if not list_param == ['']:      # Отсекаем пустые 
            self.table_param_basic.setRowCount(len(list_param))
            for i, param in enumerate(list_param):
                self.table_param_basic.setItem(i, 0, self.createItem(param, QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled))
        else:
            self.table_param_basic.setRowCount(0)

    def createItem(self, text, flags):
        tableWidgetItem = QtWidgets.QTableWidgetItem(text)
        tableWidgetItem.setFlags(flags)
        return tableWidgetItem

    #---------- КОНЕЦ: ФУНКЦИЯ "ПЕРЕЧИТАЙ ПОЛЯ С ПАРАМЕТРАМИ" ----------   

    #---------- ФУНКЦИЯ "НАЙДИ ЗНАЧЕНИЕ ПАРАМЕТРА" ----------       
    
    def return_param(self, text, param):
        for line in text.split('\n'):
            if param in line:
                return line[len(param):]
        return '1'

    #---------- КОНЕЦ: ФУНКЦИЯ "НАЙДИ ЗНАЧЕНИЕ ПАРАМЕТРА" ----------   

    #---------- ФУНКЦИЯ "ОБОГАТИ СКРИПТ ПАРАМЕТРАМИ" ----------   

    def param_to_sql(self, sql, code_run):
        # Базовые параметры
        if not self.table_param_basic.rowCount() == 0:
            for i in reversed(range(self.table_param_basic.rowCount())):    # В обратном порядке так как были ошибки что мы $P10 первым же параметром реплейсили (так как находили в нем $P1)
                sql = sql.replace(i_param_basic + str(i+1), '\'' + self.table_param_basic.item(i, 1).text() + '\'')
        # Дополнительные параметры
        param_add = ''
        param_addit = self.text_param_addit.toPlainText().split('\n')
        if param_addit:
            for i, line in enumerate(param_addit):
                param_add += '\'' + line + '\'' + '\n'
                if not i == len(param_addit) - 1:
                    param_add += ','
        sql = sql.replace(i_param_add, param_add)
        # Даты левая правая
        sql = sql.replace(i_param_date_1, '\'' + str(self.date_from.date().toString("dd.MM.yyyy")) + '\'')
        sql = sql.replace(i_param_date_2, '\'' + str(self.date_to.date().toString("dd.MM.yyyy")) + '\'')
        # Идентификатор лога
        sql = sql.replace(i_param_log, '\'' + code_run + '\'')

        #with open(os.getcwd() + r'\\' + code_run + '_' + r'''.txt''' ,'w', encoding= 'Windows-1251') as File:
        #    File.write(sql)

        return sql

    #---------- КОНЕЦ: ФУНКЦИЯ "ОБОГАТИ СКРИПТ ПАРАМЕТРАМИ" ----------   

    #---------- ФУНКЦИЯ "ПРОВЕРЬ, ЕСТЬ ЛИ ОШИБКИ" ----------   

    def errors(self):
        # Чекнем креды
        if (not self.line_user.text()) or (not self.line_pass.text()) or (not self.line_base.text()):
            return True
        # Чекнем базовые параметры
        if not self.table_param_basic.rowCount() == 0:
            for i in range(self.table_param_basic.rowCount()):
                if self.table_param_basic.item(i, 1) == None:
                    return True
        # Чекнем директорию
        if self.combo_why.currentText() == type_select:
            if not self.line_path.text():
                return True
        # Чекнем дополнительные параметры
        if i_param_add in dict_sql[self.combo_sql.currentData()][1]:
            if not self.text_param_addit.toPlainText():
                return True
        return False

    #---------- КОНЕЦ: ФУНКЦИЯ "ПРОВЕРЬ, ЕСТЬ ЛИ ОШИБКИ" ----------   

    #---------- ФУНКЦИЯ ПОД КНОПКОЙ "СТАРТ" ----------    
    
    def start(self):
        if self.errors():
            QtWidgets.QMessageBox.information(self,'ERROR!!!', '''Заполнены не все необходимые параметры! Выполнение невозможно.''')
        else:
            try:
                # Замутим код запуска
                code_run = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                # Начитаем sql                 
                sql = dict_sql[self.combo_sql.currentData()][1]     
                # Погнали в базу    
                logs = body.execute(USER        = self.line_user.text(),
                                    PASSWORD    = self.line_pass.text(),
                                    DB          = self.line_base.text(),
                                    WHAT        = self.combo_why.currentText(),
                                    PATH        = self.line_path.text(),
                                    SQL_NAME    = self.combo_sql.currentText(),
                                    SQL         = self.param_to_sql(sql = sql, code_run = code_run),
                                    DELIMITER   = self.return_param(text = sql, param = i_delimiter),
                                    THREADS_CNT = self.return_param(text = sql, param = i_threads_cnt),
                                    COLUMNS     = self.return_param(text = sql, param = i_columns),
                                    CODE_RUN    = code_run
                                    )
                QtWidgets.QMessageBox.information(self,'Информация', '''Завершено успешно!\n''' + logs)
            except Exception as e:
                QtWidgets.QMessageBox.information(self,'ERROR!!!', '''Произошла критическая ошибка:\n''' + str(e))
            

    #---------- КОНЕЦ: ФУНКЦИЯ ПОД КНОПКОЙ "СТАРТ" ----------    


    #---------- КОНЕЦ КЛАССА "ПРИЛОЖЕНИЕ" ----------
            

    #---------- ФУНКЦИЯ ПРИЗЫВА ЭКРАННОЙ ФОРМЫ НА ЭКРАН ----------

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = application()                  # Создаём объект класса application
    window.show()                           # Показываем окно
    app.exec_()                             # и запускаем приложение

    #---------- КОНЕЦ ФУНКЦИИ ПРИЗЫВА ЭКРАННОЙ ФОРМЫ НА ЭКРАН ----------


    #---------- ВЫЗОВ ФУНКЦИИ СОЗДАНИЯ ЭКРАННОЙ ФОРМЫ ----------

if __name__ == '__main__':              # Если мы запускаем файл напрямую, а не импортируем
    multiprocessing.freeze_support()    # Вот эта муть позволяет тормозить лишние окна, ибо мультипроцессинг начинает их активно генерить
    main()                              # то запускаем функцию main()

    #---------- КОНЕЦ ВЫЗОВА ФУНКЦИИ СОЗДАНИЯ ЭКРАННОЙ ФОРМЫ ----------