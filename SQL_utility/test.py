from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidgetItem
 
from widgets import CustomTableWidget
 
 
# Наследование от QMainWindow
class MainWindow(QMainWindow):
    # Overriding the class constructor
    def __init__(self):
        # Обязательно вызовите метод суперкласса
        QMainWindow.__init__(self)
 
        self.setMinimumSize(QSize(480, 80))  # Установить размеры
        self.setWindowTitle("Работа с QTableWidget")  # Установите заголовок окна
        central_widget = QWidget(self)  # Создать центральный виджет
        self.setCentralWidget(central_widget)  # Установить центральный виджет
 
        grid_layout = QGridLayout()  # Создать QGridLayout
        central_widget.setLayout(grid_layout)  # Установите это размещение в центральном виджете
 
        table = CustomTableWidget(self)  # Создать таблицу
        table.setColumnCount(3)  # Мы устанавливаем три колонки
        table.setRowCount(1)  # и один ряд в таблице
 
        # Установить заголовки таблицы
        table.setHorizontalHeaderLabels(["Header 1", "Header 2", "Header 3"])
 
        # Установить подсказки для заголовков
        table.horizontalHeaderItem(0).setToolTip("Column 1 ")
        table.horizontalHeaderItem(1).setToolTip("Column 2 ")
        table.horizontalHeaderItem(2).setToolTip("Column 3 ")
 
        # Установите выравнивание к заголовкам
        table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)
 
        # заполните первую строку
        table.setItem(0, 0, self.createItem("Text in column 1", Qt.ItemIsSelectable | Qt.ItemIsEnabled))
        table.setItem(0, 1, self.createItem("Text in column 2", Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable))
        table.setItem(0, 2, self.createItem("Text in column 3", Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable))
 
        # изменить размер столбца по содержимому
        table.resizeColumnsToContents()
 
        #grid_layout.addWidget(table, 0, 0)  # Add a table to the grid
 
    def createItem(self, text, flags):
        tableWidgetItem = QTableWidgetItem(text)
        tableWidgetItem.setFlags(flags)
        return tableWidgetItem
 
 
if __name__ == "__main__":
    import sys
 
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())