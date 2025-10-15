
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from . import TransportationLeg
from . import TransportMode
from ..location import Location
from ...units import KILOMETER
from ...utilities import log


class ForeignLeg(TransportationLeg):
    """ A leg of Global transportation.
    
    Attributes
    ----------
    transport_scenario : {'Global'}
        A discriptor of the tranportation scenario.
    """

    def __init__(self):
        super().__init__()
        self.transport_scenario = None
        self._cache_travel_dist = None
        self._last_params = None

    # ================================
    # Constructors
    # ================================
    @classmethod
    def in_project(cls, good, project, name=None):
        """ Create a new transportation leg in the project. Also create a corresponding domestic transportation leg.

        Parameters
        ----------
        good : ~pod_lca.materials_screening.Master
            Product being transported.
        project : ~pod_lca.materials_screening.Project
            The project to which the transportation leg belongs.
        name : str
            Name of the transportation leg (default is None).

        Returns
        -------
        ~pod_lca.transportation.TransportationLeg
            Transportation leg created in the project.
        """
        leg = super().in_project(good, project, name)

        domestic_leg = TransportationLeg.in_project(good, project, name + '_domestic')
        leg.set_next(domestic_leg)

        return leg
    
    # ================================
    # Setters
    # ================================
    def set_transport_scenario(self, transport_scenario:(str)):
        """ Set the transport scenario of the transportation leg.

        Parameters
        ----------
        transport_scenario : {'Global'}
            Transport scenario of the transportation leg.

        Raises
        ------
        ValueError
            Transportation scenario not recognized.
        TypeError
            Transportation scenario is not None or a string.
        """
        if transport_scenario is None:
            self.transport_scenario = None
        elif isinstance(transport_scenario, str):
            if transport_scenario in ["Global"]:
                self.transport_scenario = transport_scenario
            else:
                raise ValueError("Transportation scenario not recognized")
        else:
            raise TypeError("Transport scenario must be a string.")

        self._invalidate_cache()
        return self

    def set_material(self, material):
        """ Set the material being transported.

        Parameters
        ----------
        material : ~pod_lca.materials_screening.Product
            Material being transported.
        """
        self = super().set_material(material)
        self._invalidate_cache()
        return self
    
    def set_shipping_destination(self, shipping_dest=None):
        """ Set the shipping destination of the project.

        Parameters
        ----------
        shipping_dest : ~pod_lca.location.Location
            Name of the shipping destination location.
        """
        if shipping_dest is None:
            most_common_state = self.get_dataset().find_most_common_US_destination(self.get_material())
            self.shipping_destination = Location.from_US_state(most_common_state)
        else:
            super().set_shipping_destination(shipping_dest)

        self._invalidate_cache()
        return self
        
    def set_shipping_origin(self, shipping_org=None):
        """ Set the shipping origin of the project.

        Parameters
        ----------
        shipping_org : ~pod_lca.location.Location
            Name of the shipping origin location.
        """
        if shipping_org is None:
            most_common_faf_region = self.get_dataset().find_most_common_FAF_origin(self.get_material(), self.get_shipping_destination())
            self.shipping_origin = Location.from_faf_regions(most_common_faf_region)
        else:
            super().set_shipping_origin(shipping_org)

        self._invalidate_cache()
        return self

    def set_mode(self, mode, efficiency):
        """ Set the transportation mode of the transportation leg.

        Parameters
        ----------
        mode : str or ~pod_lca.transportation.TransportMode
            Transportation mode of the transportation leg.
        efficiency : {'High', 'Median', 'Low'}
            Efficiency of the transportation mode.

        Raises
        ------
        ValueError
            Transportation mode not recognized.
        """
        if isinstance(mode, TransportMode):
            self.mode = mode
            self.get_next().set_mode(mode)
        
        else:
            mode_efficiency = 'Median' if efficiency is None else efficiency
            foreign_mode_name = 'Ocean' if mode is None else mode
            
            foreign_mode_obj = TransportMode.new(foreign_mode_name, mode_efficiency)
            self.mode = foreign_mode_obj
        
        # set domestic mode
        mode_name =  mode if isinstance(mode, str) else self.mode.get_name()
        if mode_name in ['Rail', 'Air']:
            domestic_mode_obj = TransportMode.new(foreign_mode_name, mode_efficiency)
            self.get_next().set_mode(domestic_mode_obj)
        elif mode_name in ['Truck', 'Ocean']:
            domestic_mode_obj = TransportMode.new('Truck', mode_efficiency)
            self.get_next().set_mode(domestic_mode_obj)
        else:
            raise ValueError("Transportation mode not recognized.")

        self.mode.set_parent(self)
        self.mode.set_inventory_records()
        
        return self
        
    def set_travel_dist(self, travel_dist=None, dist_unit=None, return_trip_factor=None):
        """ Set the travel distance of the transportation leg.

        Parameters
        ----------
        travel_dist : None
            For ForeignLink objects travel distance are autogenerated using a dataset.
        dist_unit : ~pod_lca.units.Unit
            Unit of the travel distance.
        return_trip_factor : float
            Return trip factor of the transportation leg (default is None).
        """
        self.dist_unit = KILOMETER if dist_unit is None else dist_unit
        self._invalidate_cache()
        return self
 
    # ================================
    # Getters
    # ================================
    def get_domestic_leg(self):
        """ Get the corresponding domestic leg of transportation.

        Returns
        -------
        ~pod_lca.transportation.TransportationLeg
            Domestic transportation leg.
        """
        return self.next

    def get_transport_scenario(self):
        """ Retrieve the transport scenario of the transportation leg.

        Returns
        -------
        str
            The transport scenario of the transportation leg.
        """
        return self.transport_scenario
     
    def get_travel_dist(self):
        """ Get the travel distance of the transportation leg.

        Returns
        -------
        float
            travel distance of the transportation leg.
        """
        current_params = (self.get_material(), 
                          self.get_shipping_destination(), 
                          self.get_shipping_origin(), 
                          self.get_mode().get_name(),
                          self.get_mode().get_efficiency(),
                          self.get_domestic_leg().get_mode().get_name(),
                          self.get_domestic_leg().get_mode().get_efficiency(),
                          self.get_transport_scenario(), 
                          self.get_dist_unit())

        if self._last_params == current_params and self._cache_travel_dist is not None:
            log("Returning cached result.", "Info")
            return self._cache_travel_dist
        else:
            transport_scenario = self.get_transport_scenario()

            domestic_dis, foreign_travel_dist = self.get_distance_from_dataset(transport_scenario)
            self.get_next().set_travel_dist(domestic_dis, self.get_dist_unit(), self.get_return_trip_factor())    

            self._cache_travel_dist = foreign_travel_dist
            self._last_params = current_params                               

            return foreign_travel_dist

    def get_return_trip_factor(self):   
        """ Retrieve the return trip factor of the transportation leg.

        Returns
        -------
        float
            The return trip factor of the transportation leg.
        """
        return 1.0
 
    def get_dataset(self):
        """ Get the dataset.

        Returns
        -------
        ~pod_lca.transportation.TransportDataset
            Dataset used.
        """
        return self.get_manager().get_dataset()
    
    # ================================
    # Dataset Methods
    # ================================
    def get_distance_from_dataset(self, transport_scenario):
        """ Get the average distance from the CFS dataset based on the scenario.

        Parameters
        ----------
        scenario : {'Global'}
            The tranportation scenario.

        Returns
        -------
        float
            The distance estimate for the specified scenario.

        Raises
        ------
        ValueError
            The transportation origin and transportation mode are inconsistant.
        """
        dataset = self.get_dataset()

        if not self.check_mode_origin_compatibility():
            raise ValueError(f'The transportation origin and transportation mode are inconsistant.')

        conversion_factor = self.get_dist_unit().convert_to(KILOMETER)
        datasets_filtered = dataset.filter_datasets(self.get_material(), self.get_shipping_destination(), self.get_shipping_origin(), self.get_next().get_mode(), self.get_mode())
        domestic_dis, foreign_dis = dataset.get_distance_estimate(datasets_filtered, self.get_shipping_destination(), self.get_shipping_origin(), self.get_mode().get_name())

        return domestic_dis * conversion_factor, foreign_dis * conversion_factor

    def check_mode_origin_compatibility(self):
        """ Check if the mode and origin combinations are realistic.
        """
        if self.get_mode().get_name() == 'Truck':
            if not self.get_shipping_origin().get_country_code() in ['CA', 'MX']:
                return False

        if self.get_mode().get_name() == 'Rail':
            if not self.get_shipping_origin().get_country_code() == 'CA':
                return False

        return True
    
    # ================================
    # Cache Method
    # ================================
    def _invalidate_cache(self):
        self._cache_travel_dist = None
        self._last_params = None


if __name__ == '__main__':
    pass
