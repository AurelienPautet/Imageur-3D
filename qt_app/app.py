import sys
from PySide6 import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from test import Ui_Imageur3D 
import traceback, sys


import builtins
import io
import os
import threading
import time

import numpy as np

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure

sys.path.insert(0, 'C:/Users/aurel/OneDrive/Bureau/imageur 3D/qt_app/code/Pb_sens_direct')
#sys.path.insert(0, '/Users/thomas/Desktop/pronto/qt_app/code/Pb_sens_direct')
from numpy import loadtxt
from Objet import create_and_display_object
from franges_objet import faire_franges_objets
from franges_recepteur import faire_franges_recepteur
from Trames_binaires import faire_franges
sys.path.insert(0, 'C:/Users/aurel/OneDrive/Bureau/imageur 3D/qt_app/code/Pb_sens_inverse')
from Local_cotes_franges import localisation_cotes_franges
from Coord3D_objet import genere_coord3D

class PrintWrapper(io.StringIO):
  def __call__(self, *args, **kwargs):
    return builtins.print(*args, file=self, **kwargs)

print = PrintWrapper()
print.getvalue()

class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs['progress_callback'] = self.signals.progress

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result) 
        finally:
            self.signals.finished.emit()  




class MyApp(QMainWindow, Ui_Imageur3D):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_console)  
        self.timer.start(1000) 
        self.simulateObjectButton.clicked.connect(self.generer_objet)
        self.frangesButton.clicked.connect(self.genrere_franges)
        self.TroisDButton.clicked.connect(self.genere_cotes_franges)
        self.autoButton.clicked.connect(self.autoButtonClicked)
        self.threadpool = QThreadPool()
        self.numberoftabs = 0
        self.imagetabs = {}
        self.imagelabels = {}
        self.auto = False
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())


    def progress_fn(self, n):
        self.progressBar_2.setValue(n)
        print("%d%% done" % n)

    def print_output(self, s):
        print(s)



    def add_image_to_tab(self,tab,image_path):
        self.numberoftabs += 1
        self.imagetabs[self.numberoftabs] = QWidget()
        self.imagetabs[self.numberoftabs].setObjectName(u"tab_4")

        tab.addTab(self.imagetabs[self.numberoftabs], "")
        self.resultTabWidget.setTabText(self.numberoftabs, QCoreApplication.translate("Imageur3D", image_path, None))

        self.imagelabels[self.numberoftabs] = QLabel(self.imagetabs[self.numberoftabs])
        self.imagelabels[self.numberoftabs].setObjectName(image_path)
        self.imagelabels[self.numberoftabs].setGeometry(QRect(0, 0, 621, 321))
        self.imagelabels[self.numberoftabs].setPixmap(QPixmap(image_path))
        self.imagelabels[self.numberoftabs].setScaledContents(True)  # Ajuste l'image à la taille du QLabel
        tab.setCurrentIndex(self.numberoftabs)
    
    def autoButtonClicked(self):
        self.auto = True
        self.generer_objet()

    def generer_objet(self):
        # Pass the function to execute
        worker = Worker(create_and_display_object) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)

    def thread_complete(self):
        self.add_image_to_tab(self.resultTabWidget,"Objet1.png")
        print("THREAD COMPLETE!")
        if(self.auto):
            self.genrere_franges()
    
    def genrere_franges_objet(self):
        worker = Worker(faire_franges_objets) 
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.frange_objet_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)
    
    def frange_objet_complete(self):
        N = loadtxt("N.txt")
        N = int(N)
        for k in range(N):
            self.add_image_to_tab(self.resultTabWidget,'I' + str(k + 1) + '.bmp')
        print("THREAD COMPLETE!")
        self.genrere_franges_recepteur()

    def genrere_franges(self):
        worker = Worker(faire_franges,bruit = self.checkBox.isChecked(),halo = self.checkBox_2.isChecked())
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.frange_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)
    
    def frange_complete(self):
        N = loadtxt("N.txt")
        N = int(N)
        for k in range(N):
            self.add_image_to_tab(self.resultTabWidget,'Trame' + str(k+1) + '.bmp')
        print("THREAD COMPLETE!")
        self.genrere_franges_objet()
    
    def genrere_franges_recepteur(self):
        worker = Worker(faire_franges_recepteur) 
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.frange_recepteur_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)
    
    def frange_recepteur_complete(self):
        N = loadtxt("N.txt")
        N = int(N)
        for k in range(N):
            self.add_image_to_tab(self.resultTabWidget,'IRZoom' + str(k+1) + '.bmp'   )
        print("THREAD COMPLETE!")
        if self.auto:
            self.genere_cotes_franges()

    def genere_objet_3D(self):
        worker = Worker(genere_coord3D) 
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.genere_objet_3D_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)
        
    def genere_objet_3D_complete(self):
        self.add_image_to_tab(self.resultTabWidget,"Nuances.png")
        self.fig = Figure(figsize=(5, 3))
        static_canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111, projection='3d')
        self.numberoftabs += 1
        self.resultTabWidget.addTab(static_canvas, "")
        self.resultTabWidget.setTabText(self.numberoftabs, QCoreApplication.translate("Imageur3D", "3D OBJECT PLOT", None))

        X = loadtxt('X_scan.txt')
        Y = loadtxt('Y_scan.txt')
        Z = loadtxt('Z_scan.txt')
        self.axes.scatter(X, Y, Z,s=0.5)
        self.axes.set_xlabel('X')
        self.axes.set_ylabel('Y')
        self.axes.set_zlabel('Z')
        self.axes.set_aspect('equal')
        self.fig.tight_layout()


    def genere_cotes_franges(self):
        print("genere_cotes_franges")
        worker = Worker(localisation_cotes_franges) 
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.genere_cotes_franges_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)


    def genere_cotes_franges_complete(self):
        self.genere_objet_3D()

    def update_console(self):
        oldvertical = self.consoleLayout.verticalScrollBar().value()
        self.consoleLayout.setText(print.getvalue())
        if(self.autoScrollButton.isChecked()):
            self.consoleLayout.verticalScrollBar().setValue(self.consoleLayout.verticalScrollBar().maximum())
        else:
            self.consoleLayout.verticalScrollBar().setValue(oldvertical)

if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    window = MyApp()
    window.show()
 
    sys.exit(app.exec_())