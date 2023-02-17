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
        
        # max imag number not enterable, calculated from other three
        toolbar_layout.addWidget(QLabel("I_max: "))
        # self.imax_entry = Number_input_box()
        # toolbar_layout.addWidget(self.imax_entry)
        self.imax_entry_txt = QLabel()
        toolbar_layout.addWidget(self.imax_entry_txt)
        self.imax_entry_txt.setText("None yet")
        
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

    def __init__(self, passmap, toolbar):
        super().__init__()
        self.palette = fractal_palette.Fractal_palette() # palette
        self.toolbar = toolbar
        
        # print(passmap.shape)
        # old grayscale: qImg = QImage(passmap, len(passmap[0]), len(passmap), len(passmap[0]),  QImage.Format_Grayscale8)
        # qImg = QImage(passmap, len(passmap[0]), len(passmap), len(passmap[0]),  QImage.Format_ARGB32)
        # qImg = QImage("Fractal_05.jpg") # testpic works
        
        # This too did not work:
        # qImg = QImage(passmap, len(passmap[0]), len(passmap), len(passmap[0]),  QImage.Format_RGB888)
        
        self.f_width, self.f_height = len(passmap[0]), len(passmap)
        
        qImg = QImage(self.f_width, self.f_height, QImage.Format_RGB32)
        for x in range(self.f_width):
            for y in range(self.f_height):
                # print(self.palette.get_color(passmap[y, x]))
                qImg.setPixelColor(x, y, self.palette.get_color(passmap[y, x]))
        # https://stackoverflow.com/questions/14821878/cant-fill-qimage-via-setpixel-properly
        
        pixmap01 = QPixmap.fromImage(qImg)
        pixmap_image = QPixmap(pixmap01)
        
        
        self.setPixmap(pixmap_image)
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(False)
        self.setFixedSize(self.f_width, self.f_height) # to ease mouse track calculations etc
        
        self.setMouseTracking(True)
        return None
    
    def set_complex_plane_values(self, minr, maxr, mini, maxi):
        self.minr, self.maxr, self.mini, self.maxi = minr, maxr, mini, maxi
        return None
        
    def mousePressEvent(self, e):
        point = e.pos()
        mouse_r_pos = point.x() * (self.maxr - self.minr) / self.f_width + self.minr
        mouse_i_pos = point.y() * (self.maxi - self.mini) / self.f_height + self.mini
        self.toolbar.infobar.setText(f"mouse pressed at {mouse_r_pos:.5}, {mouse_i_pos:.5}")    
        return None
    
    def update_fractal_picture(self, passmap):
        qImg = QImage(self.f_width, self.f_height, QImage.Format_RGB32)
        for x in range(self.f_width):
            for y in range(self.f_height):
                # print(self.palette.get_color(passmap[y, x]))
                qImg.setPixelColor(x, y, self.palette.get_color(passmap[y, x]))
        # https://stackoverflow.com/questions/14821878/cant-fill-qimage-via-setpixel-properly
        
        pixmap01 = QPixmap.fromImage(qImg)
        pixmap_image = QPixmap(pixmap01)
        self.setPixmap(pixmap_image)
        return None

    
class Main_window(QMainWindow):
    """Main window class for GUI (QMainWindow)

    Args:
        QMainWindow (): 
    """    

    def __init__(self, rmin, rmax, imin, imax,
                 FRACTAL_WIDGET_WIDTH, FRACTAL_WIDGET_HEIGHT):
        super().__init__()
        self.setWindowTitle("Julia")
        # set complexplane values to be visualized, passed from julia.py and then 
        # passed further to complexplane constructor:
        self.min_r = rmin
        self.max_r = rmax
        self.min_i = imin
        self.max_i = (self.max_r-self.min_r)*1.0j + self.min_i
        self.frac_width = FRACTAL_WIDGET_WIDTH
        self.frac_height = FRACTAL_WIDGET_HEIGHT
        print(self.min_r, self.max_r, self.min_i, self.max_i)
        
         # complex plane for math, numpy 2d array
        cplane = fractal_math.Complex_plane(self.min_r, self.max_r, self.min_i, self.max_i,
                                            self.frac_width, self.frac_height)
        
        # self.palette = fractal_palette.Fractal_palette() # palette for fractal
        
        # Set all objects in Mainwindow: toolbar, fractal image
        window_layout = QVBoxLayout() # Vertical Box layout
        
        self.toolbar = Toolbar() # toolbar, custom toolbar from class Toolbar
        window_layout.addWidget(self.toolbar)
        self.toolbar.calc_button.clicked.connect(self.calc_button_clicked)
        
        # set texts for toolbar plane frame
        self.toolbar.imax_entry_txt.setText(str(self.max_i.imag) + "j")
        self.toolbar.imin_entry.setText(str(self.min_i.imag) + "j")
        self.toolbar.rmax_entry.setText(str(self.max_r.real))
        self.toolbar.rmin_entry.setText(str(self.min_r.real))
        
        # import time
        # # time it for numpy:
        # start = time.time()
        self.fractal_image = Fractal_QLabel(cplane.pass_map(), self.toolbar) # 2d numpy array of passes
        self.fractal_image.set_complex_plane_values(self.min_r, self.max_r, self.min_i, self.max_i)
        # end = time.time()
        # print("Time for numpy array iterations: ", end-start)
        # # time it for python list 2d
        # start = time.time()
        # fractal_image = Fractal_QLabel(cplane.pass_map2())
        # end = time.time()
        # print("Time for Python array iterations: ", end-start)
        
        window_layout.addWidget(self.fractal_image) # QLabel child class containing fractal image
        
        widget = QWidget() # add widget to contain all stuff in main window
        widget.setLayout(window_layout)
        self.setCentralWidget(widget)
        return None
    
    def calc_button_clicked(self):
        # print("calc_button was clicked!")
        self.toolbar.infobar.setText("Starting fractal calculation")
        cplane = fractal_math.Complex_plane(self.min_r, self.max_r, self.min_i, self.max_i,
                                            self.frac_width, self.frac_height)
        self.fractal_image.update_fractal_picture(cplane.pass_map())
        self.toolbar.infobar.setText("Fractal calculation complete")
        return None