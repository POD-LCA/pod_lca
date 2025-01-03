__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"



class TransportMode:
    def __init__(self, mode_name, efficiency, project):
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
        self.mode_name = mode_name
        self.efficiency = efficiency
        self.project = project
        self.impacts = {"GWP": 0.0, "AP": 0.0, "EP": 0.0, "ODP": 0.0, "SFP": 0.0}
        self.limitations = []
        self.faf_mode = None
        self.set_impact()

    def set_impact(self):
        """
        Retrieve and update the environmental impacts for the given transportation mode and efficiency.
        """
        # Retrieve emission data from the project
        emission_data = self.project.get_subdataset("Emission")

        # Filter the dataset for the current mode and efficiency
        filtered_data = emission_data[(emission_data["mode_name"] == self.mode_name) &
                                       (emission_data["eff"] == self.efficiency)]

        # If data is found, update the impacts
        if not filtered_data.empty:
            row = filtered_data.iloc[0]  # Get the first (and only) matching row
            self.impacts = {
                "GWP": row["GWP"],
                "AP": row["AP"],
                "EP": row["EP"],
                "ODP": row["ODP"],
                "SFP": row["SFP"]
            }
        else:
            print(f"No matching data found for mode: {self.mode_name} and efficiency: {self.efficiency}.")


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

    def get_impacts (self):
        """
        Retrieve the impacts of the transportation mode.
        """
        return self.impacts

    def get_faf_mode (self):
        """
        Retrieve the FAF mode code of the transportation mode.
        """

        faf_mapping = {"Truck": 1 , "Rail": 2, "Water": 3, "Air": 4}
        if self.mode_name in faf_mapping:
            self.faf_mode = faf_mapping[self.mode_name]

        return self.faf_mode


if __name__ == '__main__':

    from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager

    data_folder = r"C:\Users\mhtaba\Desktop\pod_lca_git\pod_lca\data\transportation_dataset"
    project = ProjectLogisticManager(name="Building A", shipping_dest= None, data_folder=data_folder, shipping_org= None)

    transport = TransportMode ("Truck", 1, project)
    print (transport.get_impacts ())
