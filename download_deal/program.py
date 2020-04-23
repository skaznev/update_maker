
    #---------- ПОДКЛЮЧАЕМ БИБЛИОТЕКИ ----------

import sys                          # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore # Виджеты для экранной формы
import Ui_design                    # Это наш конвертированный файл дизайна
import body                         # Собственно наш файл со всей логикой
import cx_Oracle                    # Конкретно тут не нужен, но если его притягивать только в модуле (body), то выеживается pyinstaller
import multiprocessing              # Нужно для торможения лишних окон из-за мультипроцессинга в модуле с логикой
import os                           # Выставляю через него переменные окружения

    #---------- КОНЕЦ ПОДКЛЮЧЕНИЯ БИБЛИОТЕК ----------

    
    #---------- ОБЪЯВЛЯЕМ ПЕРЕМЕННЫЕ ----------

try:
    with open('set.txt', 'r') as file:
        os.environ["PATH"] = file.read()    # Выставляем переменную окружения, что б cx_oracle не ругался
except:
    print('Не найден файл настроек set.txt. PATH: ' + os.environ["PATH"] )

    #---------- КОНЕЦ ОБЪЯВЛЕНИЯ ПЕРЕМЕННЫХ ----------


    #---------- ОПИСЫВАЕМ КЛАСС "ПРИЛОЖЕНИЕ" ----------

class application(QtWidgets.QMainWindow, Ui_design.Ui_MainWindow):

    #---------- ФУНКЦИЯ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    

    def __init__(self):
       
        super().__init__()                                                  # Это здесь нужно для доступа к переменным, методам и т.д. в файле design.py
        self.setupUi(self)                                                  # Это нужно для инициализации нашего дизайна
        self.date_from.setDate(QtCore.QDate.currentDate().addDays(-1))
        self.date_to.setDate(QtCore.QDate.currentDate())
        self.date_from.dateChanged.connect(self.set_date)
        self.button_start.clicked.connect(self.start)
        
    #---------- КОНЕЦ ФУНКЦИИ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    

    #---------- ФУНКЦИЯ "ПЕРЕСЧИТАЙ ПРАВУЮ ДАТУ" ----------    

    def set_date(self):
        self.date_to.setDate(self.date_from.date().addDays(1))

    #---------- КОНЕЦ: ФУНКЦИЯ "ПЕРЕСЧИТАЙ ПРАВУЮ ДАТУ" ----------    

    #---------- ФУНКЦИЯ ПОД КНОПКОЙ "СТАРТ" ----------    
    
    def start(self):
        try:
            body.execute(USER = self.line_user.text(), PASSWORD = self.line_pass.text(), DB = self.line_base.text(), DATE_FROM = str(self.date_from.date().toString("yyyy.MM.dd")), DATE_TO = str(self.date_to.date().toString("yyyy.MM.dd")), TYPE_DATE = self.combo_type_date.currentText(), WHAT = self.combo_why.currentText(), PATH = os.path.join(os.getcwd(), 'export'))
            QtWidgets.QMessageBox.information(self,'Информация', '''Сделки были успешно экспортированы.''' )
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
    multiprocessing.freeze_support( )   # Вот эта муть позволяет тормозить лишние окна, ибо мультипроцессинг начинает их активно генерить
    main()                              # то запускаем функцию main()

    #---------- КОНЕЦ ВЫЗОВА ФУНКЦИИ СОЗДАНИЯ ЭКРАННОЙ ФОРМЫ ----------