
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from ..impacts import Emissions
from ..impacts import Impacts
from ..location import Location
from ..transportation import TransportMode
from ...units import KILOMETER
from ...units import MILE


class LogisticLink:
    """ A generic transportation link of transporting goods.

    Attributes
    ----------
    project : Project obj.
        Refers to the main project.
    name : str
        Name of the logistic link.
    material : str.
        name of the material.
    travel_dist : float.
        transportation distance
    travel_dist_unit : Unit Obj.
        Unit corresponding to the travel distance.
    return_trip_factor : float.
        transportation return trip factor.
    shipping_dest : Location obj.
        shipping destination location.
    shipping_org : Location obj.
        shipping origin location.
    mode : TransportationMode Obj.
        transportation mode.
    impacts : Impacts obj.
        Environmental impacts of the transportation link.
    emissions : Emissions obj.
        Emissions of the transportation link.
    next : LogisticLink obj.
        Next transportation link for the goods transported.
    previous : LogisticLink obj.
        Previous transportation link for the goods transported.
    """

    def __init__(self):
        self.project = None
        self.name = None
        self.material = None
        self.travel_dist = None
        self.travel_dist_unit = None
        self.return_trip_factor = None
        self.shipping_dest = None
        self.shipping_org = None
        self.mode = None
        self.impacts = None
        self.emissions = None
        self.next = None
        self.previous = None

    def __str__(self):
        """ String representation of the Link object.

        Returns
        -------
        str
            String representation of the Link object.
        """
        str = "="*75 + "\n" + f"Material: {self.get_material()} | Quantity: {self.get_qty()} | Travel distance: {self.get_travel_dist() } | Mode_domestic: {self.get_mode_domestic()}\n"

        return str

    # ================================
    # Constructors
    # ================================
    @classmethod
    def in_project(cls, good, project, name=None):
        """ Create a new transportation link in the project.

        Parameters
        ----------
        good : Master obj.
            Product being transported.
        project : Project obj.
            The project to which the transportation link belongs.
        name : str, optional
            Name of the transportation link (default is None).

        Returns
        -------
        LogisticLink obj.
            Transportation link created in the project.
        """
        link = cls()
        link.set_material(good)
        link.set_project(project)
        link.set_name(name)

        link.impacts = Impacts.from_parent(link)
        link.emissions = Emissions.from_parent(link)

        project.goods_links_map[good].append(link)

        return link

    # ================================
    # Setters
    # ================================
    def set_project (self, project):
        """ Set the project of the transportation link.

        Parameters
        ----------
        project : Project obj.
            The project of the transportation link.
        """
        self.project = project

        return self

    def set_name (self, name):
        """ Set the name of the transportation link.

        Parameters
        ----------
        name : str
            Name of the transportation link.
        """
        self.name = name

        return self

    def set_material(self, material):
        """ Set the quantity of the transportation link.

        Parameters
        ----------
        material : Master Obj.
            Material name of the transportation link.
        """
        self.material = material
        if isinstance(self.get_next(), LogisticLink):
            self.get_next().set_material(material)  

        return self

    def set_travel_dist(self, 
                        travel_dist, 
                        travel_dist_unit=None, 
                        return_trip_factor=None):
        """ Set the travel distance of the transportation link.

        Parameters
        ----------
        travel_dist : float
            Travel distance of the transportation link.
        travel_dist_unit : Unit Obj
            Unit of the travel distance.
        return_trip_factor : float
            Return trip factor of the transportation link (default is None).
        """
        if isinstance(travel_dist, (float, int)):
            self.travel_dist = travel_dist
        else:
            raise ValueError("Travel distance must be a number.")

        self.travel_dist_unit = KILOMETER if travel_dist_unit is None else travel_dist_unit
        self.return_trip_factor = return_trip_factor

        return self

    def set_shipping_destination(self, shipping_dest):
        """ Set the shipping destination of the project.

        Parameters
        ----------
        shipping_dest : Location Obj.
            Name of the shipping destination location.
        """
        if shipping_dest is None:
            self.shipping_dest = None
        elif isinstance(shipping_dest, Location):
            self.shipping_dest = shipping_dest
        else:
            raise ValueError("Shipping destination must be a Location object.")

        return self

    def set_shipping_origin(self, shipping_org):
        """ Set the shipping origin of the project.

        Parameters
        ----------
        shipping_org : Location Obj.
            Name of the shipping origin location.
        """
        if shipping_org is None:
            self.shipping_org = None
        elif isinstance(shipping_org, Location):
            self.shipping_org = shipping_org
        else:
            raise ValueError("Shipping origin must be a Location object.")

        return self

    def set_mode(self, mode=None, efficiency=None):
        """ Set the transportation mode of the transportation link.

        Parameters
        ----------
        mode : str or TransportMode Obj
            transportation mode of the transportation link.
        efficiency : str
            efficiency of the transportation mode "low, medium, high" (default is "medium").
        """
        if isinstance(mode, TransportMode):
            self.mode = mode
        else:
            mode_efficiency = "Median" if efficiency is None else efficiency
            mode_name = "Truck" if mode is None else mode

            self.mode = TransportMode.new(mode_name, mode_efficiency)
        
        self.mode.set_parent(self)
        self.mode.set_inventory_records()

        return self

    def set_next(self, next):
        """ Set the next transportation link for the material.

        Returns
        -------
        LogisticLink obj.
            The next transportation link for the same material.
        """
        self.next = next
        next.previous = self

        return self
    
    # ================================
    # Getters
    # ================================
    def get_project(self):
        """ Retrieve the project of the transportation link.

        Returns
        -------
        Project obj.
            The project of the transportation link.
        """
        return self.project 

    def get_name(self):
        """ Retrieve the name of the transportation link.

        Returns
        -------
        str
            The name of the transportation link.
        """
        return self.name

    def get_material(self):
        """ Retrieve the material of the transportation link.

        Returns
        -------
        str
            The material of the transportation link.
        """
        return self.material

    def get_travel_dist(self):
        """ Retrieve the travel distance of the transportation link.

        Returns
        -------
        float or str
            The travel distance of the transportation link.
        """
        return self.travel_dist
    
    def get_dist_unit(self):
        """ Retrieve the distance unit of the transportation link.

        Returns
        -------
        Unit Obj.
            The distance unit of the transportation link.
        """
        return self.travel_dist_unit

    def get_return_trip_factor(self):   
        """ Retrieve the return trip factor of the transportation link.

        Returns
        -------
        float
            The return trip factor of the transportation link.
        """
        if self.return_trip_factor is None:
            dist = self.get_travel_dist()
            convertion_factor = self.get_dist_unit().convert_to(MILE)

            return 1.5 if dist * convertion_factor < 500 else 1.0
        
            # FIXME: 1.5 only truck / domestic
        
        else:
            return self.return_trip_factor
        
    def get_shipping_destination(self):
        """ Retrieve the shipping destination of the project.

        Returns
        -------
        str
            Name of the shipping destination location.
        """
        return self.shipping_dest

    def get_shipping_origin(self):
        """ Retrieve the shipping origin of the project.

        Returns
        -------
        str
            Name of the shipping origin location.
        """
        return self.shipping_org

    def get_mode(self):
        """ Retrieve the transportation mode of the transportation link.

        Returns
        -------
        TransportMode obj.
            The domestic transportation mode of the transportation link.
        """
        return self.mode
    
    def get_next(self):
        """ Retrieve the next transportation link for the material.

        Returns
        -------
        LogisticLink obj.
            The next transportation link for the same material.
        """
        return self.next
    
    def get_previous(self):
        """ Retrieve the previous transportation link for the material.

        Returns
        -------
        LogisticLink obj.
            The previous transportation link for the same material.
        """
        return self.previous

    def get_impacts(self):
        """ Retrieve the impact of the transportation link.

        Returns
        -------
        Impacts obj.
            The impact of the transportation link.
        """
        self.update_inventory_records()
        return self.impacts 
    
    def get_emissions(self):
        """ Retrieve the emissions of the transportation link.

        Returns
        -------
        Emissionbs obj.
            The emissions of the transportation link.
        """
        self.update_inventory_records()
        return self.emissions 

    # ================================
    # Methods
    # ================================ 
    def update_inventory_records(self):
        """ Compute and update all invetories.
        """
        inventories_declared_qty = self.get_mode().get_inventories_declared_qty()
        inventories_declared_unit = self.get_mode().get_inventories_declared_unit()
        computed_unit = self.get_material().get_unit() * self.get_dist_unit()
        conversion_factor = computed_unit.convert_to(inventories_declared_unit)

        travel_dist = self.get_travel_dist()
        transport_material_qty = self.get_material().get_qty()
        return_trip_factor = self.get_return_trip_factor()

        if conversion_factor is None:
            raise ImportError(f"{self.get_name()} (of units {self.get_unit()}) and the LCA data chosen ({self.get_impact_database_entry()} of units {self.inventories_declared_unit}) are of incompatible units.")
        
        impacts = {key: self.get_mode().get_unit_impacts().get_record(key) * conversion_factor * transport_material_qty * travel_dist * return_trip_factor / inventories_declared_qty for key in self.impacts.record_attr_dict}
        self.impacts.update_qty(impacts)

        emissions = {key: self.get_mode().get_unit_emissions().get_record(key) * conversion_factor * transport_material_qty * travel_dist * return_trip_factor / inventories_declared_qty for key in self.emissions.record_attr_dict}
        self.emissions.update_qty(emissions)

        return self


if __name__ == '__main__':
    pass
