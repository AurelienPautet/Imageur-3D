# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TEST.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_Imageur3D(object):
    def setupUi(self, Imageur3D):
        if not Imageur3D.objectName():
            Imageur3D.setObjectName(u"Imageur3D")
        Imageur3D.resize(1080, 720)
        Imageur3D.setMinimumSize(QSize(1080, 720))
        Imageur3D.setMaximumSize(QSize(1080, 720))
        self.centralwidget = QWidget(Imageur3D)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(270, 220, 75, 23))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(170, 10, 151, 20))
        Imageur3D.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Imageur3D)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1080, 31))
        Imageur3D.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Imageur3D)
        self.statusbar.setObjectName(u"statusbar")
        Imageur3D.setStatusBar(self.statusbar)

        self.retranslateUi(Imageur3D)

        QMetaObject.connectSlotsByName(Imageur3D)
    # setupUi

    def retranslateUi(self, Imageur3D):
        Imageur3D.setWindowTitle(QCoreApplication.translate("Imageur3D", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("Imageur3D", u"PushButton", None))
        self.label.setText(QCoreApplication.translate("Imageur3D", u"Imageur 3D", None))
    # retranslateUi

