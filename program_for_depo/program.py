
    #---------- ПОДКЛЮЧАЕМ БИБЛИОТЕКИ ----------

import sys                      # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets     # Виджеты для экранной формы
import design                   # Это наш конвертированный файл дизайна
import body         as mxml     # Вся логика
import cx_Oracle                # Конкретно тут не нужен, но если его притягивать только в модуле (body), то выеживается pyinstaller
import os                       # Выставляю через него переменные окружения

    #---------- КОНЕЦ ПОДКЛЮЧЕНИЯ БИБЛИОТЕК ----------


    #---------- ОБЪЯВЛЯЕМ ПЕРЕМЕННЫЕ ----------

path_in     = ''                        # Директория с исходными файлами
path_out    = ''                        # Директория с обработанными файлами
try:
    with open('set.txt', 'r') as file:
        os.environ["PATH"] = file.read()    # Выставляем переменную окружения, что б cx_oracle не ругался
except:
    print('Не найден файл настроек set.txt. PATH: ' + os.environ["PATH"] )


    #---------- КОНЕЦ ОБЪЯВЛЕНИЯ ПЕРЕМЕННЫХ ----------


    #---------- ОПИСЫВАЕМ КЛАСС "ПРИЛОЖЕНИЕ" ----------

class update_maker_App(QtWidgets.QMainWindow, design.Ui_MainWindow):

    #---------- ФУНКЦИЯ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    

    def __init__(self):
       
        super().__init__()                                     # Это здесь нужно для доступа к переменным, методам и т.д. в файле design.py
        self.setupUi(self)                                     # Это нужно для инициализации нашего дизайна
        
        self.button_open_1.clicked.connect(self.browse_folder_1)   # Выполнить функцию browse_folder  при нажатии кнопки button_open
        self.button_open_2.clicked.connect(self.browse_folder_2)   # Выполнить функцию browse_folder  при нажатии кнопки button_open
        self.button_start.clicked.connect(self.start)
        
    #---------- КОНЕЦ ФУНКЦИИ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    


    #---------- ФУНКЦИЯ "ОКНО ПОИСКА ДИРЕКТОРИИ" ----------    

    def browse_folder_1(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self,'Выбор директории с обрабатываемыми файлами') 
        if directory:                                  # не продолжать выполнение, если пользователь не выбрал директорию
            self.line_dir_1.clear()                    # На случай, если в списке уже есть элементы
            self.line_dir_1.setText(directory)        

    def browse_folder_2(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self,'Выбор директории с готовыми файлами') 
        if directory:                                  # не продолжать выполнение, если пользователь не выбрал директорию
            self.line_dir_2.clear()                    # На случай, если в списке уже есть элементы
            self.line_dir_2.setText(directory)        
    

    #---------- КОНЕЦ ФУНКЦИИ "ОКНО ПОИСКА ДИРЕКТОРИИ" ----------    


    #---------- ФУНКЦИЯ ПОД КНОПКОЙ "СТАРТ" ----------    
    
    def start(self):
        try: 
            mxml.execute(PATH_IN = self.line_dir_1.text(), PATH_OUT = self.line_dir_2.text(), USER = self.line_user.text(), PASSWORD = self.line_pass.text(), DATABASE = self.line_base.text())
            QtWidgets.QMessageBox.information(self,'Информация', '''Файлы были успешно обработаны. Каталог:\n''' + str(self.line_dir_2.text()) )
        except:
            QtWidgets.QMessageBox.information(self,'ERROR!!!', '''Произошла критическая ошибка:\n''' + str(sys.exc_info()) )
            

    #---------- ФУНКЦИЯ ПОД КНОПКОЙ "СТАРТ" ----------    


    #---------- КОНЕЦ КЛАССА "ПРИЛОЖЕНИЕ" ----------
            

    #---------- ФУНКЦИЯ ПРИЗЫВА ЭКРАННОЙ ФОРМЫ НА ЭКРАН ----------

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = update_maker_App()             # Создаём объект класса update_maker_App
    window.show()                           # Показываем окно
    app.exec_()                             # и запускаем приложение

    #---------- КОНЕЦ ФУНКЦИИ ПРИЗЫВА ЭКРАННОЙ ФОРМЫ НА ЭКРАН ----------


    #---------- ВЫЗОВ ФУНКЦИИ СОЗДАНИЯ ЭКРАННОЙ ФОРМЫ ----------

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()                  # то запускаем функцию main()

    #---------- КОНЕЦ ВЫЗОВА ФУНКЦИИ СОЗДАНИЯ ЭКРАННОЙ ФОРМЫ ----------