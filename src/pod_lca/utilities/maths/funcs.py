
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "; mhtaba@uw.edu"
__version__ = "0.1.0"

from math import exp

from numpy import atleast_1d
from numpy import exp as np_exp
from numpy import floor
from numpy import isfinite
from numpy import log10
from numpy import ndarray


class MathFuncs:

    @staticmethod
    def round_to_significant(values, sig_figs=3):
        """ Round a list of numbers to the given number of significant figures.

        Parameters
        ----------
        values : list of float
            Numbers to be rounded off.
        sig_fig : int
            Number of significant digits.
        """
        return [
            0 if val == 0 else round(val, sig_figs - int(floor(log10(abs(val))))) if isfinite(val) else val
            for val in atleast_1d(values)
        ]
    
    @staticmethod
    def integrate_exp(a, b, coeff=1.0, pow_coeff=1.0):
        """ Evaluate the integral of (coeff) * e ** (pow_coeff * x), from a to b, with respect to x.
        
        Parameters
        ----------
        a : float
            Start of integral evaluation.
        b : float
            End of integral evaluation.
        coeff : float
            Coeffecient on the exponent.
        pow_coeff : float
            Power of the exponent.
        """
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return (coeff / pow_coeff) * (exp(b * pow_coeff) - exp(a * pow_coeff))
        elif isinstance(a, ndarray) or  isinstance(b, ndarray):
            return (coeff / pow_coeff) * (np_exp(b * pow_coeff) - np_exp(a * pow_coeff))


if __name__ == '__main__':
    pass
