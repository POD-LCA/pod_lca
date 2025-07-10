
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from ..transportation import CFSDataset
from ..transportation import DomesticLink
from ..transportation import ForeignLink
from ..transportation import LogisticLink
from ..transportation import ProjectLogisticManager
from ...units import KILOMETER


class USDomesticLogisticProject(ProjectLogisticManager):
    """ A project in US uding domestic logistic.
    """

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, name=None):
        """ Create a new project.

        Parameters
        ----------
        name : str
            Name of the project.

        Returns
        -------
        Project Obj.
            Project created.
        """
        new_project = super().new(name)
        new_project.dataset = CFSDataset()

        return new_project  
    
    # ================================
    # Model Methods
    # ================================
    def add_good(self, 
                  good, 
                  travel_dist=None,
                  shipping_dest=None, 
                  shipping_org=None,
                  transport_scenario=None,
                  distance_unit= KILOMETER, 
                  return_trip_factor=None, 
                  mode_name=None,
                  mode_fuel_type="Regular", 
                  mode_efficiency="Median"):
        """ Add goods to the project. This method creates the appropriate logistick links based on the data provided

        Parameters
        ----------
        goods : list of Product Obj.
            Goods to be transported.
        travel_dist : float
            Transportation distance for goods
        shipping_dest : Location Obj
            Shipping destination.
        shipping_org : Location Obj
            Shipping origin
        transportation_scenario : str
            Transportation scenario considered.
        distance_unit : Unit Obj
            Unit of measurement of distances.
        return_trip_factor : float
            Return trip factor.
        mode_name : str
            Name of the transportation mode.
        mode_fuel_type : str
            Fuel type used by the transportation mode.
        mode_efficiency : str
            Efficiency of the transportation mode.
        """
        self.goods_links_map[good] = []

        # select type of link
        if isinstance(travel_dist, (int, float)):
            LinkClass = LogisticLink

        elif (shipping_dest is not None) and (shipping_org is not None):
            if (shipping_dest.get_country_code() == 'US') and (shipping_org.get_country_code() == 'US'):
                LinkClass = DomesticLink
            else:
                raise ValueError("This project is for US domestic logistics only")

        elif isinstance(transport_scenario, str):
            if transport_scenario in ["National", "Regional_c", "Regional", "Local", "Average"]:
                LinkClass = DomesticLink
            else:
                raise ValueError("Transport scenario not recognized.")
            
        else:
            LinkClass = DomesticLink

        # create link
        link = LinkClass.in_project(good, self, 'transport_' + good.get_name())
        
        link.set_mode(mode_name, mode_efficiency)

        link.set_travel_dist(travel_dist, distance_unit, return_trip_factor)
        link.set_shipping_destination(shipping_dest)
        link.set_shipping_origin(shipping_org)
        if isinstance(link, (DomesticLink, ForeignLink)):
            link.set_transport_scenario(transport_scenario)

        return self


if __name__ == '__main__':
    pass
