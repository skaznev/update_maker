
    #---------- ПОДКЛЮЧАЕМ БИБЛИОТЕКИ ----------

import sys                          # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore # Виджеты для экранной формы
import Ui_design_pyqt as design     # Это наш конвертированный файл дизайна
import parsser as report            # Собственно наш файл со всей логикой

    #---------- КОНЕЦ ПОДКЛЮЧЕНИЯ БИБЛИОТЕК ----------

    
    #---------- ОБЪЯВЛЯЕМ ПЕРЕМЕННЫЕ ----------

try:
    with open('W8Script_for_parser.sql', 'r') as file:
         sql_text= file.read()    
except:
    print('Не найден файл со скриптом ')

    #---------- КОНЕЦ ОБЪЯВЛЕНИЯ ПЕРЕМЕННЫХ ----------

    #---------- ОПИСЫВАЕМ КЛАСС "ПРИЛОЖЕНИЕ" ----------

class application(QtWidgets.QMainWindow, design.Ui_MainWindow):

    #---------- ФУНКЦИЯ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    

    def __init__(self):
       
        super().__init__()                                                  # Это здесь нужно для доступа к переменным, методам и т.д. в файле design.py
        self.setupUi(self)                                                  # Это нужно для инициализации нашего дизайна
        self.button_path.clicked.connect(self.browse_folder)                # Выполнить функцию browse_folder  при нажатии кнопки button_open
        self.button_start.clicked.connect(self.start)

    #---------- КОНЕЦ ФУНКЦИИ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    


    #---------- ФУНКЦИЯ "ОКНО ПОИСКА ДИРЕКТОРИИ" ----------    

    def browse_folder(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self,'Выбор файла отчёта', filter = 'Excel (*);;Excel (*.xlsx)',initialFilter = 'Excel (*.xlsx)') 
        if directory:                                 # не продолжать выполнение, если пользователь не выбрал директорию
            self.line_path.clear()                    # На случай, если в списке уже есть элементы
            self.line_path.setText(directory[0])        

    #---------- КОНЕЦ ФУНКЦИЯ "ОКНО ПОИСКА ДИРЕКТОРИИ" ----------    

    #---------- КОНЕЦ: ФУНКЦИИ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    

    #---------- ФУНКЦИЯ ПОД КНОПКОЙ "СТАРТ" ----------    
    
    def start(self):
        try:
            report.execute( PATH_BOOK = str(str(self.line_path.text())), SQL_TEXT = sql_text)
            QtWidgets.QMessageBox.information(self,'Информация', '''Формирование скрипта успешно завершено!''')
        except Exception as e:
            QtWidgets.QMessageBox.information(self,'ERROR!!!', '''Произошла критическая ошибка:\n''' + str(e))
            

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
    main()                              # то запускаем функцию main()

    #---------- КОНЕЦ ВЫЗОВА ФУНКЦИИ СОЗДАНИЯ ЭКРАННОЙ ФОРМЫ ----------