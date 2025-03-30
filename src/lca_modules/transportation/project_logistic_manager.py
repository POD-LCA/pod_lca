import os
import pandas as pd
from lca_modules.transportation.logistics_link import Link
from lca_modules.transportation.scenarios import Scenario
from lca_modules.location.location import Location
import matplotlib.pyplot as plt
from lca_modules.impacts.impacts import Impacts


__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"



class ProjectLogisticManager:

    def __init__(self, name, shipping_dest, data_folder, shipping_org):

        """
        ProjectLogisticManager class which maintains the links of transportation.

        Attributes
        ----------
        name : int.
            name of the project.
        shipping_dest : str.
            neme of the shipping destination location.
        data_folder : str.
            path to the data folder.
        shipping_org : str.
            name of the shipping origin location.
        links : list.
            list of links.
        impact : obj.
            impact object.
        subdataset : dict.
            dictionary of subdatasets.
        """

        self.name = name
        self.shipping_dest = None if shipping_dest is None else Location.from_str (shipping_dest)
        self.data_folder = data_folder
        self.shipping_org = None if shipping_org is None else Location.from_str (shipping_org)
        self.links = []
        self.impacts = Impacts.from_parent(self)
        self.subdataset = {}


    def sub_dataset(self):
        """
        Read the subdatasets from the data folder.

        """
        for file in os.listdir(self.data_folder):
            file_path = os.path.join(self.data_folder, file)
            if file.endswith(".csv"):
                try:
                    df = pd.read_csv(file_path)
                    dataset_name = os.path.splitext(file)[0]
                    self.subdataset[dataset_name] = df
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
            elif file.endswith((".xlsx", ".xls")):
                try:
                    df = pd.ExcelFile(file_path)
                    dataset_name = os.path.splitext(file)[0]
                    self.subdataset[dataset_name] = df
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    def get_subdataset(self, sub_dataset):
        """
        Retrieve the subdataset.
        """

        if not self.subdataset:
            self.sub_dataset()
        return self.subdataset.get(sub_dataset)

    def create_link(self, material, qty, travel_dist, return_trip_factor, dist_unit, mode_name, feul_type, mode_dms_name, efficiency, efficiency_dms):
        """
        Create a link of transportation for the project.
        """
        link = Link(self, material, qty, travel_dist, return_trip_factor, dist_unit, mode_name, feul_type, mode_dms_name, efficiency, efficiency_dms)
        self.links.append(link)

        self.impacts.update_impact_qty(link.compute_impact().get_impact_dict())

            
    @staticmethod
    def merge_impacts(impact1, impact2):
        """
        Merge the impacts of the links.
        """
        for key in impact1:
            impact1[key] += impact2.get(key, 0)
        return impact1

    def get_name(self):
        """
        Retrieve the name of the project.
        """
        return self.name


    def get_impacts(self):
        """ Retrieve the impacts of the Transportation.

            Returns
            -------
            Impacts Obj.
                Impacts of the Transportation.

        """

        return self.impacts

    def get_links (self):
        """
        Retrieve the links of the project.
        """
        return self.links

    def get_shipping_dest (self):
        """
        Retrieve the shipping destination of the project.
        """
        return self.shipping_dest

    def get_shipping_org (self):
        """
        Retrieve the shipping origin of the project.
        """

        return self.shipping_org

    def get_scenario_distance (self, link):
        """
        Retrieve the scenario distance of the project.
        """
        return self.links[link].get_scenario_distances()






