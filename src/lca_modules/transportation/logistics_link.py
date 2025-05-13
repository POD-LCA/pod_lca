import os
import pandas as pd
from lca_modules.transportation.scenarios import Scenario
from lca_modules.transportation.transport_mode import TransportMode

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"



class Link:
    
    def __init__(self, project, material, qty, travel_dist, return_trip_factor, dist_unit, mode_name, feul_type, mode_dms_name, efficiency, efficiency_dms):
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

        mode_name : str.
            transportation mode (ex: truck, rail).

        mode_dms_name : str.
            transportation domestic mode (ex: truck, rail).

        efficiency : int.
            transportation mode efficiency (ex: (1)high, (2)medium, (3)low).

        efficiency_dms : int.
            Domestic transportation mode efficiency (ex: (1)high, (2)medium, (3)low).

        """
        self.project = project  
        self.material = material
        self.qty = 0.0
        self.travel_dist = travel_dist
        self.return_trip_factor = None
        self.dist_unit = dist_unit
        self.efficiency = efficiency
        self.efficiency_dms = efficiency_dms
        self.mode = None if mode_name is None else TransportMode(mode_name, efficiency, project, feul_type)
        self.mode_domestic = None if mode_dms_name is None else TransportMode(mode_dms_name, efficiency_dms, project, feul_type)
        self.unit_conversion = {"km": 1, "mi": 0.621371}[dist_unit]
        self.link_distances = {"Domestic": 0, "Foreign": 0}
        self.impact = None



    # ================================
    # Setters
    # ================================

    def set_qty (self, qty:float):
        """ Set the quantity of the transportation link.

            Parameters
            ----------
            qty : float
                quantity of the transportation link.
        """

        self.qty = qty

    def set_material (self, material:str):
        """ Set the material name of the transportation link.

            Parameters
            ----------
            material : str
                material name of the transportation link.
        """

        self.material = material
    
    def set_travel_dist (self, travel_dist):
        """ Set the travel distance of the transportation link.

            Parameters
            ----------
            travel_dist : float or str
                travel distance of the transportation link.
        """

        self.travel_dist = travel_dist

    def set_return_trip_factor (self, return_trip_factor:float):
        """ Set the return trip factor of the transportation link.

            Parameters
            ----------
            return_trip_factor : float
                return trip factor of the transportation link.
        """

        self.return_trip_factor = return_trip_factor

    def set_mode (self, mode:str):
        """ Set the transportation mode of the transportation link.

            Parameters
            ----------
            mode : str
                transportation mode of the transportation link.
        """



        self.mode = mode
        




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
                if self.dist_unit == "mi":
                    self.return_trip_factor = 1.5 if dist < 500 else 1
                elif self.dist_unit == "km":
                    self.return_trip_factor = 1.5 if dist < 805 else 1

            impact = self.mode.get_impacts()
            impact = impact * self.qty * self.travel_dist * self.return_trip_factor * self.unit_conversion
            self.link_distances ["Domestic"] = self.travel_dist
            self.impact = impact


        else:

            Scenario_link = Scenario(self.project, self.travel_dist, self.material, self.mode, self.mode_domestic)
            self.link_distances["Domestic"],self.link_distances["Foreign"]  = Scenario_link.get_distances()

            if self.return_trip_factor is None:

                dist = self.link_distances["Domestic"] + self.link_distances["Foreign"]

                if self.dist_unit == "mi":
                    self.return_trip_factor = 1.5 if dist < 500 else 1
                elif self.dist_unit == "km":
                    self.return_trip_factor = 1.5 if dist < 805 else 1

            impact = Scenario_link.get_scenario_impact() 
            impact = impact * self.qty * self.return_trip_factor * self.unit_conversion
            self.impact = impact


    def get_qty (self):
        """ Retrieve the quantity of the transportation link.

            Returns
            -------
            float
                quantity of the transportation link.
        """
        return self.qty

    def get_material (self):
        """ Retrieve the material name of the transportation link.

            Returns
            -------
            str
                material name of the transportation link.
        """

        return self.material

    def get_mode (self):
        """ Retrieve the transportation mode of the transportation link.

            Returns
            -------
            str
                transportation mode of the transportation link.
        """

        return self.mode

    def get_efficiency (self):
        """ Retrieve the transportation efficiency of the transportation link.

            Returns
            -------
            int
                transportation efficiency of the transportation link.
        """

        return self.efficiency

    def get_efficiency_dms (self):
        """ Retrieve the transportation domestic efficiency of the transportation link.

            Returns
            -------
            int
                transportation domestic efficiency of the transportation link.
        """

        return self.efficiency_dms

    def get_return_trip_factor (self):
        """ Retrieve the return trip factor of the transportation link.

            Returns
            -------
            float
                return trip factor of the transportation link.
        """

        return self.return_trip_factor

    def get_travel_dist (self):
        """ Retrieve the travel distance of the transportation link.

            Returns
            -------
            float
                travel distance of the transportation link.
        """

        return self.link_distances
    
    def get_impact (self):
        """ Retrieve the impact of the transportation link.

            Returns
            -------
            object
                impact of the transportation link.
        """

        return self.impact

