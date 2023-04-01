from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, \
                            QPushButton, QLineEdit, QRubberBand
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QRect, QPoint, QSize
import time

import fractal_math
import fractal_palette


# GUI for displaying fractal
# Includes toolbar (top), infobar, and widget to show the fractal (bottom)
# In the init of this Fractal_QLabel, palette is set and image is made from the
# passmap (from fractalmath) using the palette that returns QColors.

# Check also:
# https://doc.qt.io/qtforpython-6.2/overviews/qtcore-threads-mandelbrot-example.html


class Number_input_box(QLineEdit):
    """A QLineEdit box a bit narrower for input of floats for frame
    """    
    def __init__(self):
        super().__init__()
        self.setMaximumWidth(100)


class Toolbar(QWidget):
    """Toolbar class (QWidget) for creating a toolbar on the top of GUI
    """    
    def __init__(self):
        """Creates the top toolbar displaying coords and calculate button
        """        
        super().__init__()
        toolbar_layout = QHBoxLayout() # horizontal box
        
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
                       
        self.setLayout(toolbar_layout)
        return None
    
        
class Fractal_QLabel(QLabel):
    """Class (QLabel) for displaying the fractal picture. Picture is passed as numpy 2d-array and
    stored as a QPixmap
    """    

    def __init__(self, passmap, toolbar, infobar):
        """Class (QLabel) for displaying the fractal

        Args:
            passmap (2d array): 2d array holding pass-values for the fractal
            toolbar (QWidget): the top toolbar is passed for reference
            infobar (QLabel): Infobar is passed for reference
        """        
        super().__init__()
        self.palette = fractal_palette.Fractal_palette() # palette
        self.toolbar = toolbar
        self.infobar = infobar
             
        self.f_width, self.f_height = len(passmap[0]), len(passmap) 
        
        self.update_fractal_picture(passmap) # draws the pic
        
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(False)
        self.setFixedSize(self.f_width, self.f_height) # to ease mouse track calculations etc
        
        self.setMouseTracking(True)
        self.rubberBand = None # For holding QRubberband, when there is a selection 
        return None
    
    def set_complex_plane_values(self, minr, maxr, mini, maxi) -> None:
        """Sets the complex plane values for reference in Fractal_QLabel, needed in mouse tracking

        Args:
            minr (float): minimum real
            maxr (float): maximum real
            mini (np.complex128): minimum imaginary
            maxi (np.complex128): maximum imaginary
        """        
        self.minr, self.maxr, self.mini, self.maxi = minr, maxr, mini, maxi
        return None
        
    def mousePressEvent(self, event) -> None:
        """Activated when mouse is pressed in Fractal_QLabel. Information of press in
        infobar. Left click sets min_r and min_i to toolbar, right click max_r and max_i

        Args:
            event (event): mouse press event
        """        
        self.origin = QPoint(event.position().x(),event.position().y())
        if self.rubberBand == None:
            self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()
        return None
    
    
    def mouseMoveEvent(self, event):
        """Mouse moving updates QRubberband, i.e. the selection in Fractal_QLabel
        """        
        if (self.rubberBand != None) and (event.position().x() <= self.f_width):
            self.rubberBand.setGeometry(QRect(self.origin, QPoint(event.position().x(), self.origin.y() + (event.position().x() - self.origin.x()) * self.f_height / self.f_width)))
        return None
    
    
    def mouseReleaseEvent(self, event):
        """Mouse release finishes the QRubberband, i.e. the selection in Fractal_QLabel
        """        
        minpoint = self.origin
        maxpoint = QPoint(event.position().x(),event.position().y())
        rmin = minpoint.x() * (self.maxr - self.minr) / self.f_width + self.minr
        self.toolbar.rmin_entry.setText(f"{rmin:.5f}")
        imin = minpoint.y() * (self.maxi - self.mini) / self.f_height + self.mini
        self.toolbar.imin_entry.setText(f"{imin:.5}")
        
        minx = self.rubberBand.x()
        miny = self.rubberBand.y()
        maxx = minx + self.rubberBand.width()-1
        maxy = miny + self.rubberBand.height()-1
        rmax = maxpoint.x() * (self.maxr - self.minr) / self.f_width + self.minr
        imax = (rmax-float(self.toolbar.rmin_entry.text()))*1.0j + complex(self.toolbar.imin_entry.text())
        self.toolbar.rmax_entry.setText(f"{rmax:.5f}")
        self.toolbar.imax_entry_txt.setText(f"{imax:.5}")
        self.infobar.setText(f"New selection from ({minx}, {miny}) -> ({maxx}, {maxy})")
        
        self.rubberBand.hide()
        self.rubberBand = None 
        return None

    def update_fractal_picture(self, passmap) -> None:
        """Recalculates the fractal and displays it according to refreshed passmap. Sets PixMap

        Args:
            passmap (2d int array): the refreshed passmap

        Returns:
            None: 
        """        
        fract_img = QImage(self.f_width, self.f_height, QImage.Format_RGB32)
        for x in range(self.f_width):
            for y in range(self.f_height):
                fract_img.setPixelColor(x, y, self.palette.get_color(passmap[y, x]))
        
        # for debugging, the palette is drawn to pic:
        for i, color in enumerate(self.palette.palette_array):
            for j in range(1, 10):
                fract_img.setPixelColor(j, i, color)          
        
        self.setPixmap(QPixmap(QPixmap.fromImage(fract_img)))
        return None

    
