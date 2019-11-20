# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'beta.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from client import *
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Chat(object):
    def setupUi(self, Chat):
        Chat.setObjectName("Chat")
        Chat.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Chat)
        self.centralwidget.setObjectName("centralwidget")
        # self.startServer = QtWidgets.QPushButton(self.centralwidget)
        # self.startServer.setGeometry(QtCore.QRect(150, 110, 111, 41))
        # self.startServer.setObjectName("startServer")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(430, 160, 256, 192))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(700, 370, 51, 41))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(430, 370, 251, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.connectServer = QtWidgets.QPushButton(self.centralwidget)
        self.connectServer.setGeometry(QtCore.QRect(158, 194, 101, 41))
        self.connectServer.setObjectName("connectServer")
        self.connectServer.clicked.connect(self.connect_server)
        Chat.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Chat)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        Chat.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Chat)
        self.statusbar.setObjectName("statusbar")
        Chat.setStatusBar(self.statusbar)
        self.actionClose = QtWidgets.QAction(Chat)
        self.actionClose.setObjectName("actionClose")
        self.menuFile.addAction(self.actionClose)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(Chat)
        QtCore.QMetaObject.connectSlotsByName(Chat)

    def retranslateUi(self, Chat):
        _translate = QtCore.QCoreApplication.translate
        Chat.setWindowTitle(_translate("Chat", "MainWindow"))
        self.startServer.setText(_translate("Chat", "Start Server"))
        self.pushButton.setText(_translate("Chat", "Send"))
        self.connectServer.setText(_translate("Chat", "PushButton"))
        self.menuFile.setTitle(_translate("Chat", "File"))
        self.actionClose.setText(_translate("Chat", "Close"))

    def connect_server(self):
        client_initiate()

    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Chat = QtWidgets.QMainWindow()
    ui = Ui_Chat()
    ui.setupUi(Chat)
    Chat.show()
    sys.exit(app.exec_())
