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
from numpy import savetxt


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
sys.path.insert(0,  os.path.join(basedir,'qt_app/code/Calibration'))
from Calib_emetteur import calib_emet
from Calib_recepteur import calib_recep
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
    from ctypes import windll 
    myappid = 'GR9-2.PRONTO.IMAGEUR-3D.v0'
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
        self.photo_taken = -1;

    def new_trame(self):
        N = loadtxt('N.txt', np.int32)
        if  self.photo_taken != -1 and self.photo_taken < N:
            window.startcapture()
            ret, frame = window.capture.read()
            if ret:
                cv2.imwrite(f"capture{self.currentTram}.bmp", frame)
                print(self.currentTram)
                self.photo_taken += 1

        if window.cadri_emet_check.isChecked():
            self.label.setPixmap(QPixmap("Mire_damier.bmp"))


        if window.mire_emet_check.isChecked():
            window.afficher_frange_checkbox.setChecked(False)
            NbHE = 1280  # sur horizontal
            NbVE = 800  # sur vertical
            white_image = np.ones((NbVE, NbHE, 3), np.uint8) * 255
            cv2.line(white_image, (NbHE // 2, 0), (NbHE // 2, NbVE), (0, 0, 255), 2)  
            cv2.line(white_image, (0, NbVE // 2), (NbHE, NbVE // 2), (0, 0, 255), 2) 
            cv2.imwrite("white_image.bmp", white_image)
            self.label.setPixmap(QPixmap("white_image.bmp"))
            self.label.setScaledContents(True)  # Ajuste l'image à la taille du QLabel

        if window.afficher_frange_checkbox.isChecked():
            self.currentTram += 1
            if self.currentTram > N:
                self.currentTram = 1
            self.label.setPixmap(QPixmap("Trame" + str(self.currentTram) + ".bmp"))

        
        
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
        self.frangesButton.clicked.connect(lambda: self.genrere_franges(show=True))
        self.TroisDButton.clicked.connect(self.genere_cotes_franges)
        self.autoButton.clicked.connect(self.autoButtonClicked)
        self.slider_exp.valueChanged.connect(self.slider_exp_changed)
        self.slider_sat.valueChanged.connect(self.slider_sat_changed)
        self.slider_cont.valueChanged.connect(self.slider_cont_changed)

        self.tabWidget.mousePressEvent = self.mousePressEvent
        self.generate_frange_button.clicked.connect(lambda: self.genrere_franges(show=False, N=self.number_of_franges.value()))
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
        self.add_image_to_tab(self.resultTabWidget_3,"CAMERA.jpg")
        self.add_image_to_tab(self.resultTabWidget_3,"recep_z0.jpg")
        self.add_image_to_tab(self.resultTabWidget_3,"recep_zN.jpg")
        self.add_image_to_tab(self.resultTabWidget_3,"emet_z0.jpg")
        self.add_image_to_tab(self.resultTabWidget_3,"emet_zN.jpg")


    
        self.EXPOSURE = 0
        self.SATURATION = 100
        self.CONTRAST = 100

        self.clicked_points = {1:[],2:[],3:[],4:[],5:[]} 
        self.emet_z0_reset_button.clicked.connect(lambda: (self.clicked_points[4].clear(), 
                              self.update_calibration_nb_point_label(4)))
        self.emet_zN_reset_button.clicked.connect(lambda: (self.clicked_points[5].clear(), 
                              self.update_calibration_nb_point_label(5)))
        self.recep_z0_reset_button.clicked.connect(lambda: (self.clicked_points[2].clear(), 
                              self.update_calibration_nb_point_label(2)))
        self.recep_zN_reset_button.clicked.connect(lambda: (self.clicked_points[3].clear(), 
                              self.update_calibration_nb_point_label(3)))
        self.emet_z0_controlz_button.clicked.connect(lambda: (self.clicked_points[4].pop(), 
                              self.update_calibration_nb_point_label(4)))
        self.emet_zN_controlz_button.clicked.connect(lambda: (self.clicked_points[5].pop(), 
                              self.update_calibration_nb_point_label(5)))
        self.recep_z0_controlz_button.clicked.connect(lambda: (self.clicked_points[2].pop(), 
                              self.update_calibration_nb_point_label(2)))
        self.recep_zN_controlz_button.clicked.connect(lambda: (self.clicked_points[3].pop(), 
                              self.update_calibration_nb_point_label(3)))

        self.emet_calib_nb_points = 12
        self.recep_calib_nb_points = 9


        self.emet_z0_photo_button.clicked.connect(lambda: (self.take_picture("emet_z0.jpg")) )
        self.emet_zN_photo_button.clicked.connect(lambda: (self.take_picture("emet_zN.jpg")) )
        self.recep_z0_photo_button.clicked.connect(lambda: (self.take_picture("recep_z0.jpg")) )
        self.recep_zN_photo_button.clicked.connect(lambda: (self.take_picture("recep_zN.jpg")) )


        self.save_img_button.clicked.connect(self.save_file_dialog)
        self.take_picutres_button.clicked.connect(lambda: (setattr(self.w, 'photo_taken', 0),self.afficher_frange_checkbox.setChecked(True)))
        self.coord_3D_button.clicked.connect(self.genere_objet_3D)
        self.cote_franges_button.clicked.connect(self.genere_cotes_franges)
    def take_picture(self,path):
        self.startcapture()
        ret, frame = window.capture.read()
        if ret:
            cv2.imwrite(path, frame)
        self.endcapture()

    def save_file_dialog(self):
        current_tab = self.tabWidget.currentIndex()
        if current_tab == 0:
            sb_tab = self.resultTabWidget_3.currentIndex()
            file_to_save = self.tab_dict[self.resultTabWidget_3].imagelabels[sb_tab].pixmap()
            file_name = self.resultTabWidget_3.tabText(sb_tab)
        else:
            sb_tab = self.resultTabWidget.currentIndex()
            file_to_save = self.tab_dict[self.resultTabWidget].imagelabels[sb_tab].pixmap()
            file_name = self.resultTabWidget.tabText(sb_tab)

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", file_name, "All Files (*);;Image Files (*.png *.jpg *.bmp)", options=options)
        if file_name:
            file_to_save.save(file_name)
            print("file save :", file_name)   

    def progress_fn(self, n):
        self.progressBar.setValue(n)

    def print_output(self, s):
        print(s)

    def startcapture(self):
        if not self.capturing:
            self.capture = cv2.VideoCapture(1)
            self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
            self.capture.set(cv2.CAP_PROP_FPS, 60);
            self.capture.set(cv2.CAP_PROP_EXPOSURE, self.EXPOSURE)  # Adjust exposure value as needed
            self.capture.set(cv2.CAP_PROP_SATURATION, self.SATURATION)  # Adjust saturation value as needed
            self.capture.set(cv2.CAP_PROP_CONTRAST, self.CONTRAST)  # Adjust contrast value as needed
            width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = self.capture.get(cv2.CAP_PROP_FPS)
            #print(width, height, fps)
            self.capturing = True

    def endcapture(self):
        if self.capturing:
            self.capture.release()
            self.capturing = False

    def get_photo_x_y(self):
        cursor = QCursor()
        pos = cursor.pos()
        x = pos.x()
        y = pos.y()
        x = x - self.resultTabWidget_3.x() 
        y = y - self.resultTabWidget_3.y() 
        x = int(x * 1920 / 1280)
        y = int(y * 1080 / 720)
        x = x - self.tabWidget.x() -3
        y = y - self.tabWidget.y()  -31*2 -33
        return x, y

    def mousePressEvent(self, event):
        x, y = self.get_photo_x_y()
        i = self.resultTabWidget_3.currentIndex()
        if i <= 5 and self.tabWidget.currentIndex() == 0:
            if x >= 0 and y >= 0 and x < 1920 and y < 1080:
                will_add =True 
                if i == 2 or i == 3:
                    if len(self.clicked_points[i]) >= self.recep_calib_nb_points:
                        will_add = False
                if i == 4 or i == 5:
                    if len(self.clicked_points[i]) >= self.emet_calib_nb_points:
                        will_add = False
                if will_add:
                    self.clicked_points[i].append((int(x), int(y)))
                    if i!=1:
                        self.update_calibration_nb_point_label(i)
                if len(self.clicked_points[i]) == self.recep_calib_nb_points :
                    if i == 2:
                        data = np.column_stack((self.clicked_points[i], np.zeros(len(self.clicked_points[i]))))
                        savetxt('recep_z0_points.txt', data, fmt='%d')  
                        self.calibration_recepteur()
                    elif i == 3:
                        data = np.column_stack((self.clicked_points[i], np.full(len(self.clicked_points[i]), int(self.z_recep_spinbox.value()))))
                        savetxt('recep_zN_points.txt', data, fmt='%d')
                        self.calibration_recepteur()

                if len(self.clicked_points[i]) == self.emet_calib_nb_points :  
                    if i == 4:
                        data = np.column_stack((self.clicked_points[i], np.zeros(len(self.clicked_points[i]))))
                        savetxt('emet_z0_points.txt', data, fmt='%d')
                        self.calibration_emeteur()

                    elif i == 5:
                        data = np.column_stack((self.clicked_points[i], np.full(len(self.clicked_points[i]), int(self.z_emet_spinbox.value()))))
                        savetxt('emet_zN_points.txt', data, fmt='%d')
                        self.calibration_emeteur()
                print("clicked", x, y)

     
    def update_calibration_nb_point_label(self,i):
        if i == 4:
            label = self.emet_z0_nb_point_label
        elif i == 5:
            label = self.emet_zN_nb_point_label
        elif i == 2:
            label = self.recep_z0_nb_point_label
        elif i == 3:
            label = self.recep_zN_nb_point_label
        if i == 2 or i == 3:
            label.setText(str(len(self.clicked_points[i])) + "/" + str(self.recep_calib_nb_points)+" points")
        else:
            label.setText(str(len(self.clicked_points[i])) + "/" + str(self.emet_calib_nb_points)+" points")
    def update_camera(self):
        x,y = self.get_photo_x_y()
        i = self.resultTabWidget_3.currentIndex()
        if i == 1 and self.tabWidget.currentIndex() == 0:
            self.startcapture() 
            ret, frame = self.capture.read()
            if ret:
                if self.mire_recep_check.isChecked():            
                    center_x, center_y = frame.shape[1] // 2, frame.shape[0] // 2
                    cv2.line(frame, (center_x, 0), (center_x, frame.shape[0]), (0, 255, 0), 2) 
                    cv2.line(frame, (0, center_y), (frame.shape[1], center_y), (0, 255, 0), 2) 
                    #cv2.imshow('frame', frame)
            self.tab_dict[self.resultTabWidget_3].imagelabels[1].setPixmap(QPixmap.fromImage(QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888).rgbSwapped()))
        else:
            self.endcapture()

        if i <= 5 and self.tabWidget.currentIndex() == 0:
            if i==1:
                frame_bis = frame
            else:
                frame_bis = cv2.imread(self.resultTabWidget_3.tabText(i))

            for point in self.clicked_points[i]:
                    cv2.circle(frame_bis,point, 5, (0, 0, 255), -1)
            
            self.tab_dict[self.resultTabWidget_3].imagelabels[i].setPixmap(QPixmap.fromImage(QImage(frame_bis.data, frame_bis.shape[1], frame_bis.shape[0], frame_bis.strides[0], QImage.Format_RGB888).rgbSwapped()))

            if x >= 0 and y >= 0 and x < 1920 and y < 1080:
                frame = frame_bis
                zoom = frame[max(0, y-25):min(frame.shape[0], y+25), max(0, x-25):min(frame.shape[1], x+25)]
                if zoom.shape[0] < 50 or zoom.shape[1] < 50:
                    zoom = cv2.copyMakeBorder(zoom, 
                                                top=max(0, 25 - y), 
                                                bottom=max(0, y + 25 - frame.shape[0]), 
                                                left=max(0, 25 - x), 
                                                right=max(0, x + 25 - frame.shape[1]), 
                                                borderType=cv2.BORDER_CONSTANT, 
                                                value=[0, 0, 0])
                cross_size = 5
                cross_color = (250, 250, 250)  # Green color
                center_x, center_y = 25, 25  # Center of the zoomed area
                cv2.line(zoom, (center_x - cross_size, center_y), (center_x + cross_size, center_y), cross_color, 1)
                cv2.line(zoom, (center_x, center_y - cross_size), (center_x, center_y + cross_size), cross_color, 1)
                zoom = cv2.resize(zoom, (250, 250), interpolation=cv2.INTER_NEAREST)

                zoom_qimage = QImage(zoom.data, zoom.shape[1], zoom.shape[0], zoom.strides[0], QImage.Format_RGB888).rgbSwapped()
                self.label_zoom.setPixmap(QPixmap.fromImage(zoom_qimage))
                self.label_zoom.setScaledContents(True)
                    

        else :
            self.endcapture()

           
    def update_console(self):
        oldvertical = self.consoleLayout.verticalScrollBar().value()
        self.consoleLayout.setText(print.getvalue())
        if(self.autoScrollButton.isChecked()):
            self.consoleLayout.verticalScrollBar().setValue(self.consoleLayout.verticalScrollBar().maximum())
        else:
            self.consoleLayout.verticalScrollBar().setValue(oldvertical)


    def slider_exp_changed(self):
        self.EXPOSURE = self.slider_exp.value()
        self.label_val_exp.setText(str(self.EXPOSURE))
        if self.capturing:
            self.capture.set(cv2.CAP_PROP_EXPOSURE, self.EXPOSURE)
    
    def slider_sat_changed(self):
        self.SATURATION = self.slider_sat.value()
        self.label_val_sat.setText(str(self.SATURATION))
        if self.capturing:
            self.capture.set(cv2.CAP_PROP_SATURATION, self.SATURATION)
    
    def slider_cont_changed(self):
        self.CONTRAST = self.slider_cont.value()
        self.label_val_cont.setText(str(self.CONTRAST))
        if self.capturing:
            self.capture.set(cv2.CAP_PROP_CONTRAST, self.CONTRAST)

    def add_image_to_tab(self,tab,image_path):
        self.tab_dict[tab].numberoftabs += 1
        numerotab = self.tab_dict[tab].numberoftabs
        self.tab_dict[tab].imagetabs[numerotab]= QWidget()
        self.tab_dict[tab].imagetabs[numerotab].setObjectName(u"tab_4")
        tab.addTab(self.tab_dict[tab].imagetabs[numerotab], "")
        tab.setTabText(numerotab, QCoreApplication.translate("Imageur3D", image_path, None))
        self.tab_dict[tab].imagelabels[numerotab] = QLabel(self.tab_dict[tab].imagetabs[numerotab])
        self.tab_dict[tab].imagelabels[numerotab].setObjectName(image_path)
        self.tab_dict[tab].imagelabels[numerotab].setGeometry(QRect(0, 0, 1280, 720))
        self.tab_dict[tab].imagelabels[numerotab].setPixmap(QPixmap(image_path))
        self.tab_dict[tab].imagelabels[numerotab].setScaledContents(True)  # Ajuste l'image à la taille du QLabel
        tab.setCurrentIndex(numerotab)
    
    def autoButtonClicked(self):
        self.auto = True
        self.generer_objet()

    
    
    def calibration_recepteur(self):
        print("debut d'éxecution de calibration_recepteur")
        # Pass the function to execute
        worker = Worker(calib_recep) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.calibration_recepteur_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)

    def calibration_recepteur_complete(self):
        print("fin d'exécution de calibration_recepteur")   
    
    def calibration_emeteur(self):
        print("debut d'éxecution de calibration_emeteur")
        # Pass the function to execute
        worker = Worker(calib_emet) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.calibration_emeteur_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)

    def calibration_emeteur_complete(self):
        print("fin d'exécution de calibration_emeteur")   


    def generer_objet(self):
        print("debut d'éxecution de generer_objet")
        # Pass the function to execute
        worker = Worker(create_and_display_object) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)

    def thread_complete(self):
        print("fin d'exécution de generer_objet")   
        self.add_image_to_tab(self.resultTabWidget,"Objet1.png")
        print("THREAD COMPLETE!")
        if(self.auto):
            self.genrere_franges()
    
    def genrere_franges_objet(self):
        print("debut d'éxecution de genrere_franges_objet")
        worker = Worker(faire_franges_objets) 
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.frange_objet_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)
    
    def frange_objet_complete(self):
        print("fin d'exécution de genrere_franges_objet")
        N = loadtxt("N.txt")
        N = int(N)
        for k in range(N):
            self.add_image_to_tab(self.resultTabWidget,'I' + str(k + 1) + '.bmp')
        self.genrere_franges_recepteur()

    def genrere_franges(self,show = True,N=5):
        print("debut d'éxecution de genrere_franges")
        worker = Worker(faire_franges,bruit = (self.checkBox.isChecked() and show),halo = (self.checkBox_2.isChecked()and show),N=N)
        worker.signals.result.connect(self.print_output)
        print("show",show)
        if show:
            worker.signals.finished.connect(self.frange_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)
    
    def frange_complete(self):
        print("fin d'exécution de genrere_franges")
        N = loadtxt("N.txt")
        N = int(N)
        for k in range(N):
            self.add_image_to_tab(self.resultTabWidget,'Trame' + str(k+1) + '.bmp')
        self.genrere_franges_objet()
    
    def genrere_franges_recepteur(self):
        print("debut d'éxecution de genrere_franges_recepteur")
        worker = Worker(faire_franges_recepteur) 
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.frange_recepteur_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)
    
    def frange_recepteur_complete(self):
        print("fin d'éxecution de genrere_franges_recepteur")
        N = loadtxt("N.txt")
        N = int(N)
        for k in range(N):
            self.add_image_to_tab(self.resultTabWidget,'IRZoom' + str(k+1) + '.bmp'   )
        if self.auto:
            self.genere_cotes_franges()

    def genere_objet_3D(self):
        print("debut d'éxecution de genere_objet_3D")
        worker = Worker(genere_coord3D) 
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.genere_objet_3D_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)
        
    def genere_objet_3D_complete(self):
        if self.tabWidget.currentIndex() == 0:
            exp = "scan"
        else:
            exp = "simu"
        print("fin d'éxecution de genere_objet_3D")
        if exp == "scan":
            self.add_image_to_tab(self.resultTabWidget_3,"Nuances.png")
        else:
            self.add_image_to_tab(self.resultTabWidget,"Nuances.png")
        self.fig = Figure(figsize=(5, 3))
        static_canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111, projection='3d')
        if exp == "scan":
            tab = self.resultTabWidget_3
        else:
            tab = self.resultTabWidget

        self.tab_dict[tab].numberoftabs += 1
        numerotab = self.tab_dict[tab].numberoftabs

        self.tab_dict[tab].imagetabs[numerotab]= static_canvas
        tab.addTab(static_canvas, "")
        tab.setTabText(numerotab, QCoreApplication.translate("Imageur3D", "3D OBJECT PLOT", None))

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
        print("debut d'éxecution de genere_cotes_franges")
        if self.tabWidget.currentIndex() == 0:
            exp = "scan"
            threshold = self.seuil_spinbox.value()
        else:
            exp = "simu"
            threshold = 240
        print("exp",exp)

        worker = Worker(localisation_cotes_franges,exp = exp,threshold = threshold) 
        worker.signals.finished.connect(self.genere_cotes_franges_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)

    def helps(self):
        print("help")
    def genere_cotes_franges_complete(self):
        if self.tabWidget.currentIndex() == 0:
            exp = "scan"
        else:
            exp = "simu"
        print("fin d'éxecution de genere_cotes_franges")
        N = loadtxt("N.txt")
        N = int(N)
        for k in range(N):
            if exp == "scan":
                self.add_image_to_tab(self.resultTabWidget_3,f'processed_IRZoom_bis_bis{str(k + 1)}.bmp')
            else:
                self.add_image_to_tab(self.resultTabWidget,f'processed_IRZoom_bis_bis{str(k + 1)}.bmp')
        if exp == "scan":
            self.add_image_to_tab(self.resultTabWidget_3,"Cotes_franges.bmp")
        else:
            self.add_image_to_tab(self.resultTabWidget,"Cotes_franges.bmp")
            self.genere_objet_3D()


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