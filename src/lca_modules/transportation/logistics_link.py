import os
import pandas as pd
from lca_modules.transportation.scenarios import Scenario


__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"



class Link:
    
    def __init__(self, project, material, qty, travel_dist, return_trip_factor, dist_unit, mode, eff):
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

        mode : str.
            transportation mode (ex: truck, rail).

        eff : str.
            transportation mode efficiency (ex: high, medium).

        shipping_org : str.
            origin of the transportation.

        """
        self.project = project  # Pass a Project_logestic_manager instance
        self.material = material
        self.qty = qty
        self.travel_dist = travel_dist
        self.return_trip_factor = return_trip_factor
        self.dist_unit = dist_unit
        self.mode = mode
        self.eff = eff
        self.shipping_org = None


    def compute_impact(self):
        """ 
        compute the impaact of the transportation link.

            Returns
            -------
            dict
                A dictionary of impacts for each category.
        """
        if isinstance(self.travel_dist, float): 

            dataset = self.project.get_subdataset("Emission")

            if self.mode not in dataset['mode_name'].tolist():
                
                raise ValueError(f"Mode {self.mode} not found in dataset.")
                
            impact = dataset.loc[dataset['mode_name'] == self.mode].iloc[[0], 4:] * self.qty * self.travel_dist * self.return_trip_factor
            impact = impact.iloc[0].to_dict()
             
            return impact

        else:
            
            impact = Scenario(self.project, self.travel_dist, self.qty, self.material, self.mode).scenario_impact() 

            for value in impact.values():
                value * self.qty * self.return_trip_factor

            return impact


    def get_qty (self):
        """ 
        Retrieve the quantity of the transportation link.

            Returns
            -------
            float
                quantity of the transportation link.
        """
        return self.qty

    def get_material (self):
        """ 
        Retrieve the material name of the transportation link.

            Returns
            -------
            str
                material name of the transportation link.
        """

        return self.material


    def compute_with_location(self):
        # Dummy implementation for demonstration
        # Actual logic for compute_with_location needs to be added
        return {"GWP": 100, "AP": 50}