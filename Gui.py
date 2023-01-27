from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, \
QHBoxLayout, QLabel, QToolBar, QFrame
from PySide6.QtGui import QPalette, QColor, QImage, QPixmap
from PySide6.QtCore import Qt

import fractal_math
    

class Toolbar(QWidget):
    
    def __init__(self):
        super().__init__()
        # make a toolbar
        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(QLabel("X:"))
        toolbar_layout.addWidget(QWidget())
        toolbar_layout.addWidget(QLabel("Y: "))
        toolbar_layout.addWidget(QWidget()) 
        # frame = QFrame()
        # frame.panel()
        # frame.setLineWidth(2)
        # toolbar_layout.addWidget(frame)
        self.setLayout(toolbar_layout)
        return None
    
class Fractal_pic(QLabel):
# qImg = QtGui.QImage(normal.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)(
    def __init__(self, passmap):
        super().__init__()
        # self.image = QImage(passmap, len(passmap), len(passmap[0]), 64, QImage.Format_RGB888)
        
        qImg = QImage(passmap, len(passmap), len(passmap[0]), 64, QImage.Format_RGB888)
        pixmap01 = QPixmap.fromImage(qImg)
        pixmap_image = QPixmap(pixmap01)
        self.setPixmap(pixmap_image)
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(True)
        self.setMinimumSize(100,100)
        self.show()
        

    
class Main_window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Julia")
        # Set all objects in Mainwindow: toolbar, teststuff
        window_layout = QVBoxLayout() # Vertical Box layout
        self.toolbar = Toolbar() # toolbar, custom toolbar from class Toolbar
        window_layout.addWidget(self.toolbar)
        window_layout.addWidget(QLabel("AAAAAAA")) # test stuff
        window_layout.addWidget(QLabel("BBBBBBB"))
        window_layout.addWidget(QLabel("CCCCCCC"))
        
        cplane = fractal_math.Complex_plane()
        fractal_image = Fractal_pic(cplane.pass_map())
        window_layout.addWidget(fractal_image)
        
        widget = QWidget() # add widget to contain all stuff in main window
        widget.setLayout(window_layout)
        self.setCentralWidget(widget)
        return None
    