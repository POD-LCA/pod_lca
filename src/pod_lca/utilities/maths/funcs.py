
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "; mhtaba@uw.edu"
__version__ = "0.1.0"

from numpy import floor, log10, isfinite, atleast_1d


class MathFuncs:

    @staticmethod
    def round_to_significant(values, sig_figs=3):
        """Round a list of numbers to the given number of significant figures.
        """
        return [
            0 if val == 0 else round(val, sig_figs - int(floor(log10(abs(val))))) if isfinite(val) else val
            for val in atleast_1d(values)
        ]
    

if __name__ == '__main__':
    pass
