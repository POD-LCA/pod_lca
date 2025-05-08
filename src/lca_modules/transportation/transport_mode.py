from lca_modules.impacts.impacts import Impacts
from utilities.data_imports.data_importer import Data_Importer

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

# TODO: Make this mappings JSON and set the file paths in config
cfs_mapping = {"Truck": [3, 4, 5] , "Rail": [6], "Barge": [7, 8, 9, 10, 101 ], "Air": [11]}
faf_mapping = {"Truck": 1 , "Rail": 2, "Barge": 3, "Ocean": 3, "Air": 4}

class TransportMode:
    """ 
    Initialize the TransportMode object.

    Attributes
    ----------
    name: str
        the name of the transportation mode (e.g., 'Truck', 'Rail').
    efficiency: int
        the efficiency level (e.g., 1, 2, 3).
    project: Project Obj.
        an object representing the project.
    impacts: Impacts Obj
        Impacts of the transportation mode.
    limitations: list
        A list of limitations for the transportation mode.
    faf_mode: int
        the FAF mode code for the transportation mode.
    """
    def __init__(self, mode_name, efficiency, project, feul_type = "Regular"):
        self.mode_name = mode_name
        self.efficiency = efficiency
        self.project = project
        self.feul_type = feul_type
        self.impacts = Impacts.from_parent(self)
        self.limitations = []
        self.faf_mode = None
        self.cfs_mode = None
        self.set_impact() # TODO: Remove method from init. This can be avoided by having a constructor method

    # ========================
    # Setters
    # ========================
    def set_impact(self):
        """ Retrieve and update the environmental impacts for the given transportation mode and efficiency.
        """
        # TODO: For consistancy, consider importing via an ImpactDatabase object
        emission_data = Data_Importer.csv_to_pandas(r"data\transportation_podlca_emission.csv")

        filtered_data = emission_data[(emission_data["mode_name"] == self.mode_name) &
                                       (emission_data["eff"] == self.efficiency) & (emission_data["feul"] == self.feul_type) ]

        # If data is found, update the impacts
        if not filtered_data.empty:
            row = filtered_data.iloc[0]  # Get the first (and only) matching row
            impacts = {
                "GWP": row["GWP"],
                "AP": row["AP"],
                "EP": row["EP"],
                "ODP": row["ODP"],
                "POCP": row["POCP"]
            }

            self.impacts.update_qty(impacts)
        else:
            print(f"No matching data found for mode: {self.mode_name} and efficiency: {self.efficiency}.")

    # ========================
    # Setters
    # ========================
    def get_name (self):
        """ Retrieve the name of the transportation mode.
        """
        return self.mode_name

    def get_efficiency (self):
        """ Retrieve the efficiency of the transportation mode.
        """
        return self.efficiency

    def get_impacts (self):
        """ Retrieve the impacts of the transportation mode.
        """
        return self.impacts

    def get_faf_mode (self):
        """ Retrieve the FAF mode code of the transportation mode.
        """
        faf_mapping = {"Truck": 1 , "Rail": 2, "Barge": 3, "Ocean": 3, "Air": 4} #TODO: as suggested above, make this mappings JSON and set the file paths in config
        if self.mode_name in faf_mapping:
            self.faf_mode = faf_mapping[self.mode_name]

        return self.faf_mode

    def get_cfs_mode (self):
        """ Retrieve the CFS mode code of the transportation mode.
        """
        cfs_mapping = {"Truck": [3, 4, 5] , "Rail": [6], "Barge": [7, 8, 9, 10, 101 ], "Air": [11]} #TODO: as suggested above, make this mappings JSON and set the file paths in config
        if self.mode_name in cfs_mapping:
            self.cfs_mode = cfs_mapping[self.mode_name]

        return self.cfs_mode

    def get_fuel_type (self):
        """ Retrieve the fuel type of the transportation mode.
        """
        return self.feul_type


if __name__ == '__main__':
    pass
