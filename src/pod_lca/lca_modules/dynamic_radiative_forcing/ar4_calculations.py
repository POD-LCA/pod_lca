__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu; etel5501@uw.edu"
__version__ = "0.1.0"

from . import ARXCalculation


class AR4Calculations(ARXCalculation):
    """Computation methods related to dynamic radiative forcing methods, following IPCC AR4."""

    _ipcc_annual_report = "AR4"


if __name__ == "__main__":
    pass
