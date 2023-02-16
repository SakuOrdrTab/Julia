# main file, ver 1.00

import Gui
from PySide6.QtWidgets import QApplication
import sys

# Initial values:
r_min = -2.0
r_max = 2.0
i_min = -2.0j
i_max = r_max-r_min*600/800 + i_min


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = Gui.Main_window(r_min, r_max, i_min, i_max)
    gui.show()
    app.exec()
    sys.exit(0)
    