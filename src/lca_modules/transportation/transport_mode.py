from lca_modules.impacts.impacts import Impacts
from utilities.data_imports.data_importer import Data_Importer

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

cfs_mapping = {"Truck": [3, 4, 5] , "Rail": [6], "Barge": [7, 8, 9, 10, 101 ], "Air": [11]}
faf_mapping = {"Truck": 1 , "Rail": 2, "Barge": 3, "Ocean": 3, "Air": 4}

class TransportMode:

    """
    Initialize the TransportMode object.

    Parameters:
    - name: str, the name of the transportation mode (e.g., 'Truck', 'Rail').
    - efficiency: int, the efficiency level (e.g., 1, 2, 3).
    - project: an object representing the project.
    - impacts: dict, a dictionary containing the environmental impacts of the transportation mode.
    - limitations: list, a list of limitations for the transportation mode.
    - faf_mode: int, the FAF mode code for the transportation mode.
    - set_impact: method, a method to retrieve and update the environmental impacts for the given transportation mode and efficiency.

    """

    def __init__(self):

        self.mode_name = None
        self.efficiency = None
        self.fuel_type = None
        self.impact = None
        self.electricity_consumption = None
        self.limitations = []
        self.faf_mode = None
        self.cfs_mode = None


    def __str__(self):
        """
        String representation of the TransportMode object.
        """

        str = "="*75 + "\n" + f"Transportation Mode: {self.get_name()}\n" + "="*75 + "\n"

        return str


    # ================================
    # Constructors
    # ================================


    @classmethod
    def new(cls, mode_name, efficiency = "Median", fuel_type = "Regular"):
        
        """ Create a new transportation mode.

        Parameters:
        - mode_name: str, the name of the transportation mode (e.g., 'Truck', 'Rail').
        - efficiency: int, the efficiency level (e.g., 1, 2, 3).
        - project: an object representing the project.
        - fuel_type: str, the type of fuel used (default is "Regular").

        Returns:
        - TransportMode object.
        """
        
        mode = cls()
        mode.set_name(mode_name)
        mode.set_efficiency(efficiency)
        mode.set_fuel_type(fuel_type)
        mode.set_impact()
        mode.set_faf_mode()
        mode.set_cfs_mode()

        return mode


    # ================================
    # Setters
    # ================================

    def set_name(self, mode_name:(str)):
        """
        Set the name of the transportation mode.

        Parameters:
        - mode_name: str, the name of the transportation mode.
        """
        self.mode_name = mode_name

        return self

    def set_efficiency(self, efficiency:(str)):
        """
        Set the efficiency of the transportation mode.

        Parameters:
        - efficiency: str, the efficiency level (e.g., 'Low', 'Medium', 'High').
        """
        self.efficiency = efficiency

        return self

    def set_fuel_type(self, fuel_type:(str)):
        """
        Set the fuel type of the transportation mode.

        Parameters:
        - fuel_type: str, the type of fuel used (e.g., 'Regular', 'Premium').
        """
        self.fuel_type = fuel_type

        return self

    def set_faf_mode(self):
        """
        Set the FAF mode code for the transportation mode.
        """
        if self.mode_name in faf_mapping:
            self.faf_mode = faf_mapping[self.mode_name]
        else:
            print(f"Warning: FAF mode mapping not found for {self.mode_name}.")

        return self

    def set_cfs_mode(self):
        """
        Set the CFS mode code for the transportation mode.
        """
        if self.mode_name in cfs_mapping:
            self.cfs_mode = cfs_mapping[self.mode_name]
        else:
            print(f"Warning: CFS mode mapping not found for {self.mode_name}.")

        return self

    def set_impact(self):
        """
        Retrieve and update the environmental impacts for the given transportation mode and efficiency.
        """
        #TODO: create transprtation database
        emission_data = Data_Importer.import_as_pandas(r"data\transportation_podlca_emission.csv")
        filtered_data = emission_data[(emission_data["mode_name"] == self.mode_name) &
            (emission_data["eff"] == self.efficiency) & (emission_data["fuel"] == self.fuel_type) ]

        self.impact = Impacts.from_parent(self)
        # If data is found, update the impacts
        if not filtered_data.empty:
            row = filtered_data.iloc[0]  # Get the first (and only) matching row

            self.electricity_consumption = row["Electricity consumtion (kWh)"]

            impacts = {
                "GWP": row["GWP"],
                "AP": row["AP"],
                "EP": row["EP"],
                "ODP": row["ODP"],
                "SFP": row["SFP"]
            }

            self.impact.update_impact_qty(impacts)
        else:

            print(f"No matching data found for mode: {self.mode_name} and efficiency: {self.efficiency}.")

    # ================================
    # Getters
    # ================================


    def get_name (self):
        """
        Retrieve the name of the transportation mode.
        """
        return self.mode_name

    def get_efficiency (self):
        """
        Retrieve the efficiency of the transportation mode.
        """
        return self.efficiency

    def get_impact (self):
        """
        Retrieve the impacts of the transportation mode.
        """
        return self.impact

    def get_faf_mode (self):
        """
        Retrieve the FAF mode code of the transportation mode.
        """

        return self.faf_mode

    def get_cfs_mode (self):
        """
        Retrieve the CFS mode code of the transportation mode.
        """

        return self.cfs_mode

    def get_fuel_type (self):
        """
        Retrieve the fuel type of the transportation mode.
        """
        return self.fuel_type

    def get_electricity_consumption (self):
        """
        Retrieve the electricity consumption of the transportation mode.
        """
        return self.electricity_consumption

if __name__ == '__main__':

    pass
