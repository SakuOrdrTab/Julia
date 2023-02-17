# main file, ver 1.1
# 1.1 added gui features etc

import Gui
from PySide6.QtWidgets import QApplication
import sys

#constants for fractal widget dimensions:
FRACTAL_WIDGET_WIDTH = 800
FRACTAL_WIDGET_HEIGHT = 600

# Initial values:
r_min = -3.0 # -2.0
r_max = 3.0 # 2.0
i_min = -3.0j # -2.0j
i_max = (r_max-r_min)*1.0j + i_min # -> 2.0j
# check the Julia set with c = 0.285+0.01i.

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = Gui.Main_window(r_min, r_max, i_min, i_max, FRACTAL_WIDGET_WIDTH, FRACTAL_WIDGET_HEIGHT)
    gui.show()
    app.exec()
    sys.exit(0)
    