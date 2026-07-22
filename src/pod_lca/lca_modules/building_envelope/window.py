__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from pod_lca.units import SQUARE_METER
from pod_lca.units import Quantity as Q
from pod_lca.lca_modules.building_envelope import Surface
from pod_lca.lca_modules.building_envelope.construction import Construction
from pod_lca.utilities.geometry import centroid, distance_point_point, area_polygon
from pod_lca.utilities.geometry import scale_vector, normalize_vector, subtract_vectors, add_vectors

class Window(Construction):
    """Window object based on the ~pod_lca.building_envelope.Construction
    class. 

    Attributes
    ----------
    surfaces :  (dict of) ~pod_lca.building_envelope.Surface
        The surfaces assigned to this construction.
    __type__ : str
        Fixed varialble specifying window type. 
    wall_key : str
        The key or name of the wall the window is assigned to. 
    width :  ~pod_lca.units.Quantity
        The width of the window
    length :  ~pod_lca.units.Quantity
        The length of the window
    wwr :  ~pod_lca.units.Quantity
        The window-to-wall ratio of the window
    """
    def __init__(self):
        super().__init__()
        self.surfaces = {}
        self.__type__ = 'Window'
        self.wall_key = None # the wall this window is related to
        self.width = None
        self.height = None
        self.wwr = None

    def set_width_height(self, width, height):
        """Sets the width and height of the window

        Parameters
        ----------
        width :  ~pod_lca.units.Quantity
            The width of the window.
        length :  ~pod_lca.units.Quantity
            The length of the window.
        """
        self.width = width
        self.height = height

    def set_wwr(self, wwr):
        """Sets the window-to-wall ratio of the window.

        Parameters
        ----------
        wwr :  ~pod_lca.units.Quantity
            The window-to-wall ratio of the window
        """
        self.wwr = wwr

    @classmethod
    def from_data(cls, data):
        """Creates an instance of the window from a data dictionary. 

        Parameters
        ----------
        data : dict
            The data dictionary. 

        Returns
        -------
        win : ~pod_lca.building_envelope.Window
            The window instance. 
        """
        win = cls()
        win.name         = data['name']
        win.wall_key     = data['wall_key']
        win.width        = data['width']
        win.height       = data['height']
        win.wwr          = data['wwr']
        win.materials    = data['materials']
        win.service_life_category = data['service_life_category']
        win.layers       = data['layers']
        win.layer_order  = data['layer_order']
        win.surfaces     = {}
        for sk in data['surfaces']:
            win.surfaces[sk] = Surface.from_data(data['surfaces'][sk])
        for mat in data['materials']:
            mat.set_parent(win)

        return win

    def to_data(self):
        """Returns a dictionary containing all of the Window data. 

        Returns
        -------
        data : dict
            The dictionary containing all window data.  
        """
        data = {}
        data['name']            = self.name
        data['wall_key']        = self.wall_key       
        data['width']           = self.width          
        data['height']          = self.height        
        data['wwr']             = self.wwr          
        data['materials']       = self.materials
        data['service_life_category']  = self.service_life_category
        data['layers']          = self.layers
        data['layer_order']     = self.layer_order
        data['surfaces'] = {}
        for sk in self.surfaces:
            data['surfaces'][sk] = self.surfaces[sk].to_data()
        return data
   
    @property
    def area(self):
        """Returns the surface area of the window. 

        Returns
        -------
        area : ~pod_lca.units.Quantity
            The window wurface area. 
        """
        area = Q(0, SQUARE_METER)
        for s in self.surfaces:
            area += self.surfaces[s].area
        return area
    
    def create_window_surface_from_envelope_wall_key(self, envelope, wall_key):
        """Generates the windo surface given an envelope wall. The geometry is
        generated using the window objects wwr. 

        Parameter
        ---------
        envelope : ~pod_lca.building_envelope.Envelope
            The envelope where the wall is located. 
        wall_key : str
            The key / name of the wall where the window is to be made. 
        """
        polygon = envelope.surfaces[wall_key].polygon
        cpt = centroid(polygon)

        if self.wwr:
            if self.wwr > .95:
                wwr = .95
            else:
                wwr = self.wwr
            area =  area_polygon(polygon).value * wwr
            lx = distance_point_point(polygon[0], polygon[1]) - .1
            ly = area / lx

        elif self.width:
            lx = self.width
            ly = self.height
        
        vx  = scale_vector(normalize_vector(subtract_vectors(polygon[0], polygon[1]), unitless=True), lx / 2.)
        vy  = scale_vector(normalize_vector(subtract_vectors(polygon[0], polygon[-1]), unitless=True), ly / 2.)
        vx_ = scale_vector(normalize_vector(subtract_vectors(polygon[0], polygon[1]), unitless=True), -lx / 2.)
        vy_ = scale_vector(normalize_vector(subtract_vectors(polygon[0], polygon[-1]), unitless=True), -ly / 2.)

        p0 = add_vectors(cpt, add_vectors(vx_, vy_))
        p1 = add_vectors(cpt, add_vectors(vx, vy_))
        p2 = add_vectors(cpt, add_vectors(vx, vy))
        p3 = add_vectors(cpt, add_vectors(vx_, vy))

        sk = 'window_{}'.format(wall_key)
        self.surfaces[sk] = Surface.from_polygon(sk, [p0, p1, p2, p3], surface_type = 'Window')



if __name__ == '__main__':
    pass