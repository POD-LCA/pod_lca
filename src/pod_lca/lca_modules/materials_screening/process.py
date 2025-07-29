
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import Master


class Process(Master):
    """ Process object, inheriting from the Master object, represent a process.

    Attributes
    ----------
    inputs : list of Master Obj.
        Input products and processes.
    """

    def __init__(self):
        super().__init__()
        self.inputs = []

    def __str__(self):
        return f"Process(name={self.get_name()}, LC stage={self.get_life_cycle_stage()}, qty={self.get_qty()} {self.get_unit().get_standard_notation()})"


if __name__ == '__main__':
    pass
