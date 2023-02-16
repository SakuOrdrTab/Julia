from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, \
QHBoxLayout, QLabel, QToolBar, QFrame, QPushButton, QLineEdit
from PySide6.QtGui import QPalette, QColor, QImage, QPixmap
from PySide6.QtCore import Qt

import fractal_math
import fractal_palette

# Gui for displaying fractal
# Toolbor created and laid on top, then the fractal is in it's own widget,
# derived from QWidget
# In the init of this Fractal_QLabel, palette is set and image is made from the
# passmap (from fractalmath) using the palette that returns QColors.

class Number_input_box(QLineEdit):
    """A QLineEdit box a bit narrower for input of floats for frame
    """    
    def __init__(self):
        super().__init__()
        self.setMaximumWidth(100)

class Toolbar(QWidget):
    """Toolbar class (QWidget) for creating a toolbar on the top of GUI

    Args:
        QWidget (): 
    """    
    def __init__(self):
        super().__init__()
        # make a toolbar
        toolbar_layout = QHBoxLayout()
        
        toolbar_layout.addWidget(QLabel("R_min:"))
        self.rmin_entry = Number_input_box()
        toolbar_layout.addWidget(self.rmin_entry)
        
        toolbar_layout.addWidget(QLabel("R_max: "))
        self.rmax_entry = Number_input_box()
        toolbar_layout.addWidget(self.rmax_entry)
        
        toolbar_layout.addWidget(QLabel("I_min: "))
        self.imin_entry = Number_input_box()
        toolbar_layout.addWidget(self.imin_entry)
        
        toolbar_layout.addWidget(QLabel("I_max: "))
        self.imax_entry = Number_input_box()
        toolbar_layout.addWidget(self.imax_entry)
        
        self.calc_button = QPushButton("Calculate")
        toolbar_layout.addWidget(self.calc_button)
        
        self.infobar = QLabel()
        self.infobar.setText("Infobar")
        toolbar_layout.addWidget(self.infobar)
        
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
        self.palette = fractal_palette.Fractal_palette() # palette
        
        # print(passmap.shape)
        # old grayscale: qImg = QImage(passmap, len(passmap[0]), len(passmap), len(passmap[0]),  QImage.Format_Grayscale8)
        # qImg = QImage(passmap, len(passmap[0]), len(passmap), len(passmap[0]),  QImage.Format_ARGB32)
        # qImg = QImage("Fractal_05.jpg") # testpic works
        
        # This too did not work:
        # qImg = QImage(passmap, len(passmap[0]), len(passmap), len(passmap[0]),  QImage.Format_RGB888)
        
        qImg = QImage(len(passmap[0]), len(passmap), QImage.Format_RGB32)
        for x in range(len(passmap[0])):
            for y in range(len(passmap)):
                # print(self.palette.get_color(passmap[y, x]))
                qImg.setPixelColor(x, y, self.palette.get_color(passmap[y, x]))
        # https://stackoverflow.com/questions/14821878/cant-fill-qimage-via-setpixel-properly
        
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

    def __init__(self, rmin = -2.0, rmax = 2.0, imin = -2.0j, imax = 2.0j):
        super().__init__()
        self.setWindowTitle("Julia")
        # set complexplane values to be visualized, passed from julia.py and then 
        # passed further to complexplane constructor:
        self.min_r = rmin
        self.max_r = rmax
        self.min_i = imin
        self.max_i = (self.max_r-self.min_r)*1.0j + self.min_i
        print(self.min_r, self.max_r, self.min_i, self.max_i)
        
         # complex plane for math, numpy 2d array
        cplane = fractal_math.Complex_plane(self.min_r, self.max_r, self.min_i, self.max_i)
        
        # self.palette = fractal_palette.Fractal_palette() # palette for fractal
        
        # Set all objects in Mainwindow: toolbar, fractal image
        window_layout = QVBoxLayout() # Vertical Box layout
        
        self.toolbar = Toolbar() # toolbar, custom toolbar from class Toolbar
        window_layout.addWidget(self.toolbar)
        
        # import time
        # # time it for numpy:
        # start = time.time()
        fractal_image = Fractal_QLabel(cplane.pass_map()) # 2d numpy array of passes
        # end = time.time()
        # print("Time for numpy array iterations: ", end-start)
        # # time it for python list 2d
        # start = time.time()
        # fractal_image = Fractal_QLabel(cplane.pass_map2())
        # end = time.time()
        # print("Time for Python array iterations: ", end-start)
        
        window_layout.addWidget(fractal_image) # QLabel child class containing fractal image
        
        widget = QWidget() # add widget to contain all stuff in main window
        widget.setLayout(window_layout)
        self.setCentralWidget(widget)
        return None
    