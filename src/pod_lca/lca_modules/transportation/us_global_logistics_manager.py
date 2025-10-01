
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from ..transportation import USGlobalDataset
from ..transportation import DomesticLeg
from ..transportation import ForeignLeg
from ..transportation import TransportationLeg
from ..transportation import TransportationManager
from ...units import KILOMETER


class USGlobalTransportationManager(TransportationManager):
    """ A project in US using global logistic.

    Attributes
    ----------
    dataset : ~pod_lca.transportation.TransportDataset
        Dataset corresponding to the project.    
    """

    def __init__(self):
        super().__init__()
        self.dataset = None

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
        ~pod_lca.transportation.TransportationManager
            Project created.
        """
        new_project = super().new(name)
        new_project.set_dataset(USGlobalDataset())

        return new_project  
    
    # ================================
    # Setters and Getters
    # ================================
    def set_dataset(self, dataset):
        """ Set background dataset for the proect.

        Parameters
        ----------
        dataset : ~pod_lca.transportation.TransportDataset
            Dataset corresponding to the project.           
        """
        self.dataset = dataset

        return self

    def get_dataset(self, name=None):
        """ Return the dataset corresponding to the project.

        Returns
        -------
        ~pod_lca.transportation.TransportDataset
            Dataset corresponding to the project.
        """
        if name is None:
            return self.dataset
        elif isinstance(self.database, dict) and isinstance(name, str):
            return self.dataset[name] 
        
    # ================================
    # Model Methods
    # ================================
    def add_good(self, good, travel_dist=None, shipping_dest=None, shipping_org=None,
                 transport_scenario=None, distance_unit= KILOMETER, return_trip_factor=None, 
                 mode_name='Ocean', mode_efficiency='Median'):
        """ Add good to the project. This method creates the appropriate tranportation leg based on the data provided

        Parameters
        ----------
        good : list of ~pod_lca.materials_screening.Product
            Good to be transported.
        travel_dist : float
            Transportation distance for goods.
        shipping_dest : ~pod_lca.location.Location
            Shipping destination.
        shipping_org : ~pod_lca.location.Location
            Shipping origin
        transport_scenario : {'Global'}
            Transportation scenario considered.
        distance_unit : ~pod_lca.units.Unit
            Unit of measurement of distances.
        return_trip_factor : float
            Return trip factor.
        mode_name : {'Truck', 'E_Truck', 'Rail', 'Ocean', 'Air'}
            Name of the transportation mode.
        mode_efficiency : {'High', 'Median', 'Low'}
            Efficiency of the transportation mode. Default is 'Median'.

        Raises
        ------
        ValueError
            Transport scenario not recognized.
        """
        self.transport_legs[good] = []

        # select type of tranportation leg
        if isinstance(travel_dist, (int, float)):
            LinkClass = TransportationLeg

        elif (shipping_dest is not None) and (shipping_org is not None):
            if (shipping_dest.get_country_code() == 'US') and not (shipping_org.get_country_code() == 'US'):
                LinkClass = ForeignLeg
            else:
                raise ValueError("This project is for US global logistics only")

        else:
            LinkClass = ForeignLeg

        # create transport leg
        leg = LinkClass.in_project(good, self, 'transport_' + good.get_name())
        
        leg.set_mode(mode_name, mode_efficiency)

        leg.set_travel_dist(travel_dist, distance_unit, return_trip_factor)
        leg.set_shipping_destination(shipping_dest)
        leg.set_shipping_origin(shipping_org)
        if isinstance(leg, (DomesticLeg, ForeignLeg)):
            leg.set_transport_scenario(transport_scenario)

        return self


if __name__ == '__main__':
    pass
