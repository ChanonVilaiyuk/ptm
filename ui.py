# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'O:\studioTools\tools\ptm\ui.ui'
#
# Created: Tue Mar 08 14:55:28 2016
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from qtshim import QtCore, QtGui
from qtshim import Signal
from qtshim import wrapinstance


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_taskManager(object):
    def setupUi(self, taskManager):
        taskManager.setObjectName(_fromUtf8("taskManager"))
        taskManager.resize(1029, 636)
        self.centralwidget = QtGui.QWidget(taskManager)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.user_comboBox = QtGui.QComboBox(self.frame)
        self.user_comboBox.setObjectName(_fromUtf8("user_comboBox"))
        self.gridLayout_2.addWidget(self.user_comboBox, 1, 1, 1, 1)
        self.project_comboBox = QtGui.QComboBox(self.frame)
        self.project_comboBox.setObjectName(_fromUtf8("project_comboBox"))
        self.gridLayout_2.addWidget(self.project_comboBox, 2, 1, 1, 1)
        self.step_comboBox = QtGui.QComboBox(self.frame)
        self.step_comboBox.setObjectName(_fromUtf8("step_comboBox"))
        self.gridLayout_2.addWidget(self.step_comboBox, 2, 7, 1, 1)
        self.episode_comboBox = QtGui.QComboBox(self.frame)
        self.episode_comboBox.setEnabled(True)
        self.episode_comboBox.setObjectName(_fromUtf8("episode_comboBox"))
        self.gridLayout_2.addWidget(self.episode_comboBox, 2, 3, 1, 1)
        self.entity_comboBox = QtGui.QComboBox(self.frame)
        self.entity_comboBox.setObjectName(_fromUtf8("entity_comboBox"))
        self.gridLayout_2.addWidget(self.entity_comboBox, 2, 5, 1, 1)
        self.label_10 = QtGui.QLabel(self.frame)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 2, 6, 1, 1)
        self.label_6 = QtGui.QLabel(self.frame)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 2, 4, 1, 1)
        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 2, 2, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 2)
        self.gridLayout_2.setColumnStretch(2, 1)
        self.gridLayout_2.setColumnStretch(3, 2)
        self.gridLayout_2.setColumnStretch(4, 1)
        self.gridLayout_2.setColumnStretch(5, 2)
        self.gridLayout_2.setColumnStretch(6, 1)
        self.gridLayout_2.setColumnStretch(7, 2)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.path_lineEdit = QtGui.QLineEdit(self.frame)
        self.path_lineEdit.setText(_fromUtf8(""))
        self.path_lineEdit.setObjectName(_fromUtf8("path_lineEdit"))
        self.horizontalLayout_2.addWidget(self.path_lineEdit)
        self.status_label = QtGui.QLabel(self.frame)
        self.status_label.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.status_label.setObjectName(_fromUtf8("status_label"))
        self.horizontalLayout_2.addWidget(self.status_label)
        self.refresh_pushButton = QtGui.QPushButton(self.frame)
        self.refresh_pushButton.setObjectName(_fromUtf8("refresh_pushButton"))
        self.horizontalLayout_2.addWidget(self.refresh_pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_7.addWidget(self.frame)
        self.logo2_label = QtGui.QLabel(self.centralwidget)
        self.logo2_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.logo2_label.setObjectName(_fromUtf8("logo2_label"))
        self.horizontalLayout_7.addWidget(self.logo2_label)
        self.logo_label = QtGui.QLabel(self.centralwidget)
        self.logo_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.logo_label.setObjectName(_fromUtf8("logo_label"))
        self.horizontalLayout_7.addWidget(self.logo_label)
        self.horizontalLayout_7.setStretch(0, 18)
        self.horizontalLayout_7.setStretch(1, 3)
        self.horizontalLayout_7.setStretch(2, 3)
        self.verticalLayout_9.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame_4 = QtGui.QFrame(self.centralwidget)
        self.frame_4.setFrameShape(QtGui.QFrame.Box)
        self.frame_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.label_9 = QtGui.QLabel(self.frame_4)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout_8.addWidget(self.label_9)
        self.status_listWidget = QtGui.QListWidget(self.frame_4)
        self.status_listWidget.setObjectName(_fromUtf8("status_listWidget"))
        self.verticalLayout_8.addWidget(self.status_listWidget)
        self.verticalLayout_5.addLayout(self.verticalLayout_8)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.label_7 = QtGui.QLabel(self.frame_4)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_6.addWidget(self.label_7)
        self.task_listWidget = QtGui.QListWidget(self.frame_4)
        self.task_listWidget.setObjectName(_fromUtf8("task_listWidget"))
        self.verticalLayout_6.addWidget(self.task_listWidget)
        self.verticalLayout_5.addLayout(self.verticalLayout_6)
        self.verticalLayout_5.setStretch(0, 4)
        self.verticalLayout_5.setStretch(1, 2)
        self.horizontalLayout.addWidget(self.frame_4)
        self.frame_6 = QtGui.QFrame(self.centralwidget)
        self.frame_6.setFrameShape(QtGui.QFrame.Box)
        self.frame_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_6.setObjectName(_fromUtf8("frame_6"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.frame_6)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.info_label = QtGui.QLabel(self.frame_6)
        self.info_label.setObjectName(_fromUtf8("info_label"))
        self.verticalLayout_10.addWidget(self.info_label)
        self.line = QtGui.QFrame(self.frame_6)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_10.addWidget(self.line)
        self.verticalLayout_11 = QtGui.QVBoxLayout()
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.entity_label = QtGui.QLabel(self.frame_6)
        self.entity_label.setObjectName(_fromUtf8("entity_label"))
        self.verticalLayout_11.addWidget(self.entity_label)
        self.entities_listWidget = QtGui.QListWidget(self.frame_6)
        self.entities_listWidget.setObjectName(_fromUtf8("entities_listWidget"))
        self.verticalLayout_11.addWidget(self.entities_listWidget)
        self.note_checkBox = QtGui.QCheckBox(self.frame_6)
        self.note_checkBox.setChecked(True)
        self.note_checkBox.setObjectName(_fromUtf8("note_checkBox"))
        self.verticalLayout_11.addWidget(self.note_checkBox)
        self.line_2 = QtGui.QFrame(self.frame_6)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout_11.addWidget(self.line_2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.search_lineEdit = QtGui.QLineEdit(self.frame_6)
        self.search_lineEdit.setObjectName(_fromUtf8("search_lineEdit"))
        self.horizontalLayout_5.addWidget(self.search_lineEdit)
        self.search_pushButton = QtGui.QPushButton(self.frame_6)
        self.search_pushButton.setObjectName(_fromUtf8("search_pushButton"))
        self.horizontalLayout_5.addWidget(self.search_pushButton)
        self.verticalLayout_11.addLayout(self.horizontalLayout_5)
        self.verticalLayout_10.addLayout(self.verticalLayout_11)
        self.horizontalLayout.addWidget(self.frame_6)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 4)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)
        self.frame_5 = QtGui.QFrame(self.centralwidget)
        self.frame_5.setFrameShape(QtGui.QFrame.Box)
        self.frame_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_5.setObjectName(_fromUtf8("frame_5"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.frame_5)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.frame_2 = QtGui.QFrame(self.frame_5)
        self.frame_2.setFrameShape(QtGui.QFrame.Box)
        self.frame_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.work_radioButton = QtGui.QRadioButton(self.frame_2)
        self.work_radioButton.setChecked(True)
        self.work_radioButton.setObjectName(_fromUtf8("work_radioButton"))
        self.horizontalLayout_3.addWidget(self.work_radioButton)
        self.publish_radioButton = QtGui.QRadioButton(self.frame_2)
        self.publish_radioButton.setObjectName(_fromUtf8("publish_radioButton"))
        self.horizontalLayout_3.addWidget(self.publish_radioButton)
        self.source_radioButton = QtGui.QRadioButton(self.frame_2)
        self.source_radioButton.setObjectName(_fromUtf8("source_radioButton"))
        self.horizontalLayout_3.addWidget(self.source_radioButton)
        self.verticalLayout_7.addWidget(self.frame_2)
        self.work_listWidget = QtGui.QListWidget(self.frame_5)
        self.work_listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.work_listWidget.setObjectName(_fromUtf8("work_listWidget"))
        self.verticalLayout_7.addWidget(self.work_listWidget)
        self.ip_checkBox = QtGui.QCheckBox(self.frame_5)
        self.ip_checkBox.setChecked(True)
        self.ip_checkBox.setObjectName(_fromUtf8("ip_checkBox"))
        self.verticalLayout_7.addWidget(self.ip_checkBox)
        self.new_pushButton = QtGui.QPushButton(self.frame_5)
        self.new_pushButton.setObjectName(_fromUtf8("new_pushButton"))
        self.verticalLayout_7.addWidget(self.new_pushButton)
        self.open_pushButton = QtGui.QPushButton(self.frame_5)
        self.open_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.open_pushButton.setObjectName(_fromUtf8("open_pushButton"))
        self.verticalLayout_7.addWidget(self.open_pushButton)
        self.horizontalLayout_6.addWidget(self.frame_5)
        self.frame_8 = QtGui.QFrame(self.centralwidget)
        self.frame_8.setFrameShape(QtGui.QFrame.Box)
        self.frame_8.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_8.setObjectName(_fromUtf8("frame_8"))
        self.verticalLayout_13 = QtGui.QVBoxLayout(self.frame_8)
        self.verticalLayout_13.setObjectName(_fromUtf8("verticalLayout_13"))
        self.label_12 = QtGui.QLabel(self.frame_8)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.verticalLayout_13.addWidget(self.label_12)
        self.comment_plainTextEdit = QtGui.QPlainTextEdit(self.frame_8)
        self.comment_plainTextEdit.setObjectName(_fromUtf8("comment_plainTextEdit"))
        self.verticalLayout_13.addWidget(self.comment_plainTextEdit)
        self.showAll_checkBox = QtGui.QCheckBox(self.frame_8)
        self.showAll_checkBox.setChecked(True)
        self.showAll_checkBox.setObjectName(_fromUtf8("showAll_checkBox"))
        self.verticalLayout_13.addWidget(self.showAll_checkBox)
        self.label_13 = QtGui.QLabel(self.frame_8)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.verticalLayout_13.addWidget(self.label_13)
        self.sourceFiles_listWidget = QtGui.QListWidget(self.frame_8)
        self.sourceFiles_listWidget.setObjectName(_fromUtf8("sourceFiles_listWidget"))
        self.verticalLayout_13.addWidget(self.sourceFiles_listWidget)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.openAs_radioButton = QtGui.QRadioButton(self.frame_8)
        self.openAs_radioButton.setObjectName(_fromUtf8("openAs_radioButton"))
        self.horizontalLayout_4.addWidget(self.openAs_radioButton)
        self.import_radioButton = QtGui.QRadioButton(self.frame_8)
        self.import_radioButton.setObjectName(_fromUtf8("import_radioButton"))
        self.horizontalLayout_4.addWidget(self.import_radioButton)
        self.reference_radioButton = QtGui.QRadioButton(self.frame_8)
        self.reference_radioButton.setObjectName(_fromUtf8("reference_radioButton"))
        self.horizontalLayout_4.addWidget(self.reference_radioButton)
        self.verticalLayout_13.addLayout(self.horizontalLayout_4)
        self.open_pushButton_2 = QtGui.QPushButton(self.frame_8)
        self.open_pushButton_2.setMinimumSize(QtCore.QSize(0, 30))
        self.open_pushButton_2.setObjectName(_fromUtf8("open_pushButton_2"))
        self.verticalLayout_13.addWidget(self.open_pushButton_2)
        self.horizontalLayout_6.addWidget(self.frame_8)
        self.horizontalLayout_6.setStretch(0, 11)
        self.horizontalLayout_6.setStretch(1, 7)
        self.horizontalLayout_6.setStretch(2, 6)
        self.verticalLayout_9.addLayout(self.horizontalLayout_6)
        taskManager.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(taskManager)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1029, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        taskManager.setMenuBar(self.menubar)

        self.retranslateUi(taskManager)
        QtCore.QMetaObject.connectSlotsByName(taskManager)

    def retranslateUi(self, taskManager):
        taskManager.setWindowTitle(QtGui.QApplication.translate("taskManager", "pt Task Manager v.2.0", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("taskManager", "Project : ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("taskManager", "User : ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("taskManager", "Dept : ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("taskManager", "Entity : ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("taskManager", "Episode : ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("taskManager", "Path : ", None, QtGui.QApplication.UnicodeUTF8))
        self.status_label.setText(QtGui.QApplication.translate("taskManager", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.refresh_pushButton.setText(QtGui.QApplication.translate("taskManager", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.logo2_label.setText(QtGui.QApplication.translate("taskManager", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.logo_label.setText(QtGui.QApplication.translate("taskManager", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("taskManager", "Status : ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("taskManager", "Tasks : ", None, QtGui.QApplication.UnicodeUTF8))
        self.info_label.setText(QtGui.QApplication.translate("taskManager", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.entity_label.setText(QtGui.QApplication.translate("taskManager", "Asset / Shot", None, QtGui.QApplication.UnicodeUTF8))
        self.note_checkBox.setText(QtGui.QApplication.translate("taskManager", "Show note", None, QtGui.QApplication.UnicodeUTF8))
        self.search_pushButton.setText(QtGui.QApplication.translate("taskManager", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.work_radioButton.setText(QtGui.QApplication.translate("taskManager", "Work area", None, QtGui.QApplication.UnicodeUTF8))
        self.publish_radioButton.setText(QtGui.QApplication.translate("taskManager", "Publish area", None, QtGui.QApplication.UnicodeUTF8))
        self.source_radioButton.setText(QtGui.QApplication.translate("taskManager", "Source file", None, QtGui.QApplication.UnicodeUTF8))
        self.ip_checkBox.setText(QtGui.QApplication.translate("taskManager", "Always set status to \"in progress\"", None, QtGui.QApplication.UnicodeUTF8))
        self.new_pushButton.setText(QtGui.QApplication.translate("taskManager", "New work file", None, QtGui.QApplication.UnicodeUTF8))
        self.open_pushButton.setText(QtGui.QApplication.translate("taskManager", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("taskManager", "Comment : ", None, QtGui.QApplication.UnicodeUTF8))
        self.showAll_checkBox.setText(QtGui.QApplication.translate("taskManager", "Show all note", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("taskManager", "source files : ", None, QtGui.QApplication.UnicodeUTF8))
        self.openAs_radioButton.setText(QtGui.QApplication.translate("taskManager", "Open as", None, QtGui.QApplication.UnicodeUTF8))
        self.import_radioButton.setText(QtGui.QApplication.translate("taskManager", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.reference_radioButton.setText(QtGui.QApplication.translate("taskManager", "Reference", None, QtGui.QApplication.UnicodeUTF8))
        self.open_pushButton_2.setText(QtGui.QApplication.translate("taskManager", "Open", None, QtGui.QApplication.UnicodeUTF8))

