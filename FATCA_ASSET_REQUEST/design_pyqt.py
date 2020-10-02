# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_pyqt.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(644, 141)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.line_dir_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.line_dir_1.setGeometry(QtCore.QRect(240, 40, 311, 20))
        self.line_dir_1.setObjectName("line_dir_1")
        self.button_open_1 = QtWidgets.QPushButton(self.centralwidget)
        self.button_open_1.setGeometry(QtCore.QRect(560, 40, 75, 23))
        self.button_open_1.setObjectName("button_open_1")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(10, 40, 221, 16))
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 181, 16))
        self.label_2.setObjectName("label_2")
        self.button_start = QtWidgets.QPushButton(self.centralwidget)
        self.button_start.setGeometry(QtCore.QRect(560, 100, 75, 21))
        self.button_start.setObjectName("button_start")
        self.line_dir_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.line_dir_2.setGeometry(QtCore.QRect(240, 70, 311, 20))
        self.line_dir_2.setObjectName("line_dir_2")
        self.button_open_2 = QtWidgets.QPushButton(self.centralwidget)
        self.button_open_2.setGeometry(QtCore.QRect(560, 70, 75, 23))
        self.button_open_2.setObjectName("button_open_2")
        self.line_base = QtWidgets.QLineEdit(self.centralwidget)
        self.line_base.setGeometry(QtCore.QRect(240, 100, 71, 20))
        self.line_base.setObjectName("line_base")
        self.line_user = QtWidgets.QLineEdit(self.centralwidget)
        self.line_user.setGeometry(QtCore.QRect(330, 100, 101, 20))
        self.line_user.setObjectName("line_user")
        self.line_pass = QtWidgets.QLineEdit(self.centralwidget)
        self.line_pass.setGeometry(QtCore.QRect(450, 100, 101, 20))
        self.line_pass.setObjectName("line_pass")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 100, 181, 16))
        self.label_4.setObjectName("label_4")
        self.combo_file_type = QtWidgets.QComboBox(self.centralwidget)
        self.combo_file_type.setGeometry(QtCore.QRect(240, 10, 307, 22))
        self.combo_file_type.setEditable(False)
        self.combo_file_type.setMinimumContentsLength(0)
        self.combo_file_type.setObjectName("combo_file_type")
        self.combo_file_type.addItem("")
        self.combo_file_type.addItem("")
        self.combo_file_type.addItem("")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 221, 16))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Программа обработки файлов Депозитария"))
        self.button_open_1.setText(_translate("MainWindow", "Open"))
        self.label_1.setText(_translate("MainWindow", "Директория с обрабатываемыми файлами:"))
        self.label_2.setText(_translate("MainWindow", "Директория с готовыми файлами:"))
        self.button_start.setText(_translate("MainWindow", "Start"))
        self.button_open_2.setText(_translate("MainWindow", "Open"))
        self.label_4.setText(_translate("MainWindow", "База, пользователь, пароль:"))
        self.combo_file_type.setCurrentText(_translate("MainWindow", "FATCA_ASSET_PAYMENT_REQUEST"))
        self.combo_file_type.setItemText(0, _translate("MainWindow", "FATCA_ASSET_PAYMENT_REQUEST"))
        self.combo_file_type.setItemText(1, _translate("MainWindow", "FATCA_ASSET_REQUEST"))
        self.combo_file_type.setItemText(2, _translate("MainWindow", "PLANNED_ASSET_REQUEST"))
        self.label_3.setText(_translate("MainWindow", "Тип файла"))
