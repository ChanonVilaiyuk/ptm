# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'O:\studioTools\tools\ptTaskManager\userDialog.ui'
#
# Created: Wed Oct 14 12:32:03 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from qtshim import QtCore, QtGui
from qtshim import Signal
from qtshim import wrapinstance


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.localUser_lineEdit = QtGui.QLineEdit(Dialog)
        self.localUser_lineEdit.setObjectName(_fromUtf8("localUser_lineEdit"))
        self.verticalLayout.addWidget(self.localUser_lineEdit)
        self.user_listWidget = QtGui.QListWidget(Dialog)
        self.user_listWidget.setObjectName(_fromUtf8("user_listWidget"))
        self.verticalLayout.addWidget(self.user_listWidget)
        self.setUser_pushButton = QtGui.QPushButton(Dialog)
        self.setUser_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.setUser_pushButton.setObjectName(_fromUtf8("setUser_pushButton"))
        self.verticalLayout.addWidget(self.setUser_pushButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Please select Shotgun User", None))
        self.label_2.setText(_translate("Dialog", "Local User", None))
        self.setUser_pushButton.setText(_translate("Dialog", "Set User", None))

