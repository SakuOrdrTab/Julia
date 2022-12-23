# main file, ver 0.01

import Gui
from PySide6.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = Gui.Main_window()
    gui.show()
    app.exec_()
    
    