class Main_window(QMainWindow):
    """Main window class for GUI (QMainWindow)

    Args:
        QMainWindow (): 
    """    

    def __init__(self, rmin, rmax, imin, imax,
                 FRACTAL_WIDGET_WIDTH, FRACTAL_WIDGET_HEIGHT):
        """Creates the main window holding toolbar, infopbar, and fractal image

        Args:
            rmin (float): minimum real value
            rmax (float): maximum real value
            imin (np.complex128): minimum imaginary value
            imax (np.complex128): maximum imaginary value
            FRACTAL_WIDGET_WIDTH (int): Constant derived, fractal image width in pixels
            FRACTAL_WIDGET_HEIGHT (int): Constant derived, fractal image height in pixels
        """        
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
        # print(self.min_r, self.max_r, self.min_i, self.max_i)
        
         # complex plane for math, numpy 2d array
        self.cplane = fractal_math.Complex_plane(self.min_r, self.max_r, self.min_i, self.max_i,
                                            self.frac_width, self.frac_height)
        
        # Set all objects in Mainwindow: toolbar,infobar, fractal image
        window_layout = QVBoxLayout() # Vertical Box layout
        
        self.toolbar = Toolbar() # toolbar, custom toolbar from class Toolbar
        window_layout.addWidget(self.toolbar)
        self.toolbar.calc_button.clicked.connect(self.calc_button_clicked)
        
        self.infobar = QLabel()
        self.infobar.setText("press left button to update rimn & imin, right to set rmax. "+\
            'imax is set automatically. push "calculate" to draw fractal.')
        window_layout.addWidget(self.infobar)
        
        # set texts for toolbar plane frame
        self.toolbar.imax_entry_txt.setText(str(self.max_i.imag) + "j")
        self.toolbar.imin_entry.setText(str(self.min_i.imag) + "j")
        self.toolbar.rmax_entry.setText(str(self.max_r.real))
        self.toolbar.rmin_entry.setText(str(self.min_r.real))
        
        self.fractal_image = Fractal_QLabel(self.cplane.pass_map(), self.toolbar, self.infobar) # 2d numpy array of passes
        self.fractal_image.set_complex_plane_values(self.min_r, self.max_r, self.min_i, self.max_i)
        
        window_layout.addWidget(self.fractal_image)
        
        widget = QWidget() # add widget to contain all stuff in main window
        widget.setLayout(window_layout)
        self.setCentralWidget(widget)
        return None
    
    def calc_button_clicked(self) -> None:
        """Activates when calculate button is pressed. Draws a new fractal image
        """        
        self.infobar.setText("Starting fractal calculation") # for some reason, does not work
        # copy toolbar values to self.mins and self.maxs
        self.min_r = float(self.toolbar.rmin_entry.text())
        self.max_r = float(self.toolbar.rmax_entry.text())
        self.min_i = complex(self.toolbar.imin_entry.text())
        self.max_i = complex(self.toolbar.imax_entry_txt.text()) # imax = qlabel
        
        start = time.time() # start timing
        self.cplane = fractal_math.Complex_plane(self.min_r, self.max_r, self.min_i, self.max_i,
                                            self.frac_width, self.frac_height)
        self.fractal_image.update_fractal_picture(self.cplane.pass_map())
        end = time.time() # finish timing
        self.infobar.setText(f"Fractal complete, time: {(end-start):.2f}s.")
        
        # refresh frame values to Fractal_QLabel, too
        self.fractal_image.set_complex_plane_values(self.min_r, self.max_r, self.min_i, self.max_i)
        return None