import os
import pandas as pd
from lca_modules.transportation.scenarios import Scenario
from lca_modules.transportation.transport_mode import TransportMode
from lca_modules.location.location import Location

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"



class Link:
    
    """
    Link object create a link of transportation for each material.

    Attributes
    ----------
    project : Project obj.
        Refers to the main project.

    material : str.
        name of the material.

    qty : str.
        quantity of the of the material.

    travel_dist : float or str.
        transportation distance.
        transportaion scenario.

    return_trip_factor : float.
        transportation return trip factor.

    dist_unit : str.
        transportation distance unit.

    mode_foreign : str.
        transportation mode (ex: truck, rail).

    mode_domestic : str.
        transportation domestic mode (ex: truck, rail).


    """

    def __init__(self):

        self.project = None
        self.name = None
        self.material = None
        self.qty = 0.0
        self.qty_unit = "tonne" 
        self.travel_dist = None
        self.return_trip_factor = None
        self.travel_dist_unit = "km"
        self.mode_foreign_obj = None
        self.mode_domestic_obj = None 
        self.mode_foreign_name = None
        self.mode_domestic_name = None
        self.mode_domestic_fuel_type = "Regular"
        self.mode_domestic_efficiency = "Median"
        self.mode_foreign_fuel_type = "Regular"
        self.mode_foreign_efficiency = "Median"
        self.shipping_dest = None
        self.shipping_org = None
        self.unit_conversion = {"km": 1, "mi": 0.621371}[self.travel_dist_unit]
        self.link_distances = {"Domestic": 0, "Foreign": 0}
        self.impact_foreign = None
        self.impact_domestic = None
        self.electricity_consumption = None


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


    def set_material (self, material:(str), qty:(float), qty_unit:(str) = "tonne"):
        """ Set the quantity of the transportation link.

            Parameters
            ----------
            material : str
                Material name of the transportation link.
            qty : float
                quantity of the transportation link.
            qty_unit : str, optional
        """
        self.material = material    
        self.qty = qty
        self.qty_unit = qty_unit

    
    def set_travel_dist (self, travel_dist, travel_dist_unit:(str) = "km", return_trip_factor:(float) = None):
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

        self.travel_dist = travel_dist
        self.travel_dist_unit = travel_dist_unit
        self.return_trip_factor = return_trip_factor


    def set_mode_domestic (self, mode:(str) , fuel_type:(str) , efficiency:(str) ):
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

        if fuel_type is not None:
            self.mode_domestic_fuel_type = fuel_type
        
        if efficiency is not None:
            self.mode_domestic_efficiency = efficiency

        if mode is not None:
            self.mode_domestic_name = mode
            self.mode_domestic_obj = TransportMode.new (mode, self.mode_domestic_efficiency, self.mode_domestic_fuel_type)
            self.impact_domestic = self.mode_domestic_obj.get_impact()

        
        
    def set_mode_foreign (self, mode:(str) , fuel_type:(str) , efficiency:(str) ):
        """ Set the transportation foreign mode of the transportation link.

            Parameters
            ----------
            mode : str
                transportation foreign mode of the transportation link.
            fuel_type : str, optional
                type of fuel used in the transportation mode (default is "Regular").
            efficiency : str, optional
                efficiency of the transportation mode "low, medium, high" (default is "medium").
        """

        if fuel_type is not None:
            self.mode_foreign_fuel_type = fuel_type

        if efficiency is not None:
            self.mode_foreign_efficiency = efficiency

        if mode is not None:
            self.mode_foreign_name = mode
            self.mode_foreign_obj = TransportMode.new (mode, self.mode_foreign_efficiency, self.mode_foreign_fuel_type)
            self.impact_foreign = self.mode_foreign_obj.get_impact()


    def set_shipping_dest(self, shipping_dest:(str)):
        """ Set the shipping destination of the project.

        Parameters
        ----------
        shipping_dest : str
            Name of the shipping destination location.
        """

        if shipping_dest is None:
            self.shipping_dest = None
        else:
            self.shipping_dest = Location.from_str (shipping_dest)

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
        else:
            self.shipping_org = Location.from_str (shipping_org)

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

    def get_qty(self):
        """ Retrieve the quantity of the transportation link.

            Returns
            -------
            float
                The quantity of the transportation link.
        """

        return self.qty
    
    def get_mode_domestic(self):
        """ Retrieve the domestic transportation mode of the transportation link.

            Returns
            -------
            TransportMode obj.
                The domestic transportation mode of the transportation link.
        """

        return self.mode_domestic_obj   
    
    def get_mode_foreign(self):
        """ Retrieve the foreign transportation mode of the transportation link.

            Returns
            -------
            TransportMode obj.
                The foreign transportation mode of the transportation link.
        """

        return self.mode_foreign_obj

    def get_shipping_dest(self):
        """
        Retrieve the shipping destination of the project.

        Returns
        -------
        str
            Name of the shipping destination location.
        """
        return self.shipping_dest

    def get_shipping_org(self):
        """
        Retrieve the shipping origin of the project.

        Returns
        -------
        str
            Name of the shipping origin location.
        """
        return self.shipping_org
    
    def get_dist_unit(self):
        """ Retrieve the distance unit of the transportation link.

            Returns
            -------
            str
                The distance unit of the transportation link.
        """

        return self.dist_unit

    def get_return_trip_factor(self):   
        """ Retrieve the return trip factor of the transportation link.

            Returns
            -------
            float
                The return trip factor of the transportation link.
        """

        return self.return_trip_factor
    
    def get_travel_dist(self):
        """ Retrieve the travel distance of the transportation link.

            Returns
            -------
            float or str
                The travel distance of the transportation link.
        """

        return self.travel_dist
    
    def get_link_distances(self):
        """ Retrieve the link distances of the transportation link.

            Returns
            -------
            dict
                A dictionary containing the domestic and foreign distances.
        """

        return self.link_distances

    def get_impact_domestic(self):
        """ Retrieve the domestic impact of the transportation link.

            Returns
            -------
            Impacts obj.
                The domestic impact of the transportation link.
        """

        return self.impact_domestic

    def get_impact_foreign(self):
        """ Retrieve the foreign impact of the transportation link.

            Returns
            -------
            Impacts obj.
                The foreign impact of the transportation link.
        """

        return self.impact_foreign

    def get_impact_total(self):
        """ Retrieve the total impact of the transportation link.

            Returns
            -------
            Impacts obj.
                The total impact of the transportation link.
        """

        return self.impact_total  


    def get_mode_domestic_name(self):
        """ Retrieve the name of the domestic transportation mode.

            Returns
            -------
            str
                The name of the domestic transportation mode.
        """

        return self.mode_domestic_name
    
    def get_mode_foreign_name(self):
        """ Retrieve the name of the foreign transportation mode.

            Returns
            -------
            str
                The name of the foreign transportation mode.
        """

        return self.mode_foreign_name

    def get_mode_domestic_fuel_type(self):
        """ Retrieve the fuel type of the domestic transportation mode.

            Returns
            -------
            str
                The fuel type of the domestic transportation mode.
        """

        return self.mode_domestic_fuel_type

    def get_mode_domestic_efficiency(self):
        """ Retrieve the efficiency of the domestic transportation mode.

            Returns
            -------
            str
                The efficiency of the domestic transportation mode.
        """

        return self.mode_domestic_efficiency

    def get_mode_foreign_fuel_type(self):   
        """ Retrieve the fuel type of the foreign transportation mode.

            Returns
            -------
            str
                The fuel type of the foreign transportation mode.
        """

        return self.mode_foreign_fuel_type
    
    def get_mode_foreign_efficiency(self):
        """ Retrieve the efficiency of the foreign transportation mode.

            Returns
            -------
            str
                The efficiency of the foreign transportation mode.
        """

        return self.mode_foreign_efficiency

    def get_electricity_consumption(self):
        """ Retrieve the electricity consumption of the transportation link.

            Returns
            -------
            float
                The electricity consumption of the transportation link.
        """

        return self.electricity_consumption

    # ================================
    # Model Methods
    # ================================


    def compute_impact(self):
        """ compute the impaact of the transportation link.

            Returns
            -------
            dict
                A dictionary of impacts for each category.
        """

        if isinstance(self.travel_dist, float) or isinstance(self.travel_dist, int): 
            
            if self.return_trip_factor is None:
                dist = self.travel_dist
                if self.travel_dist_unit == "mi":
                    self.return_trip_factor = 1.5 if dist < 500 else 1
                elif self.travel_dist_unit == "km":
                    self.return_trip_factor = 1.5 if dist < 805 else 1

            if self.mode_domestic_obj is not None:
                domestic_impact = self.mode_domestic_obj.get_impact()
                self.impact_domestic = domestic_impact * self.qty * self.travel_dist * self.return_trip_factor * self.unit_conversion
                self.link_distances ["Domestic"] = self.travel_dist
            
            if self.mode_foreign_obj is not None:
                foreign_impact = self.mode_foreign_obj.get_impact()
                self.impact_foreign = foreign_impact * self.qty * self.travel_dist *  self.unit_conversion
                self.link_distances ["Foreign"] = self.travel_dist

        else:
            Scenario_link = Scenario.new( self ,self.travel_dist, self.material, self.mode_foreign_obj, self.mode_domestic_obj, self.shipping_dest, self.shipping_org)
            self.link_distances["Domestic"],self.link_distances["Foreign"]  = Scenario_link.get_distances()
            
            self.mode_domestic_obj = Scenario_link.get_mode_domestic()
            self.mode_foreign_obj = Scenario_link.get_mode_foreign()


            if self.return_trip_factor is None:

                dist = self.link_distances["Domestic"]

                if self.travel_dist_unit == "mi":
                    self.return_trip_factor = 1.5 if dist < 500 else 1
                elif self.travel_dist_unit == "km":
                    self.return_trip_factor = 1.5 if dist < 805 else 1

            try:
                self.impact_domestic = Scenario_link.get_impact_domestic()
                self.impact_domestic = self.impact_domestic * self.qty * self.return_trip_factor * self.unit_conversion
            except:
                self.impact_domestic = self.mode_foreign_obj.get_impact() * 0

            try:
                self.impact_foreign = Scenario_link.get_foreign_impact()
                self.impact_foreign = self.impact_foreign * self.qty * self.unit_conversion
            except:
                self.impact_foreign = self.mode_domestic_obj.get_impact() * 0


            self.electricity_consumption = self.mode_domestic_obj.get_electricity_consumption()* self.link_distances["Domestic"]* self.return_trip_factor
