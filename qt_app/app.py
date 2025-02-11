import sys
from PySide6.QtWidgets  import QApplication, QMainWindow
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap

from V0 import Ui_Imageur3D  # Import the generated class

import builtins
import io
import sys


class PrintWrapper(io.StringIO):
  def __call__(self, *args, **kwargs):
    # Pass the object instance (self) as the file
    return builtins.print(*args, file=self, **kwargs)

print = PrintWrapper() # print is now the printer AND a buffer
print('this was added to buffer')  # triggers print.__call__()
print('this was also added to the buffer')
print.getvalue()

class MyApp(QMainWindow, Ui_Imageur3D):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_console)  # Call function every interval
        self.timer.start(1000) 
        self.label_2.setPixmap(QPixmap("I3.bmp"))
        self.label_2.setScaledContents(True)  # Ajuste l'image à la taille du QLabel

    def update_console(self):
        print("help")
        self.textBrowser.setText(print.getvalue())
        self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
 
    sys.exit(app.exec_())