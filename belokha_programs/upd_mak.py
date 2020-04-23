
#---------- ОБЪЯВЛЯЕМ БИБЛИОТЕКИ ----------

import sys                  # sys нужен для передачи argv в QApplication
import os                   # Отсюда нам понадобятся методы для отображения содержимого директорий
import subprocess           # Модуль для запуска процессов
from PyQt5 import QtWidgets # Виджеты для ПГШ
import design               # Это наш конвертированный файл дизайна

#---------- КОНЕЦ ОБЪЯВЛЕНИЯ БИБЛИОТЕК ----------


#---------- ОБЪЯВЛЯЕМ КОНСТАНТЫ ----------

i_base              = ''

i_login_fund_db     = ''
i_login_fund_dev    = ''

i_pass_fund_db      = ''
i_pass_fund_dev     = ''

i_sql_start         = '''

begin
  TR_TOOL_UPDATE.ADD_TO_LOG(i_action => 'INSERT');
  TR_TOOL.CI;
end;
/

'''
i_sql_end           = '''

begin
  TR_TOOL.CI;
  TR_TOOL.FND_2USR;
  TR_TOOL.FND_2ADM;
  TR_TOOL.CI;
  TR_TOOL_UPDATE.ADD_TO_LOG(i_action => 'UPDATE');
end;
/

'''

i_sql_metadata      = '''

begin
   TR_TOOL_METADATA.EXECUTE_ALL;
end;
/

'''

#---------- КОНЕЦ ОБЪЯВЛЕНИЯ КОНСТАНТ ----------


#---------- ОБЪЯВЛЯЕМ КЛАСС "ПРИЛОЖЕНИЕ" ----------

class application(QtWidgets.QMainWindow, design.Ui_MainWindow):
    
#---------- ФУНКЦИЯ ИНИЦИАЦИИ КЛАССА (ВЫПОЛЯЕТСЯ ПЕРВОЙ) ----------    
    
    def __init__(self):                                             # Это здесь нужно для доступа к переменным, методам и т.д. в файле design.py
        
        super().__init__()
        self.setupUi(self)                                          # Это нужно для инициализации нашего дизайна
        
#---------- ПРИВЯЗЫВАЕМ ФУНКЦИИ К КНОПКАМ ----------

        self.pushButton_3.clicked.connect   (self.browse_folder)    # Выполнить функцию browse_folder  при нажатии кнопки
        self.pushButton_2.clicked.connect   (self.install)                                                    
        self.pushButton.clicked.connect     (self.close)

#---------- КОНЕЦ ПРИВЯЗКИ ФУНКЦИЙ К КНОПКАМ ----------


#---------- ОБЪЯВЛЯЕМ ПЕРЕМЕННЫЕ ----------

        self.step = 0                                               # "Шаги" для прогрессбара
        self.text = 'Начало обновления.\n'                          # Переменная с текстом лога
        
        self.dir = os.getcwd()                                      # Текущая директория
        self.dir = os.chdir(os.path.join(self.dir , 'objects'))     # Директория с объектами в патче
        
        self.connect_string     = ''                                # Строка коннекта. Юзаю простой коннект через ТНС: 'FUND_DB/FUND_DB@XXI_PRE'
        self.sqlplus_start      = ''                                # Комманды для sqlplus'a
        self.sqlplus_table      = ''
        self.sqlplus_view       = ''
        self.sqlplus_pack       = ''
        self.sqlplus_end        = ''
        self.sqlplus_metadata   = ''
        self.sqlplus_script     = ''

#---------- КОНЕЦ ОБЪЯВЛЯЕМ ПЕРЕМЕННЫХ ----------        


#---------- ФУНКЦИЯ "ОКНО ВЫБОРА ДИРЕКТОРИИ" ----------

    def browse_folder(self):
        
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")  # открыть диалог выбора директории и установить значение переменной равной пути к выбранной директории
        if directory:                                                                   # не продолжать выполнение, если пользователь не выбрал директорию
            self.lineEdit_2.clear()                                                     # На случай, если в списке уже есть элементы
            self.lineEdit_2.setText(directory)
            
#---------- КОНЕЦ ФУНКЦИИ "ОКНО ВЫБОРА ДИРЕКТОРИИ" ----------


#---------- ФУНКЦИЯ "УСТАНОВКА ОБНОВЛЕНИЯ" ----------

    def install(self):

        self.connect_string = 'connect ' + i_login_fund_db + '/' + i_login_fund_db + '@' + i_base + '\n'
        
        self.sqlplus_start      = i_sql_start
        self.sqlplus_table      = ''
        self.sqlplus_view       = ''
        self.sqlplus_pack       = ''
        self.sqlplus_end        = i_sql_end
        self.sqlplus_metadata   = i_sql_metadata
        self.sqlplus_script     = ''

        self.push(self.sqlplus_start)       # 1
        self.push(self.sqlplus_table)       # 2
        self.push(self.sqlplus_view)        # 3
        self.push(self.sqlplus_pack)        # 4
        self.push(self.sqlplus_end)         # 5
        self.push(self.sqlplus_metadata)    # 6
        self.push(self.sqlplus_script)      # 7

        

#---------- КОНЕЦ ФУНКЦИИ "УСТАНОВКА ОБНОВЛЕНИЯ" ----------


#---------- ФУНКЦИЯ ПРИМЕНЕНИЯ SQL КОММАНД----------

    def push (self, sqlplus):
        
        self.text = self.run_sqlplus(sqlplus)

        if not self.step == 75:
            self.step = self.step + 12.5             
            self.progressBar.setValue(self.step)
            self.statusbar.showMessage('ВЫПОЛНЯЕТСЯ: УСТАНОВКА ОБНОВЛЕНИЯ')
        else:
            self.progressBar.setValue(100)
        
        self.textBrowser.insertPlainText(self.text)
        self.textBrowser.ensureCursorVisible()

#---------- КОНЕЦ ФУНКЦИИ ПРИМЕНЕНИЯ SQL КОММАНД ----------


#---------- ФУНКЦИЯ ЗАПУСКА ПРОЦЕССА УСТАНОВКИ ----------

    def run_sqlplus(self , sqlplus_script):

        text_out = ''
        sqlplus_script = self.connect_string + sqlplus_script
        p = subprocess.Popen(['sqlplus','/nolog'], cwd= self.dir ,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        (stdout, stderr) = p.communicate(sqlplus_script.encode('windows-1251'))
        stdout_lines     = stdout.decode('windows-1251').split("\n")
        for line in stdout_lines:
            text_out += line + '\n'
        return text_out

#---------- КОНЕЦ ФУНКЦИИ ЗАПУСКА ПРОЦЕССА УСТАНОВКИ ----------


#---------- КОНЕЦ КЛАССА "ПРИЛОЖЕНИЕ" ----------


#---------- ОСНОВНАЯ ФУНКЦИЯ, КОТОРАЯ ЗАПУСКАЕТ ПРИЛОЖЕНИЕ ----------

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication

    window = application()                  # Создаём объект класса application
    window.show()                           # Показываем окно
    app.exec_()                             # и запускаем приложение

#---------- КОНЕЦ ФУНКЦИИ, КОТОРАЯ ЗАПУСКАЕТИ ПРИЛОЖЕНИЕ ----------

if __name__ == '__main__':                  # Если мы запускаем файл напрямую, а не импортируем
    main()                                  # то запускаем функцию main()