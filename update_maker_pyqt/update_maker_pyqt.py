
    #---------- ПОДКЛЮЧАЕМ БИБЛИОТЕКИ ----------

import sys                      # sys нужен для передачи argv в QApplication
import os                       # Отсюда нам понадобятся методы для отображения содержимого директорий
import subprocess               # Нужно для запуска процесса инсталяции
from PyQt5 import QtWidgets     # Виджеты для экранной формы
import upd_mk_exec        as um # Наш самописный модуль с логикой запаковки файлов в обновление
import design_pyqt as design    # Это наш конвертированный файл дизайна
from tkinter import messagebox  # Высплывающие окна

    #---------- КОНЕЦ ПОДКЛЮЧЕНИЯ БИБЛИОТЕК ----------


    #---------- ОБЪЯВЛЯЕМ ПЕРЕМЕННЫЕ ----------

path                = ''                   # Директория.
path_stock          = r'''X:\Инверсия\ФОНД\U\FUND_DB\TEST'''
path_build_stock    = '''\\PATH'''
path_stock_scripts  = r'''\\fs-inversiya\inversiya$\инверсия\ФОНД\Скрипты'''

    #---------- КОНЕЦ ОБЪЯВЛЕНИЯ ПЕРЕМЕННЫХ ----------


    #---------- ОПИСЫВАЕМ КЛАСС "ПРИЛОЖЕНИЕ" ----------

class update_maker_App(QtWidgets.QMainWindow, design.Ui_MainWindow):

    #---------- ФУНКЦИЯ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    

    def __init__(self):
       
        super().__init__()                                     # Это здесь нужно для доступа к переменным, методам и т.д. в файле design.py
        self.setupUi(self)                                     # Это нужно для инициализации нашего дизайна
        
        self.button_open.clicked.connect(self.browse_folder)   # Выполнить функцию browse_folder  при нажатии кнопки button_open
        self.button_start.clicked.connect(self.start)
        
     

    #---------- КОНЕЦ ФУНКЦИИ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    


    #---------- ФУНКЦИЯ "ОКНО ПОИСКА ДИРЕКТОРИИ" ----------    

    def browse_folder(self):
        
        #options = QtWidgets.QFileDialog.Options()                                       # Призываем настройки диалогового окна
        #options |= QtWidgets.QFileDialog.DontUseNativeDialog                            # Приказываем не юзать нативный диалог (что б окно пользовало Windows'скую функцию поиска директорий, а не свою стрёмную)
        directory = QtWidgets.QFileDialog.getOpenFileName(self, 'open',)
        #QtWidgets.QFileDialog.getExistingDirectory(self, 'Open file', path_stock, QtWidgets.QFileDialog.DontUseNativeDialog)  # Открыть диалог выбора директории и установить значение переменной равной пути к выбранной директории

        if directory:                                  # не продолжать выполнение, если пользователь не выбрал директорию
            self.line_dir.clear()                      # На случай, если в списке уже есть элементы
            direct = ''.join(directory)
            i = direct.rindex(r'/')  # last occurrence
            direct = direct[:i]
            self.line_dir.setText(direct)        
            
    #---------- КОНЕЦ ФУНКЦИИ "ОКНО ПОИСКА ДИРЕКТОРИИ" ----------    


    #---------- ФУНКЦИЯ ПОД КНОПКОЙ "СТАРТ" ----------    
    
    def start(self):

        try: 
            global path_build_stock
            i_dir = self.line_dir.text()
            i_base = self.line_base.text()
            path_build = i_dir + path_build_stock
            
            um.exec(PATH = i_dir , PATH_BUILD = path_build, PATH_STOCK_SCRIPTS = path_stock_scripts)
            
            if self.radio_install.isChecked():
                    s = subprocess.Popen( path_build + r'''\\RunMe.bat ''' + i_base , cwd = path_build, creationflags=subprocess.CREATE_NEW_CONSOLE)
                    s.communicate ()
            else:
                    #message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.information, 'Info', QtWidgets.QMessageBox.Ok)
                    #message.exec_()
                    #messagebox.showinfo('Info', 'Обновление запаковано в ' + path_build)
                    print (hui)
        except:
            print ('hui')
            #messagebox.showinfo('ERROR!!!', '''ОБНОВЛЕНИЕ НЕ ЗАПАКОВАНО!!!\nПроизошла ошибка в процедуре запаковки:\n''' + str(sys.exc_info()) )
        finally:
            path_build = ''

        

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