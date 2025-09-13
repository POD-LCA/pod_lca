
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from shapely.affinity import scale
from shapely.geometry import box

from ...units import METER


class Floor:
    """ A floor of a building.
    
    Attributes
    ----------
    floor_no : int
        Floor number.
    height : float
        Floor height.   
    floor_plan : list of tuples of float
        A polygon defining the floor plan geometry [(x1, y1, z), (x2, y2, z), ... , (xn, yn, z)].    
    geometry_unit : ~pod_lca.units.Unit
        Unit of measurement
    is_below_grade : bool
        True, if the floor is above grade.
    is_on_ground : bool
        True, if the floor is on the ground.
    """

    def __init__(self):
        self.floor_no = None
        self.height = None
        self.floor_plan = None
        self.geometry_unit = METER
        self.is_below_grade = False
        self.is_on_ground = False
        self.envelope = None
        self.is_last = False

    # ================================
    # Constructors
    # ================================
    @classmethod
    def from_floor_plan(cls, floor_no, floor_plan, floor_height, geometry_unit):
        """ Create a floor from the floor plan.
        
        Parameters
        ----------        
        floor_no : int
            Floor number. 
        floor_plan : shapely.Polygon
            Floor plan.   
        height : float
            Floor height.   
        geometry_unit : ~pod_lca.units.Unit
            Unit of measurement        
        """
        floor = cls()

        floor.set_floor_no(floor_no)
        floor.set_geometry_unit(geometry_unit)
        floor.set_floor_plan(floor_plan)
        floor.set_height(floor_height)
        
        return floor

    @classmethod
    def from_rectangular_floor(cls, floor_no, length, width, floor_height, geometry_unit):
        """ Create a floor with a rectangular floor plan.
        
        Parameters
        ----------        
        floor_no : int
            Floor number. 
        length : float
            Longer dimension of the rectangular floor plan.
        width : float
            Shorter dimension of the rectangular floor plan.  
        height : float
            Floor height.   
        geometry_unit : ~pod_lca.units.Unit
            Unit of measurement        
        """
        floor = cls()

        floor.set_floor_no(floor_no)
        floor.set_geometry_unit(geometry_unit)

        floor_plan = box(xmin=0, ymin=0, xmax=width, ymax=length)

        floor.set_floor_plan(floor_plan)
        floor.set_height(floor_height)
        
        return floor

    # ================================
    # Setters
    # ================================
    def set_floor_no(self, floor_no):
        """ Set the floor number.
        
        Parameters
        ----------
        floor_no : int
            Floor number.
        """
        self.floor_no = floor_no

        return self
    
    def set_height(self, height):
        """ Set the height of the floor.
        
        Parameters
        ----------
        height : float
            Floor height.       
        """
        self.height = height

        return self
    
    def set_floor_plan(self, floor_plan):
        """ Set the floor plan.
         
        Parameters
        ----------
        floor_plan : shapely.Polygon
            Floor plan.          
        """
        self.floor_plan = floor_plan

        return self
    
    def set_geometry_unit(self, geometry_unit):
        """ Set the unit of measeurement of geometry.
        
        Parameters
        ----------
        geometry_unit : ~pod_lca.units.Unit
            Unit of measurement           
        """ 
        old_unit = self.get_geometry_unit()

        conversion_factor = old_unit.convert_to(geometry_unit)
        if self.get_height() is not None:
            self.height *= conversion_factor
        if self.get_floor_plan() is not None:
            self.set_floor_plan(scale(self.get_floor_plan(), xfact=conversion_factor, yfact=conversion_factor, origin=(0, 0)))

        self.geometry_unit = geometry_unit
        
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
    
    # ================================
    # Getters
    # ================================
    def get_floor_no(self):
        """ Get the floor number.
        
        Returns
        -------
        int
            Floor number.
        """
        return self.floor_no
    
    def get_height(self):
        """ Get the height of the floor.
        
        Returns
        -------
        height : float
            Floor height.       
        """
        return self.height
    
    def get_floor_plan(self):
        """ Get the floor plan.
         
        Returns
        -------
        shapely.Polygon
            Floor plan.          
        """
        return self.floor_plan
    
    def get_geometry_unit(self):
        """ Get the unit of measeurement of geometry.
        
        Returns
        -------
        ~pod_lca.units.Unit
            Unit of measurement           
        """ 
        return self.geometry_unit

    def get_volume(self):
        """ Get the volume of the floor.
        
        Returns
        -------
        float
            Volume of the floor.            
        """
        return self.get_height() * self.get_floor_plan().area()
    
    # ================================
    # Add
    # ================================
    def add_envelope(self, envelope):
        self.envelope = envelope

if __name__ == '__main__':
    pass  