
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from ..transportation import Scenario
from ..transportation import TransportMode


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
    mode_name : str.
        transportation mode (ex: truck, rail).
    mode_dms_name : str.
        transportation domestic mode (ex: truck, rail).
    efficiency : int.
        transportation mode efficiency (ex: (1)high, (2)medium, (3)low).
    efficiency_dms : int.
        Domestic transportation mode efficiency (ex: (1)high, (2)medium, (3)low).
    """    
    def __init__(self, project, material, qty, travel_dist, return_trip_factor, dist_unit, mode_name, feul_type, mode_dms_name, efficiency, efficiency_dms):

        self.project = project  
        self.material = material
        self.qty = qty
        self.travel_dist = travel_dist
        self.return_trip_factor = return_trip_factor
        self.dist_unit = dist_unit
        self.efficiency = efficiency
        self.efficiency_dms = efficiency_dms
        self.mode = None if mode_name is None else TransportMode(mode_name, efficiency, project, feul_type)
        self.mode_domestic = None if mode_dms_name is None else TransportMode(mode_dms_name, efficiency_dms, project, feul_type)
        self.unit_conversion = {"km": 1, "mi": 0.621371}[dist_unit] #TODO: Use the unit objects and unit map
        self.link_distances = {"Domestic": 0, "Foreign": 0}
        self.impact = None

        # TODO: create construct method
        # TODO: create corresponding setter methods

    # ========================
    # Getters
    # ========================
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

        return self.efficiency_dms # TODO: What is the difference between efficiency and efficiency_dms

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
            Impact Obj.
                impact of the transportation link.
        """

        return self.impact

    # ========================
    # Methods
    # ========================
    def compute_impact(self):
        """ compute the impaact of the transportation link.

            Returns
            -------
            dict
                A dictionary of impacts for each category. 
        """

        if isinstance(self.travel_dist, (float, int)): 
            
            if self.return_trip_factor is None:
                dist = self.travel_dist
                if self.dist_unit == "mi":
                    self.return_trip_factor = 1.5 if dist < 500 else 1
                elif self.dist_unit == "km":
                    self.return_trip_factor = 1.5 if dist < 805 else 1 # TODO: using units, do the check in either miles or km only, whichever was specified.

            impact = self.mode.get_impacts()
            impact = impact * self.qty * self.travel_dist * self.return_trip_factor * self.unit_conversion
            self.link_distances ["Domestic"] = self.travel_dist
            self.impact = impact # TODO: use compute_impact method to compute the impact and return. Create set_impact method to call the compute method and assign

        else:

            Scenario_link = Scenario(self.project, self.travel_dist, self.material, self.mode, self.mode_domestic)
            self.link_distances["Domestic"],self.link_distances["Foreign"]  = Scenario_link.get_distances()

            if self.return_trip_factor is None:

                dist = self.link_distances["Domestic"] + self.link_distances["Foreign"]

                if self.dist_unit == "mi":
                    self.return_trip_factor = 1.5 if dist < 500 else 1
                elif self.dist_unit == "km":
                    self.return_trip_factor = 1.5 if dist < 805 else 1 # TODO: using units, do the check in either miles or km only, whichever was specified.

            impact = Scenario_link.get_scenario_impact() 
            impact = impact * self.qty * self.return_trip_factor * self.unit_conversion
            self.impact = impact # TODO: use compute_impact method to compute the impact and return. Create set_impact method to call the compute method and assign

        # TODO: Not set to return anything. Docstring says returns a dictionary

if __name__ == '__main__':
    pass
