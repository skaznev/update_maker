# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\projects\update_maker\xls_parser_for_kravchenko\design_pyqt.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(422, 41)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button_start = QtWidgets.QPushButton(self.centralwidget)
        self.button_start.setGeometry(QtCore.QRect(350, 10, 61, 21))
        self.button_start.setObjectName("button_start")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label_7.setObjectName("label_7")
        self.line_path = QtWidgets.QLineEdit(self.centralwidget)
        self.line_path.setGeometry(QtCore.QRect(90, 10, 181, 20))
        self.line_path.setText("")
        self.line_path.setObjectName("line_path")
        self.button_path = QtWidgets.QPushButton(self.centralwidget)
        self.button_path.setGeometry(QtCore.QRect(280, 10, 61, 21))
        self.button_path.setObjectName("button_path")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Формирование скрипта по W8"))
        self.button_start.setText(_translate("MainWindow", "Start"))
        self.label_7.setText(_translate("MainWindow", "Директория:"))
        self.button_path.setText(_translate("MainWindow", "Open"))
