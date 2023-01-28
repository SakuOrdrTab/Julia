# main file, ver 1.00

import Gui
from PySide6.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = Gui.Main_window()
    gui.show()
    app.exec()
    sys.exit(0)
    