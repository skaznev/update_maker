
    #---------- ПОДКЛЮЧАЕМ БИБЛИОТЕКИ ----------

import sys                          # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore # Виджеты для экранной формы
import Ui_design                    # Это наш конвертированный файл дизайна
import body                         # Собственно наш файл со всей логикой

    #---------- КОНЕЦ ПОДКЛЮЧЕНИЯ БИБЛИОТЕК ----------

    
    #---------- ОБЪЯВЛЯЕМ ПЕРЕМЕННЫЕ ----------


    #---------- КОНЕЦ ОБЪЯВЛЕНИЯ ПЕРЕМЕННЫХ ----------


    #---------- ОПИСЫВАЕМ КЛАСС "ПРИЛОЖЕНИЕ" ----------

class application(QtWidgets.QMainWindow, Ui_design.Ui_MainWindow):

    #---------- ФУНКЦИЯ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    

    def __init__(self):
       
        super().__init__()                                                  # Это здесь нужно для доступа к переменным, методам и т.д. в файле design.py
        self.setupUi(self)                                                  # Это нужно для инициализации нашего дизайна
        self.button_clear.clicked.connect(self.clear)                       # Выполнить функцию browse_folder  при нажатии кнопки button_open        
        self.button_start.clicked.connect(self.start)
    
    #---------- КОНЕЦ ФУНКЦИИ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    
 
    #---------- ФУНКЦИЯ "Очисть список объектов" ----------    

    def clear(self):
        self.text_param_addit.clear()

    #---------- КОНЕЦ ФУНКЦИИ "Очисть список объектов" ----------    

    #---------- ФУНКЦИЯ "ПРОВЕРЬ, ЕСТЬ ЛИ ОШИБКИ" ----------   

    def errors(self):
        # Чекнем список объектов
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
                # Погнали 
                result = body.execute(PATH         = self.line_path.text(),
                                      LIST_OBJECTS = self.text_param_addit.toPlainText().split('\n')
                                     )
                if result == '':
                    QtWidgets.QMessageBox.information(self,'Информация', '''Пересечений нет!''')                                        
                else:
                    QtWidgets.QMessageBox.information(self,'Информация', '''Список пересечений:\n''' + result)
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
    main()                              # то запускаем функцию main()

    #---------- КОНЕЦ ВЫЗОВА ФУНКЦИИ СОЗДАНИЯ ЭКРАННОЙ ФОРМЫ ----------