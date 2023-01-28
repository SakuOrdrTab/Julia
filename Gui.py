from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, \
QHBoxLayout, QLabel, QToolBar, QFrame
from PySide6.QtGui import QPalette, QColor, QImage, QPixmap
from PySide6.QtCore import Qt

import fractal_math

class Toolbar(QWidget):
    """Toolbar class (QWidget) for creating a toolbar on the top of GUI

    Args:
        QWidget (): 
    """    
    def __init__(self):
        super().__init__()
        # make a toolbar
        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(QLabel("X:"))
        toolbar_layout.addWidget(QWidget())
        toolbar_layout.addWidget(QLabel("Y: "))
        toolbar_layout.addWidget(QWidget()) 
        
        self.setLayout(toolbar_layout)
        return None
    
class Fractal_QLabel(QLabel):
    """Class (QLabel) for displaying the fractal picture. Picture is passed as numpy 2d-array and
    stored as a QPixmap

    Args:
        QLabel (passmap): 2d numpy array of integers
    """    

    def __init__(self, passmap):
        super().__init__()
        
        # print(passmap.shape)
        qImg = QImage(passmap, len(passmap[0]), len(passmap), len(passmap[0]),  QImage.Format_Grayscale8)
        # qImg = QImage("Fractal_05.jpg") # testpic works
        pixmap01 = QPixmap.fromImage(qImg)
        pixmap_image = QPixmap(pixmap01)
        self.setPixmap(pixmap_image)
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(False)
        # self.setMinimumSize(100,100)
        

    
class Main_window(QMainWindow):
    """Main window class for GUI (QMainWindow)

    Args:
        QMainWindow (): 
    """    

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Julia")
        
        # Set all objects in Mainwindow: toolbar, fractal image
        window_layout = QVBoxLayout() # Vertical Box layout
        
        self.toolbar = Toolbar() # toolbar, custom toolbar from class Toolbar
        window_layout.addWidget(self.toolbar)
        
        # window_layout.addWidget(QLabel("AAAAAAA")) # test stuff
        # window_layout.addWidget(QLabel("BBBBBBB"))
        # window_layout.addWidget(QLabel("CCCCCCC"))
        
        cplane = fractal_math.Complex_plane() # complex plane for math, numpy 2d array
        fractal_image = Fractal_QLabel(cplane.pass_map()) # 2d numpy array of passes
        window_layout.addWidget(fractal_image) # QLabel child class containing fractal image
        
        widget = QWidget() # add widget to contain all stuff in main window
        widget.setLayout(window_layout)
        self.setCentralWidget(widget)
        return None
    