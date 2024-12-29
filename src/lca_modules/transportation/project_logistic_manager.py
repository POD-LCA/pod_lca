import os
import pandas as pd
from lca_modules.transportation.logistics_link import Link
#from lca_modules.transportation.scenarios import Scenario


__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"



class ProjectLogisticManager:

    def __init__(self, name, location, data_folder):

        self.name = name
        self.location = location
        self.data_folder = data_folder
        self.links = []
        self.impact = {"GWP": 0.0, "AP": 0.0, "EP": 0.0, "ODP": 0.0, "SFP": 0.0}
        self.subdataset = {}

    def sub_dataset(self):
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

        if not self.subdataset:
            self.sub_dataset()
        return self.subdataset.get(sub_dataset)

    def create_link(self, material, qty, travel_dist, return_trip_factor, dist_unit, mode_name, efficiency):
        
        link = Link(self, material, qty, travel_dist, return_trip_factor, dist_unit, mode_name, efficiency)
        self.links.append(link)
        self.impact = self.merge_impacts(self.impact, link.compute_impact())
        

    @staticmethod
    def merge_impacts(impact1, impact2):

        for key in impact1:
            impact1[key] += impact2.get(key, 0)
        return impact1

    def get_impact(self):

        return self.impact

    def get_links (self):

        return self.links

    def get_location (self):

        return self.location



