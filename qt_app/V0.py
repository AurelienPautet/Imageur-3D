# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'V0.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenu,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QTextBrowser, QWidget)

class Ui_Imageur3D(object):
    def setupUi(self, Imageur3D):
        if not Imageur3D.objectName():
            Imageur3D.setObjectName(u"Imageur3D")
        Imageur3D.resize(1080, 720)
        Imageur3D.setMinimumSize(QSize(1080, 720))
        Imageur3D.setMaximumSize(QSize(1080, 720))
        self.centralwidget = QWidget(Imageur3D)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 1081, 661))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.progressBar = QProgressBar(self.tab)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(800, 200, 118, 23))
        self.progressBar.setValue(24)
        self.pushButton = QPushButton(self.tab)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(760, 50, 111, 23))
        self.pushButton_2 = QPushButton(self.tab)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(890, 60, 111, 23))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.textBrowser = QTextBrowser(self.tab_2)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(0, 470, 1001, 161))
        self.label = QLabel(self.tab_2)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 435, 171, 31))
        self.label.setStyleSheet(u"font: 22pt \"MS Shell Dlg 2\";")
        self.pushButton_3 = QPushButton(self.tab_2)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(880, 40, 75, 23))
        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 60, 621, 321))
        self.label_2.setStyleSheet(u"background-color: rgb(0, 234, 255);")
        self.tabWidget.addTab(self.tab_2, "")
        Imageur3D.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Imageur3D)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1080, 31))
        self.menuhome = QMenu(self.menubar)
        self.menuhome.setObjectName(u"menuhome")
        Imageur3D.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Imageur3D)
        self.statusbar.setObjectName(u"statusbar")
        Imageur3D.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuhome.menuAction())

        self.retranslateUi(Imageur3D)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Imageur3D)
    # setupUi

    def retranslateUi(self, Imageur3D):
        Imageur3D.setWindowTitle(QCoreApplication.translate("Imageur3D", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("Imageur3D", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("Imageur3D", u"PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Imageur3D", u"Vrai experience", None))
        self.label.setText(QCoreApplication.translate("Imageur3D", u"Console :", None))
        self.pushButton_3.setText(QCoreApplication.translate("Imageur3D", u"PushButton", None))
        self.label_2.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Imageur3D", u"Simulation experience", None))
        self.menuhome.setTitle(QCoreApplication.translate("Imageur3D", u"home", None))
    # retranslateUi

