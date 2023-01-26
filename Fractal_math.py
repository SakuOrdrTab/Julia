import numpy as np

def iters_passed(c: np.complex128) -> int:
    # f = c * c + z ;mandelbrot
    z = np.complex128(0 + 0j)
    if c == (0 + 0j):
        return 0
    else:
        current = c
        for i in range(0, 256):
            if abs(current) <= 4:
                current = current**2 + z
            else:
                return i
        return 255

class Complex_plane():
    
    def __init__(self):
        self.complex_array = np.linspace(-2j, 2j, num = 800) .reshape(-1, 1) + np.linspace(-2, 2, num = 600)
        
    def plane(self):
        return self.complex_array
    
    def value(self, r, i):
        try:
            return self.complex_array[r, i]
        except Exception:
            return None
        
    def value_real(self, r, i):
        try:
            return np.real(self.complex_array[r, i])
        except Exception:
            return None
        
    def value_imag(self, r, i):
        try:
            return np.imag(self.complex_array[r, i])
        except Exception:
            return None
    
    def pass_map(self):
        result = []
        for cplane_line in self.complex_array:
            newline = []
            for cnumber in cplane_line:
                newline.append(iters_passed(cnumber))
            result.append(newline)
        return result 





# def z(n, c):
# ...     if n == 0:
# ...         return 0
# ...     else:
# ...         return z(n - 1, c) ** 2 + c
