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
# sys.path.insert(0, 'C:/Users/aurel/OneDrive/Bureau/imageur 3D/qt_app/code/Pb_sens_direct')
sys.path.insert(0, '/Users/thomas/Desktop/pronto/qt_app/code/Pb_sens_direct')
from numpy import loadtxt
from Objet import create_and_display_object
from franges_objet import faire_franges_objets
from franges_recepteur import faire_franges_recepteur

from Trames_binaires import faire_franges


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
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done




class MyApp(QMainWindow, Ui_Imageur3D):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_console)  
        self.timer.start(1000) 
        self.pushButton_3.clicked.connect(self.genrere_franges_recepteur)
        self.threadpool = QThreadPool()
        self.numberoftabs = 0
        self.imagetabs = {}
        self.imagelabels = {}
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    def progress_fn(self, n):
        self.progressBar_2.setValue(n)
        print("%d%% done" % n)

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        self.add_image_to_tab(self.tabWidget_2,"Objet1.png")
        print("THREAD COMPLETE!")

    def add_image_to_tab(self,tab,image_path):
        self.numberoftabs += 1
        self.imagetabs[self.numberoftabs] = QWidget()
        self.imagetabs[self.numberoftabs].setObjectName(u"tab_4")

        tab.addTab(self.imagetabs[self.numberoftabs], "")
        self.tabWidget_2.setTabText(self.numberoftabs, QCoreApplication.translate("Imageur3D", image_path, None))

        self.imagelabels[self.numberoftabs] = QLabel(self.imagetabs[self.numberoftabs])
        self.imagelabels[self.numberoftabs].setObjectName(image_path)
        self.imagelabels[self.numberoftabs].setGeometry(QRect(0, 0, 621, 321))
        self.imagelabels[self.numberoftabs].setPixmap(QPixmap(image_path))
        self.imagelabels[self.numberoftabs].setScaledContents(True)  # Ajuste l'image à la taille du QLabel
        tab.setCurrentIndex(self.numberoftabs)
    def on_pushButton_clicked(self):
        # Pass the function to execute
        worker = Worker(create_and_display_object) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)
    
    def genrere_franges_objet(self):
        # Pass the function to execute
        worker = Worker(faire_franges_objets) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.frange_objet_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)
    
    def frange_objet_complete(self):
        N = loadtxt("N.txt")
        N = int(N)
        for k in range(N):
            self.add_image_to_tab(self.tabWidget_2,'I' + str(k + 1) + '.bmp')
        print("THREAD COMPLETE!")

    def genrere_franges(self):
        # Pass the function to execute
        worker = Worker(faire_franges) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.frange_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)
    
    def frange_complete(self):
        N = loadtxt("N.txt")
        N = int(N)
        for k in range(N):
            self.add_image_to_tab(self.tabWidget_2,'Trame' + str(k+1) + '.bmp')
        print("THREAD COMPLETE!")
    
    def genrere_franges_recepteur(self):
        # Pass the function to execute
        worker = Worker(faire_franges_recepteur) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.frange_recepteur_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)
    
    def frange_recepteur_complete(self):
        N = loadtxt("N.txt")
        N = int(N)
        for k in range(N):
            self.add_image_to_tab(self.tabWidget_2,'IRZoom' + str(k+1) + '.bmp'   )
        print("THREAD COMPLETE!")


    def update_console(self):
        oldvertical = self.textBrowser.verticalScrollBar().value()
        self.textBrowser.setText(print.getvalue())
        if(self.radioButton.isChecked()):
            self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum())
        else:
            self.textBrowser.verticalScrollBar().setValue(oldvertical)

if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    window = MyApp()
    window.show()
 
    sys.exit(app.exec_())