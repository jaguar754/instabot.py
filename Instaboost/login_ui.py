# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Echo(object):
    def setupUi(self, Echo):
        Echo.setObjectName("Echo")
        Echo.resize(268, 194)
        self.loginEdit = QtWidgets.QLineEdit(Echo)
        self.loginEdit.setGeometry(QtCore.QRect(80, 60, 131, 20))
        self.loginEdit.setObjectName("loginEdit")
        self.senhaEdit = QtWidgets.QLineEdit(Echo)
        self.senhaEdit.setGeometry(QtCore.QRect(80, 90, 131, 20))
        self.senhaEdit.setInputMask("")
        self.senhaEdit.setMaxLength(32767)
        self.senhaEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.senhaEdit.setObjectName("senhaEdit")
        self.label = QtWidgets.QLabel(Echo)
        self.label.setGeometry(QtCore.QRect(20, 60, 51, 20))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Echo)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 51, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.confirmarButton = QtWidgets.QPushButton(Echo)
        self.confirmarButton.setGeometry(QtCore.QRect(130, 130, 75, 23))
        self.confirmarButton.setObjectName("confirmarButton")
        self.label_11 = QtWidgets.QLabel(Echo)
        self.label_11.setGeometry(QtCore.QRect(60, 20, 131, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.infoLabel = QtWidgets.QLabel(Echo)
        self.infoLabel.setGeometry(QtCore.QRect(90, 110, 111, 20))
        self.infoLabel.setText("")
        self.infoLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.infoLabel.setObjectName("infoLabel")

        self.retranslateUi(Echo)
        QtCore.QMetaObject.connectSlotsByName(Echo)

    def retranslateUi(self, Echo):
        _translate = QtCore.QCoreApplication.translate
        Echo.setWindowTitle(_translate("Echo", "Instaboost"))
        self.loginEdit.setText(_translate("Echo", "usuariobeta"))
        self.senhaEdit.setText(_translate("Echo", "usuariobeta"))
        self.label.setText(_translate("Echo", "Login:"))
        self.label_2.setText(_translate("Echo", "Senha:"))
        self.confirmarButton.setText(_translate("Echo", "Confirmar"))
        self.label_11.setText(_translate("Echo", "Instaboost - beta"))

