
    #---------- ПОДКЛЮЧАЕМ БИБЛИОТЕКИ ----------

import sys                          # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore # Виджеты для экранной формы
import Ui_design_pyqt as design     # Это наш конвертированный файл дизайна
import report                       # Собственно наш файл со всей логикой
import cx_Oracle                    # Конкретно тут не нужен, но если его притягивать только в модуле (body), то выеживается pyinstaller
import multiprocessing              # Нужно для торможения лишних окон из-за мультипроцессинга в модуле с логикой
import os                           # Выставляю через него переменные окружения

    #---------- КОНЕЦ ПОДКЛЮЧЕНИЯ БИБЛИОТЕК ----------

    
    #---------- ОБЪЯВЛЯЕМ ПЕРЕМЕННЫЕ ----------

signatorys = dict()
default_directory = ''

try:
    with open('set.txt', 'r') as file:
        os.environ["PATH"] = file.read()    # Выставляем переменную окружения, что б cx_oracle не ругался
except:
    print('Не найден файл настроек set.txt. PATH: ' + os.environ["PATH"] )

try:
    with open('signatorys.txt', 'r') as file:
        for line in file:
            lin = line.split('|')
            signatorys[lin[0]] = [lin[1].rstrip(),lin[2].rstrip()]     # Считываем справочник подписантов
except:
    print('Ошибка чтения списка подписантов signatorys.txt')

try:
    with open('default_directory.txt', 'r') as file:
        default_directory = file.read()
except:
    print('Ошибка чтения файла с дефолтной директорией default_directory.txt')

    #---------- КОНЕЦ ОБЪЯВЛЕНИЯ ПЕРЕМЕННЫХ ----------

    #---------- ОПИСЫВАЕМ КЛАСС "ПРИЛОЖЕНИЕ" ----------

class application(QtWidgets.QMainWindow, design.Ui_MainWindow):

    #---------- ФУНКЦИЯ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    

    def __init__(self):
       
        super().__init__()                                                  # Это здесь нужно для доступа к переменным, методам и т.д. в файле design.py
        self.setupUi(self)                                                  # Это нужно для инициализации нашего дизайна
        self.date_report.setDate(QtCore.QDate.currentDate().addDays(-1) )
        self.line_path.setText(default_directory)
        self.button_path.clicked.connect(self.browse_folder)                # Выполнить функцию browse_folder  при нажатии кнопки button_open
        self.button_start.clicked.connect(self.start)
        self.combo_why_action.currentTextChanged.connect(self.refresh)
        self.combo_why.setEnabled(False)
        for i in signatorys:
            self.combo_sign.addItem(signatorys[i][0], i)                    # Наполняем комбобокс с подписантами списком значений



    #---------- КОНЕЦ ФУНКЦИИ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    


    #---------- ФУНКЦИЯ "ОКНО ПОИСКА ДИРЕКТОРИИ" ----------    

    def browse_folder(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self,'Выбор директории для экспорта') 
        if directory:                                 # не продолжать выполнение, если пользователь не выбрал директорию
            self.line_path.clear()                    # На случай, если в списке уже есть элементы
            self.line_path.setText(directory)        

    #---------- КОНЕЦ ФУНКЦИЯ "ОКНО ПОИСКА ДИРЕКТОРИИ" ----------    

    #---------- ФУНКЦИЯ true => 81 false => 82 ----------    

    def if_nulls(self):
        if self.checkbox_if_nulls.isChecked():
            return 81
        else:
            return 82
            
    #---------- КОНЕЦ: ФУНКЦИЯ true => 81 false => 82 ----------    

    #---------- ФУНКЦИЯ "Обнови засериность полей" ----------   

    def refresh(self):
        if self.combo_why_action.currentText() == 'Сформировать и выгрузить':
            self.combo_why.setCurrentIndex(0)   # 'Всё'
            self.combo_why.setEnabled(False)
            self.checkbox_if_nulls.setEnabled(True)
            self.line_path.setEnabled(True)
            self.button_path.setEnabled(True)
        elif self.combo_why_action.currentText() == 'Сформировать':
            self.combo_why.setCurrentIndex(0)   # 'Всё'
            self.combo_why.setEnabled(False)
            self.checkbox_if_nulls.setEnabled(True)
            self.line_path.setEnabled(False)
            self.button_path.setEnabled(False)
        elif self.combo_why_action.currentText() == 'Выгрузить':
            self.combo_why.setEnabled(True)
            self.checkbox_if_nulls.setEnabled(False)
            self.line_path.setEnabled(True)
            self.button_path.setEnabled(True)

    #---------- КОНЕЦ: ФУНКЦИЯ "Обнови засериность полей" ----------   

    #---------- КОНЕЦ: ФУНКЦИИ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    

    #---------- ФУНКЦИЯ ПОД КНОПКОЙ "СТАРТ" ----------    
    
    def start(self):
        try:
            report.execute( USER        = self.line_user.text(),
                            PASSWORD    = self.line_pass.text(),
                            DB          = self.line_base.text(),
                            DATE        = str(self.date_report.date().toString("dd.MM.yyyy")),
                            PATH        = str(str(self.line_path.text()) + r'''\\'''),
                            WHAT        = self.combo_why.currentText(),
                            ACTION      = self.combo_why_action.currentText(),
                            USER_ID     = self.combo_sign.currentData(),
                            USER_STR    = signatorys[self.combo_sign.currentData()][1] + ' ' + signatorys[self.combo_sign.currentData()][0],
                            IF_NULLS    = self.if_nulls()
                            )
            QtWidgets.QMessageBox.information(self,'Информация', '''Формирование отчёта успешно завершено!''')
        except:
            QtWidgets.QMessageBox.information(self,'ERROR!!!', '''Произошла критическая ошибка:\n''' + str(sys.exc_info()) )
            

    #---------- ФУНКЦИЯ ПОД КНОПКОЙ "СТАРТ" ----------    


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
    multiprocessing.freeze_support( )   # Вот эта муть позволяет тормозить лишние окна, ибо мультипроцессинг их начинает активно генерить
    main()                              # то запускаем функцию main()

    #---------- КОНЕЦ ВЫЗОВА ФУНКЦИИ СОЗДАНИЯ ЭКРАННОЙ ФОРМЫ ----------