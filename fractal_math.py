import numpy as np


def iters_passed(c: np.complex128) -> int:
    """Returns number of iterations passed (= belongs to the Julia set). Currently func = c * c + Z,
    where c is the complex number argument and Z is the constant (0.25 + 0j)

    Args:
        c (np.complex128): Complex parameter for fractal function

    Returns:
        int: number of passes before iters > 255
    """    
    # f = c * c + z ; mandelbrot
    z = np.complex128(0.25 + 0.00j)
    if c == (0 + 0j):
        return 0
    else:
        current = c
        for i in range(0, 256):
            if abs(current) <= 2:
                current = current**2 + z
            else:
                return i
        return 255


class Complex_plane():
    """Class for holding the complex plane to plot fractal from.
    """    
    def __init__(self, minr, maxr, mini, maxi, FRACTAL_WIDGET_WIDTH, FRACTAL_WIDGET_HEIGHT):
        """Constructs Complex plane according to arguments

        Args:
            minr (float): minimum real value for plane
            maxr (float): maximum real value
            mini (np.complex128): minimum imaginary value for plane
            maxi (np.complex128): maximum imaginary value   
            FRACTAL_WIDGET_WIDTH (int): width of the fractal widget, constant
            FRACTAL_WIDGET_HEIGHT (int): height of the fractal widget, constant
        """        
        self.complex_array = np.linspace(mini, maxi, num = FRACTAL_WIDGET_HEIGHT) .reshape(-1, 1) + np.linspace(minr, maxr, num = FRACTAL_WIDGET_WIDTH)
        
    def plane(self):
        """returns the complex array (2d numpy float) the object is holding

        Returns:
            2d numpy array complex128: the plane
        """        
        return self.complex_array
    
    def value(self, r, i):
        """returns the complex number at certain place in array (not correlating to spatial place)

        Args:
            r (int): first dimension
            i (int): second dimension

        Returns:
            numpy.complex128: the complex number in this array slot, None if fail
        """        
        try:
            return self.complex_array[r, i]
        except Exception:
            return None
        
    def value_real(self, r, i):
        """returns the real part of the complex number at certain place in array
        (not correlating to spatial place)

        Args:
            r (int): first dimension
            i (int): second dimension

        Returns:
            float: real part of the complex number in this array slot, None if fail
        """        
        try:
            return np.real(self.complex_array[r, i])
        except Exception:
            return None
        
    def value_imag(self, r, i):
        """returns the imaginary part of the complex number as float at certain place in array
        (not correlating to spatial place)

        Args:
            r (int): first dimension
            i (int): second dimension

        Returns:
            float: imaginary part of the complex number as float in this array slot, None if fail
        """   
        try:
            return np.imag(self.complex_array[r, i])
        except Exception:
            return None
    
    def pass_map(self):
        """returns a 2d numpy array of passes that complex plane points iterate with the fractal function
        Now implemented in numpy.
        Returns:
            numpy 2d array of uint8: 2d numpy array of passes, 0 .. 255
        """
        result = np.empty(shape=self.complex_array.shape, dtype="uint8")
        for (y, x), complex in np.ndenumerate(self.complex_array):
            result[y, x] = iters_passed(complex)
        return result
    
    # def pass_map2(self):
    #     # old code, for testing purposes   
    #     result = []
    #     for cplane_line in self.complex_array:
    #         newline = []
    #         for cnumber in cplane_line:
    #             newline.append(iters_passed(cnumber))
    #         result.append(newline)
    #     return np.array(result, dtype="uint8")


