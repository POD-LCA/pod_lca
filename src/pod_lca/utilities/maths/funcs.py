
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "; mhtaba@uw.edu"
__version__ = "0.1.0"

from math import exp
from numpy import atleast_1d
from numpy import floor
from numpy import isfinite
from numpy import log10


class MathFuncs:

    @staticmethod
    def round_to_significant(values, sig_figs=3):
        """ Round a list of numbers to the given number of significant figures.
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
        a,b : float
            Start and end of integral evaluation.
        coeff, pow_coeff : float
            Coeffecient on the exponent and its power.
        """
        return (coeff / pow_coeff) * (exp(b * pow_coeff) - exp(a * pow_coeff))


if __name__ == '__main__':
    pass
