
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from numpy import array
from numpy import roll

from ...units import Quantity as Q


class BuildingFloor:
    """ A floor of a building.
    
    Attributes
    ----------
    height : ~pod_lca.units.Quantity
        Floor height.   
    floor_plan : list of tuples of ~pod_lca.units.Quantity
        A polygon defining the floor plan geometry [(x1, y1, z), (x2, y2, z), ... , (xn, yn, z)].    
    is_below_grade : bool
        True, if the floor is above grade.
    is_on_ground : bool
        True, if the floor is on the ground.
    envelope : ~pod_lca.building_envelope.Envelope
        Envelope of the floor.
    structure : ~pod_lca.units.Unit
        Structure of the floor.
    usage : {'Residential', 'Commercial'}
        The usage of the floor.
    """

    def __init__(self):
        self.height = None
        self.floor_plan = None
        self.usage = None
        self.is_below_grade = False
        self.is_on_ground = False
        self.is_last = False
        self.envelope = None
        self.structure = None

    # ================================
    # Constructors
    # ================================
    @classmethod
    def from_floor_plan(cls, floor_plan, floor_height, usage):
        """ Create a floor from the floor plan.
        
        Parameters
        ----------        
        floor_plan : list of tuples of float
            A polygon defining the floor plan geometry [(x1, y1, z), (x2, y2, z), ... , (xn, yn, z)].  
        height : float
            Floor height.   
        usage : {'Residential', 'Commercial'}
            The usage of the floor.     
        """
        floor = cls()

        floor.set_floor_plan(floor_plan)
        floor.set_height(floor_height)
        floor.set_usage(usage)
        
        return floor

    @classmethod
    def from_rectangular_floor(cls, length, width, floor_height):
        """ Create a floor with a rectangular floor plan.
        
        Parameters
        ----------        
        length : ~pod_lca.units.Quantity
            Longer dimension of the rectangular floor plan.
        width : ~pod_lca.units.Quantity
            Shorter dimension of the rectangular floor plan.  
        height : ~pod_lca.units.Quantity
            Floor height.         
        """
        floor = cls()

        zero = Q(0, width.unit)
        floor_plan = [(zero, zero), 
                      (width, zero), 
                      (width, length), 
                      (zero, length)]

        floor.set_floor_plan(floor_plan)
        floor.set_height(floor_height)
        
        return floor

    # ================================
    # Setters
    # ================================
    def set_height(self, height):
        """ Set the height of the floor.
        
        Parameters
        ----------
        height : ~pod_lca.units.Quantity
            Floor height.       
        """
        self.height = height

        return self
    
    def set_floor_plan(self, floor_plan):
        """ Set the floor plan.
         
        Parameters
        ----------
        floor_plan : list of tuples of ~pod_lca.units.Quantity
            A polygon defining the floor plan geometry [(x1, y1, z), (x2, y2, z), ... , (xn, yn, z)].        
        """
        self.floor_plan = floor_plan

        return self
    
    def set_floor_on_ground(self):
        """ Set the floor to be on ground.
        """
        self.is_on_ground = True

        return self
    
    def set_floor_below_grade(self):
        """ Set the floor to be below grade.
        """
        self.is_below_grade = True

        return self
    
    def set_usage(self, usage):
        """ Set the usage of the building floor.
        
        Parameters
        ----------
        usage : {'Residential', 'Commercial'}
            The usage of the floor.  
        """
        self.usage = usage

    # ================================
    # Getters
    # ================================
    def get_height(self):
        """ Get the height of the floor.
        
        Returns
        -------
        ~pod_lca.units.Quantity
            Floor height.       
        """
        return self.height
    
    def get_floor_plan(self):
        """ Get the floor plan.
         
        Returns
        -------
        list of tuples of ~pod_lca.units.Quantity
            A polygon defining the floor plan geometry [(x1, y1, z), (x2, y2, z), ... , (xn, yn, z)].           
        """
        return self.floor_plan
    
    def get_area(self):
        """ Get the floor area.
        
        Returns
        -------
        float
            Area of the floor.           
        """ 
        points = array(self.get_floor_plan())
        x = points[:, 0]
        y = points[:, 1]
        
        x_next = roll(x, -1)
        y_next = roll(y, -1)

        sum = 0
        for xi, yi, xni, yni in zip(x,y, x_next, y_next):
            sum += ((xi * yni) - (yi * xni)) * 0.5

        if sum.value < 0.0:
            sum *= -1
        
        return sum

    def get_volume(self):
        """ Get the volume of the floor.
        
        Returns
        -------
        ~pod_lca.units.Quantity
            Unit of measurement of volume.       
        """
        return self.get_height() * self.get_area()
    
    def get_usage(self):
        """ Set the usage of the building floor.
        
        Returns
        ----------
        str
            The usage of the floor.  
        """
        return self.usage

    # ================================
    # Add
    # ================================
    def set_envelope(self, envelope):
        self.envelope = envelope

    def set_structure(self, structure):
        self.structure = structure


if __name__ == '__main__':
    pass  