# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QListView, QMainWindow,
    QMenu, QMenuBar, QProgressBar, QPushButton,
    QRadioButton, QSizePolicy, QStatusBar, QTabWidget,
    QTextBrowser, QWidget)

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
        self.simulationTab = QWidget()
        self.simulationTab.setObjectName(u"simulationTab")
        self.consoleLayout = QTextBrowser(self.simulationTab)
        self.consoleLayout.setObjectName(u"consoleLayout")
        self.consoleLayout.setGeometry(QRect(0, 470, 1001, 161))
        self.label = QLabel(self.simulationTab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 435, 111, 31))
        self.label.setStyleSheet(u"font: 22pt \"MS Shell Dlg 2\";")
        self.simulateObjectButton = QPushButton(self.simulationTab)
        self.simulateObjectButton.setObjectName(u"simulateObjectButton")
        self.simulateObjectButton.setGeometry(QRect(30, 370, 141, 51))
        self.progressBar_2 = QProgressBar(self.simulationTab)
        self.progressBar_2.setObjectName(u"progressBar_2")
        self.progressBar_2.setGeometry(QRect(560, 440, 301, 23))
        self.progressBar_2.setValue(0)
        self.label_3 = QLabel(self.simulationTab)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(420, 430, 191, 41))
        self.label_3.setStyleSheet(u"font: 22pt \"MS Shell Dlg 2\";")
        self.resultTabWidget = QTabWidget(self.simulationTab)
        self.resultTabWidget.setObjectName(u"resultTabWidget")
        self.resultTabWidget.setGeometry(QRect(30, 10, 621, 351))
        self.result = QWidget()
        self.result.setObjectName(u"result")
        self.result.setStyleSheet(u"background-color : rgb(197,197,197);")
        self.affichage = QLabel(self.result)
        self.affichage.setObjectName(u"affichage")
        self.affichage.setGeometry(QRect(0, 0, 621, 321))
        self.affichage.setStyleSheet(u"background-color: rgb(197,197,197);")
        self.resultTabWidget.addTab(self.result, "")
        self.autoScrollButton = QRadioButton(self.simulationTab)
        self.autoScrollButton.setObjectName(u"autoScrollButton")
        self.autoScrollButton.setGeometry(QRect(150, 440, 151, 31))
        self.autoScrollButton.setChecked(True)
        self.informationList = QListView(self.simulationTab)
        self.informationList.setObjectName(u"informationList")
        self.informationList.setGeometry(QRect(700, 40, 291, 321))
        self.label_2 = QLabel(self.simulationTab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(710, 10, 271, 20))
        self.frangesButton = QPushButton(self.simulationTab)
        self.frangesButton.setObjectName(u"frangesButton")
        self.frangesButton.setGeometry(QRect(170, 390, 201, 32))
        self.TroisDButton = QPushButton(self.simulationTab)
        self.TroisDButton.setObjectName(u"TroisDButton")
        self.TroisDButton.setGeometry(QRect(370, 370, 141, 51))
        self.radioButton = QRadioButton(self.simulationTab)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(170, 370, 51, 20))
        self.radioButton_2 = QRadioButton(self.simulationTab)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(240, 370, 121, 20))
        self.autoButton = QPushButton(self.simulationTab)
        self.autoButton.setObjectName(u"autoButton")
        self.autoButton.setGeometry(QRect(520, 370, 121, 51))
        self.tabWidget.addTab(self.simulationTab, "")
        self.scanTab = QWidget()
        self.scanTab.setObjectName(u"scanTab")
        self.progressBar = QProgressBar(self.scanTab)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(800, 200, 118, 23))
        self.progressBar.setValue(24)
        self.pushButton = QPushButton(self.scanTab)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(760, 50, 111, 23))
        self.pushButton_2 = QPushButton(self.scanTab)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(890, 60, 111, 23))
        self.tabWidget.addTab(self.scanTab, "")
        Imageur3D.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Imageur3D)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1080, 24))
        self.menuhome = QMenu(self.menubar)
        self.menuhome.setObjectName(u"menuhome")
        Imageur3D.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Imageur3D)
        self.statusbar.setObjectName(u"statusbar")
        Imageur3D.setStatusBar(self.statusbar)

        self.

        self.menubar.addAction(self.menuhome.menuAction())

        self.retranslateUi(Imageur3D)

        self.tabWidget.setCurrentIndex(0)
        self.resultTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Imageur3D)
    # setupUi

    def retranslateUi(self, Imageur3D):
        Imageur3D.setWindowTitle(QCoreApplication.translate("Imageur3D", u"Imageur 3D", None))
        self.label.setText(QCoreApplication.translate("Imageur3D", u"Console :", None))
        self.simulateObjectButton.setText(QCoreApplication.translate("Imageur3D", u"Simuler un objet", None))
        self.label_3.setText(QCoreApplication.translate("Imageur3D", u"Progress :", None))
        self.affichage.setText(QCoreApplication.translate("Imageur3D", u"<html><head/><body><p align=\"center\">Ici s'affichera le r\u00e9sultat des diff\u00e9rentes \u00e9tapes de la simulation</p></body></html>", None))
        self.resultTabWidget.setTabText(self.resultTabWidget.indexOf(self.result), QCoreApplication.translate("Imageur3D", u"Resultat of the simulation", None))
        self.autoScrollButton.setText(QCoreApplication.translate("Imageur3D", u"AUTO SCROLL", None))
        self.label_2.setText(QCoreApplication.translate("Imageur3D", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Informations</span></p></body></html>", None))
        self.frangesButton.setText(QCoreApplication.translate("Imageur3D", u"G\u00e9n\u00e9rer les franges", None))
        self.TroisDButton.setText(QCoreApplication.translate("Imageur3D", u"Retrouver les \n"
" coordonn\u00e9es 3D", None))
        self.radioButton.setText(QCoreApplication.translate("Imageur3D", u"Bruit", None))
        self.radioButton_2.setText(QCoreApplication.translate("Imageur3D", u"Halo de lumi\u00e8re", None))
        self.autoButton.setText(QCoreApplication.translate("Imageur3D", u"Auto", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.simulationTab), QCoreApplication.translate("Imageur3D", u"Simulation", None))
        self.pushButton.setText(QCoreApplication.translate("Imageur3D", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("Imageur3D", u"PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.scanTab), QCoreApplication.translate("Imageur3D", u"Scan", None))
        self.menuhome.setTitle(QCoreApplication.translate("Imageur3D", u"home", None))
    # retranslateUi

