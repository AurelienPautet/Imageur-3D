import sys
from PySide6.QtWidgets  import QApplication, QMainWindow
from V0 import Ui_Imageur3D  # Import the generated class

class MyApp(QMainWindow, Ui_Imageur3D):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())