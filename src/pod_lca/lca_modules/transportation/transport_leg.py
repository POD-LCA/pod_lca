
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from . import ElectricTransportMode
from ..impacts import Emissions
from ..impacts import Impacts
from ..location import Location
from . import TransportMode
from ...units import KILOMETER
from ...units import MILE


class TransportationLeg:
    """ A generic transportation leg of transporting goods.

    Attributes
    ----------
    manager : pod_lca.transportation.TransportationManager
        Refers to the transportation manager.
    name : str
        Name of the logistic leg.
    material : str
        name of the material.
    travel_dist : float
        transportation distance
    dist_unit : ~pod_lca.units.Unit
        Unit corresponding to the travel distance.
    return_trip_factor : float
        transportation return trip factor.
    shipping_dest : ~pod_lca.location.Location
        shipping destination location.
    shipping_org : ~pod_lca.location.Location
        shipping origin location.
    mode : ~pod_lca.transportation.TransportationMode
        transportation mode.
    impacts : ~pod_lca.impacts.Impacts
        Environmental impacts of the transportation leg.
    emissions : ~pod_lca.impacts.Emissions
        Emissions of the transportation leg.
    next : ~pod_lca.transportation.TransportationLeg
        Next transportation leg for the goods transported.
    previous : ~pod_lca.transportation.TransportationLeg
        Previous transportation leg for the goods transported.
    """

    def __init__(self):
        self.manager = None
        self.name = None
        self.material = None
        self.travel_dist = None
        self.dist_unit = None
        self.return_trip_factor = None
        self.shipping_destination = None
        self.shipping_origin = None
        self.mode = None
        self.impacts = None
        self.emissions = None
        self.next = None
        self.previous = None

    def __str__(self):
        str = "="*75 + "\n" + f"Material: {self.get_material()} | Quantity: {self.get_qty()} | Travel distance: {self.get_travel_dist() } | Mode_domestic: {self.get_mode_domestic()}\n"

        return str

    # ================================
    # Constructors
    # ================================
    @classmethod
    def in_project(cls, good, manager, name=None):
        """ Create a new transportation leg in the project.

        Parameters
        ----------
        good : ~pod_lca.material_screening.Product
            Product being transported.
        manager :  ~pod_lca.transportation.TransportationManager
            The project to which the transportation leg belongs.
        name : str, optional
            Name of the transportation leg (default is None).

        Returns
        -------
         ~pod_lca.transportation.TransportationLeg
            Transportation leg created in the project.
        """
        leg = cls()
        leg.set_material(good)
        leg.set_manager(manager)
        leg.set_name(name)

        leg.impacts = Impacts.from_parent(leg)
        leg.emissions = Emissions.from_parent(leg)

        manager.transport_legs[good].append(leg)

        return leg

    # ================================
    # Setters
    # ================================
    def set_manager (self, manager):
        """ Set the project the transportation leg belongs to.

        Parameters
        ----------
        project : pod_lca.transportation.TransportationManager
            The project to which the transportation leg belong.
        """
        self.manager = manager

        return self

    def set_name (self, name):
        """ Set the name of the transportation leg.

        Parameters
        ----------
        name : str
            Name of the transportation leg.
        """
        self.name = name

        return self

    def set_material(self, material):
        """ Set the material being transported.

        Parameters
        ----------
        material : ~pod_lca.material_screening.Product
            Material being transported.
        """
        self.material = material
        if isinstance(self.get_next(), TransportationLeg):
            self.get_next().set_material(material)  

        return self

    def set_travel_dist(self, 
                        travel_dist, 
                        dist_unit=None, 
                        return_trip_factor=None):
        """ Set the travel distance of the transportation leg.

        Parameters
        ----------
        travel_dist : float
            Travel distance of the transportation leg.
        dist_unit : ~pod_lca.units.Unit, optional
            Unit of the travel distance. Defualt is KILOMETER
        return_trip_factor : float, optional
            Return trip factor of the transportation leg.
        """
        if isinstance(travel_dist, (float, int)):
            self.travel_dist = travel_dist
        else:
            raise ValueError("Travel distance must be a number.")

        self.dist_unit = KILOMETER if dist_unit is None else dist_unit
        self.return_trip_factor = return_trip_factor

        return self

    def set_shipping_destination(self, shipping_dest):
        """ Set the shipping destination of the project.

        Parameters
        ----------
        shipping_dest : ~pod_lca.location.Location
            Name of the shipping destination location.
        """
        if shipping_dest is None:
            self.shipping_destination = None
        elif isinstance(shipping_dest, Location):
            self.shipping_destination = shipping_dest
        else:
            raise ValueError("Shipping destination must be a Location object.")

        return self

    def set_shipping_origin(self, shipping_org):
        """ Set the shipping origin of the project.

        Parameters
        ----------
        shipping_org : ~pod_lca.location.Location
            Name of the shipping origin location.
        """
        if shipping_org is None:
            self.shipping_origin = None
        elif isinstance(shipping_org, Location):
            self.shipping_origin = shipping_org
        else:
            raise ValueError("Shipping origin must be a Location object.")

        return self

    def set_mode(self, mode=None, efficiency=None):
        """ Set the transportation mode of the transportation leg.

        Notes
        -----
        1. Prefix 'E_' in the mode_name is used as the identifier of an electricity based transportation mode.
        2. Electric vehicles takes electricity based on origin location.
        
        Parameters
        ----------
        mode : str or ~pod_lca.transportation.TransportMode
            transportation mode of the transportation leg.
        efficiency : {'Low', 'Median', 'High'}
            Efficiency of the transportation mode.
        """
        if isinstance(mode, TransportMode):
            self.mode = mode
        else:
            mode_efficiency = "Median" if efficiency is None else efficiency
            mode_name = "Truck" if mode is None else mode

            if mode_name[0:2] == 'E_':
                self.mode = ElectricTransportMode.new(mode_name[2:], mode_efficiency)
                self.mode.set_location(self.get_shipping_origin())
            else:
                self.mode = TransportMode.new(mode_name, mode_efficiency)
        
        self.mode.set_parent(self)
        self.mode.set_inventory_records()

        return self

    def set_next(self, next):
        """ Set the next transportation leg for the material.

        Returns
        -------
        ~pod_lca.transportation.TransportationLeg
            The next transportation leg for the same material.
        """
        self.next = next
        next.previous = self

        return self
    
    # ================================
    # Getters
    # ================================
    def get_manager(self):
        """ Retrieve the project of the transportation leg.

        Returns
        -------
        pod_lca.transportation.TransportationManager
            The project of the transportation leg.
        """
        return self.manager 

    def get_name(self):
        """ Retrieve the name of the transportation leg.

        Returns
        -------
        str
            The name of the transportation leg.
        """
        return self.name

    def get_material(self):
        """ Retrieve the material of the transportation leg.

        Returns
        -------
        ~pod_lca.materials_screening.Product
            The material of the transportation leg.
        """
        return self.material

    def get_travel_dist(self):
        """ Retrieve the travel distance of the transportation leg.

        Returns
        -------
        float or str
            The travel distance of the transportation leg.
        """
        return self.travel_dist
    
    def get_dist_unit(self):
        """ Retrieve the distance unit of the transportation leg.

        Returns
        -------
        ~pod_lca.units.Unit
            The distance unit of the transportation leg.
        """
        return self.dist_unit

    def get_return_trip_factor(self):   
        """ Retrieve the return trip factor of the transportation leg.

        Returns
        -------
        float
            The return trip factor of the transportation leg.
        """
        return self.return_trip_factor
        
    def get_shipping_destination(self):
        """ Retrieve the shipping destination of the project.

        Returns
        -------
        str
            Name of the shipping destination location.
        """
        return self.shipping_destination

    def get_shipping_origin(self):
        """ Retrieve the shipping origin of the project.

        Returns
        -------
        ~pod_lca.location.Location
            Shipping origin location.
        """
        return self.shipping_origin

    def get_mode(self):
        """ Retrieve the transportation mode of the transportation leg.

        Returns
        -------
        ~pod_lca.transportation.TransportMode
            The domestic transportation mode of the transportation leg.
        """
        return self.mode
    
    def get_next(self):
        """ Retrieve the next transportation leg for the material.

        Returns
        -------
        ~pod_lca.transportation.TransportationLeg
            The next transportation leg for the same material.
        """
        return self.next
    
    def get_previous(self):
        """ Retrieve the previous transportation leg for the material.

        Returns
        -------
        ~pod_lca.transportation.TransportationLeg
            The previous transportation leg for the same material.
        """
        return self.previous

    def get_impacts(self):
        """ Retrieve the impact of the transportation leg.

        Returns
        -------
        ~pod_lca.impacts.Impacts
            The impact of the transportation leg.
        """
        self.update_inventory_records()
        return self.impacts 
    
    def get_emissions(self):
        """ Retrieve the emissions of the transportation leg.

        Returns
        -------
        ~pod_lca.impacts.Emissionbs
            The emissions of the transportation leg.
        """
        self.update_inventory_records()
        return self.emissions 
    
    def get_impact_database(self):
        """ Get the impact database.

        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            Impacts database
        """
        return self.get_manager().get_impact_database()

    # ================================
    # Methods
    # ================================ 
    def update_inventory_records(self):
        """ Compute and update all invetories.
        """
        inventories_declared_unit = self.get_mode().get_declared_unit()
        computed_unit = self.get_material().get_unit() * self.get_dist_unit()
        conversion_factor = computed_unit.convert_to(inventories_declared_unit)

        travel_dist = self.get_travel_dist()
        transport_material_qty = self.get_material().get_qty()
        return_trip_factor = self.get_return_trip_factor()

        if conversion_factor is None:
            raise ImportError(f"{self.get_name()} (of units {self.get_unit()}) and the LCA data chosen ({self.get_impact_database_entry()} of units {self.declared_unit}) are of incompatible units.")
        
        impacts = {key: self.get_mode().get_unit_impacts().get_record(key) * conversion_factor * transport_material_qty * travel_dist * return_trip_factor for key in self.impacts.record_attr_dict}
        self.impacts.update_qty(impacts)

        emissions = {key: self.get_mode().get_unit_emissions().get_record(key) * conversion_factor * transport_material_qty * travel_dist * return_trip_factor for key in self.emissions.record_attr_dict}
        self.emissions.update_qty(emissions)

        return self


if __name__ == '__main__':
    pass
