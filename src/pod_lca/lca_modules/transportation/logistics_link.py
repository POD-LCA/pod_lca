
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from ..transportation import TransportMode
from ..location import Location
from ...units import KILOMETER


class LogisticLink:
    """ Link object create a link of transportation for each material.

    Attributes
    ----------
    project : Project obj.
        Refers to the main project.
    material : str.
        name of the material.
    qty : str.
        quantity of the of the material.
    travel_dist : float or str.
        transportation distance, if float; transportaion scenario, if string
    travel_dist_unit : Unit Obj.
        Unit corresponding to the travel distance.
    return_trip_factor : float.
        transportation return trip factor.
    mode : TransportationMode Obj.
        transportation mode.
    shipping_dest : Location obj.
        shipping destination location.
    shipping_org : Location obj.
        shipping origin location.
    impacts : Impacts obj.
        Environmental impacts of the transportation link.
    emissions : Emissions obj.
        Emissions of the transportation link.
    electricity_consumption : float.
        Electricity consumption of the transportation link.
    next : LogisticLink obj.
        Next transportation link for the goods transported.
    previous : LogisticLink obj.
        Previous transportation link for the goods transported.
    """

    def __init__(self):
        self.project = None
        self.name = None
        self.material = None
        self.transport_scenario = None
        self.travel_dist = None
        self.travel_dist_unit = None
        self.return_trip_factor = None
        self.mode = None
        self.shipping_dest = None
        self.shipping_org = None
        self.impacts = None
        self.emissions = None
        self.electricity_consumption = None
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
    def in_project(cls, project, name=None):
        """ Create a new transportation link in the project.

        Parameters
        ----------
        project : Project obj.
            The project to which the transportation link belongs.
        name : str, optional
            Name of the transportation link (default is None).

        Returns
        -------
        Link obj.
            Transportation link created in the project.
        """
        link = cls()
        link.set_project(project)
        if name is not None:
            link.set_name(name)
        else:
            link.set_name(f"Link_{len(project.links)}")

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

    def set_name (self, name:(str)):
        """ Set the name of the transportation link.

        Parameters
        ----------
        name : str
            Name of the transportation link.
        """
        self.name = name

        return self

    def set_material(self, material:(str)):
        """ Set the quantity of the transportation link.

        Parameters
        ----------
        material : Master Obj.
            Material name of the transportation link.
        """
        self.material = material    

        return self
    
    def set_transport_scenario(self, transport_scenario:(str)):
        """ Set the transport scenario of the transportation link.

        Parameters
        ----------
        transport_scenario : str
            Transport scenario of the transportation link (e.g., "North_america", "Global", "Known").
        """
        if transport_scenario is None:
            self.transport_scenario = None # TODO set the default transport scenario
        elif isinstance(transport_scenario, str):
            self.transport_scenario = transport_scenario
        else:
            raise ValueError("Transport scenario must be a string.")

        return self

    def set_travel_dist(self, 
                        travel_dist, 
                        travel_dist_unit= KILOMETER, 
                        return_trip_factor:(float) = None):
        """ Set the travel distance of the transportation link.

        Parameters
        ----------
        travel_dist : float or str
            travel distance of the transportation link.
        travel_dist_unit : str, optional
            Distance unit of the travel distance (default is "km").
        return_trip_factor : float, optional
            Return trip factor of the transportation link (default is None).
        """
        if isinstance(travel_dist, (float, int)):
            self.travel_dist = travel_dist
        else:
            raise ValueError("Travel distance must be a number.")

        self.travel_dist_unit = travel_dist_unit
        self.return_trip_factor = return_trip_factor

        return self

    def set_mode(self, mode:(str) , fuel_type:(str) , efficiency:(str) ):
        """ Set the transportation mode of the transportation link.

        Parameters
        ----------
        mode : str
            transportation mode of the transportation link.
        fuel_type : str, optional
            type of fuel used in the transportation mode (default is "Regular").
        efficiency : str, optional
            efficiency of the transportation mode "low, medium, high" (default is "medium").
        """
        fuel_type = "Regular" if fuel_type is None else fuel_type
        mode_efficiency = "Median" if efficiency is None else efficiency
        mode_name = "Truck" if mode is None else mode

        self.mode = TransportMode.new(mode_name, mode_efficiency, fuel_type)

        return self

    def set_shipping_dest(self, shipping_dest:(str)):
        """ Set the shipping destination of the project.

        Parameters
        ----------
        shipping_dest : str
            Name of the shipping destination location.
        """
        if shipping_dest is None:
            self.shipping_dest = None
        elif isinstance(shipping_dest, Location):
            self.shipping_dest = shipping_dest
        elif isinstance(shipping_dest, str):
            self.shipping_dest = Location.from_str(shipping_dest)
        else:
            raise ValueError("Shipping destination must be a Location object or a string representing the location.")

        return self

    def set_shipping_org(self, shipping_org:(str)):
        """ Set the shipping origin of the project.

        Parameters
        ----------
        shipping_org : str
            Name of the shipping origin location.
        """
        if shipping_org is None:
            self.shipping_org = None
        elif isinstance(shipping_org, Location):
            self.shipping_org = shipping_org
        elif isinstance(shipping_org, str):
            self.shipping_org = Location.from_str(shipping_org)
        else:
            raise ValueError("Shipping origin must be a Location object or a string representing the location.")

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
    
    def get_transport_scenario(self):
        """ Retrieve the transport scenario of the transportation link.

        Returns
        -------
        str
            The transport scenario of the transportation link.
        """
        return self.transport_scenario
    
    def get_mode(self):
        """ Retrieve the transportation mode of the transportation link.

        Returns
        -------
        TransportMode obj.
            The domestic transportation mode of the transportation link.
        """
        return self.mode

    def get_shipping_dest(self):
        """ Retrieve the shipping destination of the project.

        Returns
        -------
        str
            Name of the shipping destination location.
        """
        return self.shipping_dest

    def get_shipping_org(self):
        """ Retrieve the shipping origin of the project.

        Returns
        -------
        str
            Name of the shipping origin location.
        """
        return self.shipping_org

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
        str
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
        pass

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

    def get_impact(self):
        """ Retrieve the impact of the transportation link.

        Returns
        -------
        Impacts obj.
            The impact of the transportation link.
        """
        self.impact = self.get_material().get_qty() * self.get_travel_dist() * self.get_return_trip_factor() * self.get_mode().get_unit_impacts()  # TODO: add unit_conversion

        return self.impact 
    
    def get_electricity_consumption(self):
        """ Retrieve the electricity consumption of the transportation link.

            Returns
            -------
            float
                The electricity consumption of the transportation link.
        """
        return self.electricity_consumption

# TODO: global travel
# TODO: unit mapping
# TODO: issue of combined domestic and international legs
# TODO: transport mode combined with the database manager


if __name__ == '__main__':
    pass
