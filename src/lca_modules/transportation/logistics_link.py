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
    
    def __init__(self, project, material, qty, travel_dist, return_trip_factor, dist_unit, mode_name, mode_dms_name, efficiency, efficiency_dms):
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

        travel_dist : float.
            transportation distance.

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
        self.qty = qty
        self.travel_dist = travel_dist
        self.return_trip_factor = return_trip_factor
        self.dist_unit = dist_unit
        self.mode = None if mode_name is None else TransportMode(mode_name, efficiency, project)
        self.mode_domestic = None if mode_dms_name is None else TransportMode(mode_dms_name, efficiency_dms, project)
        self.unit_conversion = 1.60934

    def compute_impact(self):
        """ compute the impaact of the transportation link.

            Returns
            -------
            dict
                A dictionary of impacts for each category.
        """
        if isinstance(self.travel_dist, float) or isinstance(self.travel_dist, int): 

            impact = self.mode.set_impact()
            impact = self.mode.get_impacts()

            for key in impact:
                impact[key] *= self.qty * self.travel_dist * self.return_trip_factor
            return impact

        else:
            
            impact = Scenario(self.project, self.travel_dist, self.material, self.mode, self.mode_domestic).scenario_impact() 

            for key in impact:
                impact[key] *= self.qty * self.return_trip_factor * self.unit_conversion

            return impact


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

    def get_travel_dist (self):
        """ 
        Retrieve the transportation distance of the transportation link.

            Returns
            -------
            float
                transportation distance of the transportation link.
        """

        return self.travel_dist