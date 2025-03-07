from re import S
import sys
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
from PySide6 import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import traceback, sys
from scipy.interpolate import griddata
from skimage import io
from scipy.interpolate import griddata
from skimage import io
from skimage import filters
from skimage.morphology import disk
import builtins
import io
import threading
import time
from numpy import loadtxt
import numpy as np

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, basedir)
os.chdir(os.path.join(basedir, 'qt_app'))
sys.path.insert(0, os.path.join(basedir, 'qt_app'))
print(basedir, "basedir")

from test import Ui_Imageur3D 

sys.path.insert(0,  os.path.join(basedir,'qt_app/code/Pb_sens_direct'))
#sys.path.insert(0, '/Users/thomas/Desktop/pronto/qt_app/code/Pb_sens_direct')
from Objet import create_and_display_object
from franges_objet import faire_franges_objets
from franges_recepteur import faire_franges_recepteur
from Trames_binaires import faire_franges
sys.path.insert(0,  os.path.join(basedir,'qt_app/code/Pb_sens_inverse'))
from Local_cotes_franges import localisation_cotes_franges
from Coord3D_objet import genere_coord3D
sys.path.insert(0, basedir)
os.chdir(os.path.join(basedir, 'qt_app/active_files'))

class PrintWrapper(io.StringIO):
  def __call__(self, *args, **kwargs):
    return builtins.print(*args, file=self, **kwargs)

print = PrintWrapper()
print.getvalue()


import cv2

HIGH_VALUE = 10000
WIDTH = 1920
HEIGHT = 1080







try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

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


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.new_trame)  
        self.timer.start(500) 
        self.label = QLabel("Another Window")
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 1920, 1080))
        self.label.setPixmap(QPixmap("Trame5.bmp"))
        self.label.setScaledContents(True)  # Ajuste l'image à la taille du QLabel
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.currentTram = 1;

    def new_trame(self):
        ret, frame = window.capture.read()
        if ret:
            cv2.imwrite(f"capture{self.currentTram}.bmp", frame)
        self.currentTram += 1
        if self.currentTram > loadtxt('N.txt', np.int32):
            self.currentTram = 1
        
        self.label.setPixmap(QPixmap("Trame" + str(self.currentTram) + ".bmp"))
        if window.mire_emet_check.isChecked():
            NbHE = 1280  # sur horizontal
            NbVE = 800  # sur vertical
            white_image = np.ones((NbVE, NbHE, 3), np.uint8) * 255
            cv2.line(white_image, (NbHE // 2, 0), (NbHE // 2, NbVE), (0, 0, 255), 2)  
            cv2.line(white_image, (0, NbVE // 2), (NbHE, NbVE // 2), (0, 0, 255), 2) 
            cv2.imwrite("white_image.bmp", white_image)
            self.label.setPixmap(QPixmap("white_image.bmp"))
            self.label.setScaledContents(True)  # Ajuste l'image à la taille du QLabel
        
        
class tab_maneger():
    def __init__(self):
        self.numberoftabs = 0
        self.imagetabs = {}
        self.imagelabels = {}


class MyApp(QMainWindow, Ui_Imageur3D):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_console)  
        self.timer.start(10) 
        self.cam_timer = QTimer(self)
        self.cam_timer.timeout.connect(self.update_camera)  
        self.cam_timer.start(17) 
        self.simulateObjectButton.clicked.connect(self.generer_objet)
        self.frangesButton.clicked.connect(self.genrere_franges)
        self.TroisDButton.clicked.connect(self.genere_cotes_franges)
        self.autoButton.clicked.connect(self.autoButtonClicked)
        self.threadpool = QThreadPool()

        self.sim_tab = tab_maneger()
        self.scan_tab = tab_maneger()
        self.capturing = False
        self.tab_dict ={self.resultTabWidget_3:self.scan_tab,self.resultTabWidget:self.sim_tab}
        self.auto = False
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.w = AnotherWindow()
        screens = app.screens()

        if len(screens) > 1:
            screen = screens[1]
        else:
            screen = screens[0]

        qr = screen.geometry()
        self.w.move(qr.left(), qr.top())
        self.w.showFullScreen()
        self.add_image_to_tab(self.resultTabWidget_3,"CAMERA.bmp")

        self.EXPOSURE = -30
        self.SATURATION = 100
    def progress_fn(self, n):
        self.progressBar.setValue(n)
        print("%d%% done" % n)

    def print_output(self, s):
        print(s)

    def startcapture(self):
        if not self.capturing:
            self.capture = cv2.VideoCapture(0)
            self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
            self.capture.set(cv2.CAP_PROP_FPS, 60);
            self.capture.set(cv2.CAP_PROP_EXPOSURE, self.EXPOSURE)  # Adjust exposure value as needed
            self.capture.set(cv2.CAP_PROP_SATURATION, self.SATURATION)  # Adjust saturation value as needed
            width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = self.capture.get(cv2.CAP_PROP_FPS)
            print(width, height, fps)
            self.capturing = True

    def endcapture(self):
        if self.capturing:
            self.capture.release()
            self.capturing = False



    def add_image_to_tab(self,tab,image_path):
        self.tab_dict[tab].numberoftabs += 1
        numerotab = self.tab_dict[tab].numberoftabs
        self.tab_dict[tab].imagetabs[numerotab]= QWidget()
        self.tab_dict[tab].imagetabs[numerotab].setObjectName(u"tab_4")
        tab.addTab(self.tab_dict[tab].imagetabs[numerotab], "")
        self.resultTabWidget.setTabText(numerotab, QCoreApplication.translate("Imageur3D", image_path, None))
        self.tab_dict[tab].imagelabels[numerotab] = QLabel(self.tab_dict[tab].imagetabs[numerotab])
        self.tab_dict[tab].imagelabels[numerotab].setObjectName(image_path)
        self.tab_dict[tab].imagelabels[numerotab].setGeometry(QRect(0, 0, 1280, 720))
        self.tab_dict[tab].imagelabels[numerotab].setPixmap(QPixmap(image_path))
        self.tab_dict[tab].imagelabels[numerotab].setScaledContents(True)  # Ajuste l'image à la taille du QLabel
        tab.setCurrentIndex(numerotab)
    
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

    def update_camera(self):
        #print("update_camera",self.capturing,self.capture)
        if self.resultTabWidget_3.currentIndex() == 1 and self.tabWidget.currentIndex() == 0:
            self.startcapture()
            ret, frame = self.capture.read()
            if ret:
                self.tab_dict[self.resultTabWidget_3].imagelabels[1].setPixmap(QPixmap.fromImage(QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888).rgbSwapped()))
                if self.mire_recep_check.isChecked():            
                    center_x, center_y = frame.shape[1] // 2, frame.shape[0] // 2
                    cv2.line(frame, (center_x, 0), (center_x, frame.shape[0]), (0, 255, 0), 2) 
                    cv2.line(frame, (0, center_y), (frame.shape[1], center_y), (0, 255, 0), 2) 
                    self.tab_dict[self.resultTabWidget_3].imagelabels[1].setPixmap(QPixmap.fromImage(QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888).rgbSwapped()))
                    #cv2.imshow('frame', frame)
        else :
            self.endcapture()

           
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
    sys.path.insert(0, basedir)
    os.chdir(os.path.join(basedir, 'qt_app/images'))
    app.setWindowIcon(QIcon('icon.png'))
    sys.path.insert(0, basedir)
    os.chdir(os.path.join(basedir, 'qt_app/active_files'))
    window = MyApp()
    window.showFullScreen()
 
    sys.exit(app.exec())
    window.endcapture()
    cv2.destroyAllWindows() 