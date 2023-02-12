from PySide6.QtGui import QColor
# import math
# from numpy import complex128

# smoothing algorithm produces math error, trying to do a logarithm of
# negative number, I suppose. Needs research.
#
# def smooth(color, last_complex):
#         rgba = color.getRgb()
#         print(type(color))
#         result = []
#         for channel in rgba:
#             result.append(channel + 1 - math.log(math.log(abs(last_complex)))/abs(math.log2(last_complex)))
#         newcolor = QColor(*result)
#         return newcolor

class Fractal_palette():
           
    def __init__(self):
        self.palette_array = []
        for i in range(0, 64):
            color = QColor(int(i*255/64), 0, 0)
            self.palette_array.append(color)
        for i in range(0, 64):
            color = QColor(255, int(i*255/64), 0)
            self.palette_array.append(color) 
        for i in range(0, 64):
            color = QColor(255, 255, int(i*255/64))
            self.palette_array.append(color) 
        for i in range(0, 64):
            color = QColor(255-int((i*255/64)), 255, 255-int((i*255/64)))
            self.palette_array.append(color)
        print(len(self.palette_array), " colours in palette.")
        # quit()            
    def get_color(self, number: int) -> QColor:
        return self.palette_array[number]
    
# for debugging:    
if __name__ == "__main__":
    print("debug mode!")
    palette = Fractal_palette()
    print(palette.get_color(230))


    
    