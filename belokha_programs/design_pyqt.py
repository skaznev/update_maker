# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_test.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(648, 102)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.line_dir = QtWidgets.QLineEdit(self.centralwidget)
        self.line_dir.setGeometry(QtCore.QRect(160, 10, 391, 20))
        self.line_dir.setObjectName("line_dir")
        self.line_base = QtWidgets.QLineEdit(self.centralwidget)
        self.line_base.setGeometry(QtCore.QRect(160, 40, 133, 20))
        self.line_base.setObjectName("line_base")
        self.button_open = QtWidgets.QPushButton(self.centralwidget)
        self.button_open.setGeometry(QtCore.QRect(560, 10, 75, 23))
        self.button_open.setObjectName("button_open")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 151, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 151, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 151, 16))
        self.label_3.setObjectName("label_3")
        self.button_start = QtWidgets.QPushButton(self.centralwidget)
        self.button_start.setGeometry(QtCore.QRect(560, 70, 75, 21))
        self.button_start.setObjectName("button_start")
        self.radio_pack = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_pack.setGeometry(QtCore.QRect(160, 70, 82, 17))
        self.radio_pack.setAcceptDrops(False)
        self.radio_pack.setAutoFillBackground(False)
        self.radio_pack.setChecked(True)
        self.radio_pack.setObjectName("radio_pack")
        self.radio_install = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_install.setGeometry(QtCore.QRect(260, 70, 82, 17))
        self.radio_install.setObjectName("radio_install")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Программа запаковки/установки обновлений ФОНД"))
        self.button_open.setText(_translate("MainWindow", "Open"))
        self.label.setText(_translate("MainWindow", "Директория с обновлением:"))
        self.label_2.setText(_translate("MainWindow", "Обновляемая база:"))
        self.label_3.setText(_translate("MainWindow", "Что сделать:"))
        self.button_start.setText(_translate("MainWindow", "Start"))
        self.radio_pack.setText(_translate("MainWindow", "Запаковать"))
        self.radio_install.setText(_translate("MainWindow", "Установить"))
