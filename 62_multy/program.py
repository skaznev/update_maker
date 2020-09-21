
import sys                          # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore # Виджеты для экранной формы
import design
import dtsec
import cx_Oracle
import os

try:
    with open('set.txt', 'r') as file:
        os.environ["PATH"] = file.read()                                    # Выставляем переменную окружения, что б cx_oracle не ругался
        print('Считали set.txt')
except:
    print('Не найден файл настроек set.txt. PATH: ' + os.environ["PATH"] )

class application(QtWidgets.QMainWindow, design.Ui_MainWindow):

    #---------- ФУНКЦИЯ ИНИЦИАЛИЗАЦИИ КЛАССА ----------    

    def __init__(self):
       
        super().__init__()                                                  # Это здесь нужно для доступа к переменным, методам и т.д. в файле design.py
        self.setupUi(self)   
        self.fix_date.setDate(QtCore.QDate.currentDate())
        self.nrd_date.setDate(QtCore.QDate.currentDate())
        self.button_path.clicked.connect(self.browse_folder)                # Выполнить функцию browse_folder  при нажатии кнопки button_open
        self.button_start_2.clicked.connect(self.start)


    def browse_folder(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, r'Выбор директории для экспорта') 
        if directory:                                 # не продолжать выполнение, если пользователь не выбрал директорию
            self.exp_dir.clear()                    # На случай, если в списке уже есть элементы
            self.exp_dir.setText(directory)


    def start(self):
        try:
            if_nominal = 83
            if self.if_nominal.isChecked():
                if_nominal = 81
            else:
                if_nominal = 82
            dtsec.execute(USER = self.line_user.text(), PAS = self.line_pass.text(), DB = self.line_base.text(), REPORT_DATE = str(self.fix_date.date().toString("dd.MM.yyyy")), NRD_DATE = str(self.nrd_date.date().toString("dd.MM.yyyy")), NRD_NOTICE = self.nrd_notice.text(), REF_KD = self.ref_kd.text(), LIST_TYPE = self.list_type.currentText(), SEC_ISIN_LIST = self.isin_list.text(), STORAGE_LIST = self.storage_list.text(), IF_NOMINAL = if_nominal, PART = self.parts.text(), OUT_PATH = str(str(self.exp_dir.text()) + r'/'))
            QtWidgets.QMessageBox.information(self,'Информация', '''Файлы были успешно экспортированы. Каталог:\n''' + str(self.exp_dir.text()) )
        except Exception as e:
            QtWidgets.QMessageBox.information(self,'ERROR!!!', '''Произошла критическая ошибка:\n''' + str(e))
       

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = application()                  # Создаём объект класса application
    window.show()                           # Показываем окно
    app.exec_()  

if __name__ == '__main__':              # Если мы запускаем файл напрямую, а не импортируем
    main()