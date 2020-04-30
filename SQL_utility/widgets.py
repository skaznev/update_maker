from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QTableWidget
 
 
# Мы создаем собственный QTableWidget для реагирования на события нажатия клавиш
class CustomTableWidget(QTableWidget):
 
    # переопределяем keyPressEvent
    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key_Enter:
            print("Key enter was pressed")
        elif e.key() == Qt.Key_Return:
            print("Key return was pressed")