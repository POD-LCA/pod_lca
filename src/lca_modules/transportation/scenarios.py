import pandas as pd
import numpy as np
from lca_modules.transportation.transport_mode import TransportMode
from geopy.distance import geodesic
from lca_modules.location.data import CFS_DATA_PATH
from lca_modules.location.location import Location

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"



class Scenario:
    
    def __init__(self, project ,scenario, material, mode, mode_domestic):

        """
        Scenario object compute the impact of transportation based on different scenarios.

        Attributes
        ----------

        project : obj.
            Refers to the main project.

        scenario : str.
            name of the transportation scenario.

        material : str.
            name of the material.

        mode : obj.
            Refers to the TransportMode object.

        mode : obj.
            Refers to the TransportMode object.

        """

        self.scenario = scenario
        self.project = project
        self.material = material
        self.distances = {"Local": 0, "Regional": 0, "Regional_c": 0, "National": 0, "NA": 0, "Global": 0, "None": 0}
        self.mode = mode
        self.mode_domestic = mode_domestic
        self.shipping_dest = project.get_shipping_dest()
        self.shipping_org = project.get_shipping_org()
        self.local = None
        self.regional = None
        self.regional_c = None
        self.national = None
        self.na = None
        self.global_ = None
        self.none = None

        self.pre_global_processing()
        self.pre_us_processing()
        

    def get_sctg(self, digit):
        """
        Get the SCTG code based on the material category.

        Parameters:
        - digit: int, the digit of the SCTG code to retrieve.

        Returns:
        - int, the SCTG code.
        """
        data_material = self.project.get_subdataset("EC3 Category to CFS Group mapping")
        sctg = data_material[data_material["material"] == self.material].iloc[0, 1]
        sctg = int(str(sctg)[:digit])

        return sctg
    
    
    def pre_us_processing(self):
        """
        process the data for the US scenarios.

        """

        cfs = self.project.get_subdataset("cfs_2017_cleaned")
        emission = self.project.get_subdataset("Emission")
        sctg = self.get_sctg(2)
        cfs = cfs[cfs["SCTG"] == str(sctg)].copy()
        df = pd.read_csv(CFS_DATA_PATH)

        if self.mode is not None:
            cfs_c = cfs.copy()
 
            cfs = cfs[cfs["MODE"].isin(self.mode.get_cfs_mode()[1] [self.mode.get_name()])]
            if cfs.empty:
                cfs = cfs_c
                print ("No mode found in cfs, value shows the avarage distance of the modes")
        else:
            self.mode = TransportMode("Truck", 1, self.project)
        
        if self.shipping_dest is not None:
            cfs_c = cfs.copy()
            cfs = cfs[cfs["DEST_STATE"] == self.shipping_dest.get_cfs_area()]
            if cfs.empty:
                cfs = cfs_c
                print ("No location for destination found in cfs, The value shows the avrage of the US")

        if self.shipping_org is not None:
            cfs_c = cfs.copy()
            cfs_cc = cfs.copy()
            cfs = cfs[cfs["ORIG_STATE"] == self.shipping_org.get_cfs_area()]

            if cfs.empty:
                cfs_list = cfs_c["ORIG_STATE"].tolist()
                cfs_lat = []
                cfs_lon = []

                for state in cfs_list:
                    lat = df[df["Code"] == state]["lat"].values
                    lon = df[df["Code"] == state]["lon"].values

                    if len(lat) > 0 and len(lon) > 0:
                        cfs_lat.append(lat[0])
                        cfs_lon.append(lon[0])

                coords = list(zip(cfs_lat, cfs_lon))
                origin_to_dest = []
                
                for coord in coords:
                    distance = geodesic(coord, self.shipping_org.get_cordinates()).km
                    origin_to_dest.append(distance)

                cfs_dist = dict(zip(cfs_list, origin_to_dest))
                sorted_cfs_dist = dict(sorted(cfs_dist.items(), key=lambda item: item[1]))

                while cfs.empty:
                    closest_state = list(sorted_cfs_dist.keys())[0]
                    cfs = cfs_cc[cfs_cc["ORIG_STATE"] == closest_state]
                    del sorted_cfs_dist[closest_state]
                    print (f"No location for origin found in cfs, The value shows the closest shipping to the selected origin {closest_state}")

            if cfs.empty:
                cfs = cfs_cc
                print ("No location for origin found in cfs, The value shows the avrage of the US")


        cfs_mapping = self.mode.get_cfs_mode()[1]
        reverse_mapping = {mode: key for key, modes in cfs_mapping.items() for mode in modes}
        cfs = cfs.copy()
        cfs["mode_name"] = cfs["MODE"].map(reverse_mapping)
        merged_data = pd.merge(cfs, emission, on="mode_name", how="inner")

        merged_data = merged_data[ merged_data["eff"] == self.mode.get_efficiency()]
        merged_data.iloc[:, -5:] *= merged_data["SHIPMT_DIST_ROUTED"].values[:, None]

        self.local = merged_data[merged_data["quartile"] == "Q1"].iloc[:, -5:].mean().to_dict()
        self.distances["Local"] = merged_data[merged_data["quartile"] == "Q1"]["SHIPMT_DIST_ROUTED"].mean()

        self.regional = merged_data[merged_data["quartile"] == "Q2"].iloc[:, -5:].mean().to_dict()
        self.distances["Regional"] = merged_data[merged_data["quartile"] == "Q2"]["SHIPMT_DIST_ROUTED"].mean()

        self.regional_c = merged_data[merged_data["quartile"] == "Q3"].iloc[:, -5:].mean().to_dict()
        self.distances["Regional_c"] = merged_data[merged_data["quartile"] == "Q3"]["SHIPMT_DIST_ROUTED"].mean()

        self.national = merged_data[merged_data["quartile"] == "Q4"].iloc[:, -5:].mean().to_dict()
        self.distances["National"] = merged_data[merged_data["quartile"] == "Q4"]["SHIPMT_DIST_ROUTED"].mean()

        self.none = merged_data.iloc[:, -5:].mean().to_dict()
        self.distances["None"] = merged_data["SHIPMT_DIST_ROUTED"].mean()
        

    def pre_global_processing (self):
        """
        process the data for the North America and Global scenarios.
        
        """
        emission = self.project.get_subdataset("Emission")
        faf = self.project.get_subdataset("FAF561_cleaned")
        cfaf = self.project.get_subdataset("cfaf_cleaned")
        marine = self.project.get_subdataset("Marine_cleaned")
        sctg = self.get_sctg(2)
        
        faf = faf[faf["sctg2"] == sctg].copy()
        cfaf = cfaf[cfaf["SCTG_2digits"] == sctg].copy()
        

        if self.shipping_dest is not None:
            faf_c = faf.copy()
            marine_c = marine.copy()

            marine_location = self.shipping_dest.us_coast
            location = self.shipping_dest.get_faf_domestic_region()

            marine = marine[marine["Coast"] == marine_location]
            faf = faf[faf["dms_dest"].isin(location)]
            if faf.empty:
                faf = faf_c
                print ("The value shows the avrage of the US")
            
            if marine.empty:
                marine = marine_c
                print ("The value shows the avrage of the US coast")

        if self.shipping_org is not None:
            faf_c = faf.copy()
            marine_c = marine.copy()

            marine_location = self.shipping_org.get_marine_region()
            location = self.shipping_org.get_faf_foreign_region()

            marine = marine[marine["Region"] == marine_location]
            faf = faf[faf["fr_orig"] == location]

            if faf.empty:
                faf = faf_c[faf_c [ "fr_orig"].isin([801, 802])]
                print ("The value shows the avrage of Canada and Mexico")

            if marine.empty:
                marine = marine_c
                print ("The value shows the avrage of the marine region")

        if self.mode_domestic is not None:
            faf_c = faf.copy()
            faf = faf[faf["dms_mode"] == self.mode_domestic.get_faf_mode()]
            
            if faf.empty:
                faf = faf_c
                print ("No domestic mode found in faf, value shows the avarage distance of the modes")

        if self.mode is not None:
            faf_c = faf.copy()
            faf = faf[faf["fr_inmode"] == self.mode.get_faf_mode()]
            
            if faf.empty:
                faf = faf_c
                print ("No mode found in faf, value shows the avarage distance of the mode")
        

            if self.mode.get_name() == "Truck":
                
                distance = faf["avr_dom_dist_km"].mean()
                total_impacts = {}
                
                domestic_total = self.mode.get_impacts() * distance
                foreign_total = self.mode.get_impacts() * 200
                total_impact = domestic_total + foreign_total

                # for key, value in self.mode.get_impacts().items():
                #     domestic_total = value * distance
                #     foreign_total = value * 200  
                #     total_impacts[key] = domestic_total + foreign_total
                
                self.na = total_impacts
                self.distances["NA"] = distance
                self.global_ = total_impacts
                self.distances["Global"] = distance


            if self.mode.get_name() == "Rail":
                distance = cfaf["Average_Distance_per_Shipment"].mean()
                
                total_impacts = {}
                
                for key, value in self.mode.get_impacts().items():
                    total_impacts[key] = value * distance
                
                self.na = total_impacts
                self.distances["NA"] = distance
                self.global_ = total_impacts
                self.distances["Global"] = distance


            if self.mode.get_name() == "Barge" or "Ocean":

                domestic_total = {}
                foreign_total = {}

                if self.mode_domestic is not None:
                    distance = faf["avr_dom_dist_km"].mean()
                    for key, value in self.mode_domestic.get_impacts().items():
                        domestic_total[key] = value * distance

                else:
                    faf = faf[faf["dms_mode"] == 1] #Truck as default
                    distance = faf["avr_dom_dist_km"].mean()
                    domestic_total = TransportMode ("Truck", 1, self.project).get_impacts() * distance
                    
                marine_dis = marine["Distance_km"].mean()
                foreign_total = self.mode.get_impacts() * marine_dis

                self.global_ = foreign_total + domestic_total
                self.distances["Global"] = distance + marine_dis
                self.distances["NA"] = distance + marine_dis
                self.na = self.global_
                #self.none = self.global_


            if self.mode.get_name() == "Air":

                if self.shipping_dest is not None:
                    dest_location = self.shipping_dest.get_cordinates()
                else:
                    dest_location = (39.8283, -98.5795) #USA middle

                if self.shipping_org is not None:
                    org_location = self.shipping_org.get_cordinates()
                    distance = geodesic(org_location, dest_location).km

                else:
                    major_cities = faf["fr_orig"].mode()[0]
                    distance = faf[faf["fr_orig"] == major_cities]["avr_dom_dist_km"].mean()

                total_impacts = self.mode.get_impacts() * distance

                self.global_ = total_impacts
                self.distances["Global"] = distance
                self.distances["NA"] = distance
                self.na = self.global_

        else:

            mode_na = emission[emission["eff"] == self.project.get_links()[0].get_efficiency()].iloc[:, -5:].mean().to_dict()
            mode_global = emission[emission["eff"] == self.project.get_links()[0].get_efficiency()].iloc[:, -5:].mean().to_dict()

            if self.shipping_dest is None:
                shipping_dest_coords = (39.8283, -98.5795)  # Default location (center of the U.S.)
            else:
                shipping_dest_coords = self.shipping_dest.get_cordinates()

            # Calculate the distances
            distance_na = (
                geodesic(shipping_dest_coords, Location.from_str("Mexico").get_cordinates()).km +
                geodesic(shipping_dest_coords, Location.from_str("Canada").get_cordinates()).km
            ) / 2

            distance_global = (marine["Distance_km"].mean() + cfaf["Average_Distance_per_Shipment"].mean() + faf["avr_dom_dist_km"].mean()) / 3

            for key in mode_na:
                mode_na[key] *= distance_na
            
            for key in mode_global:
                mode_global[key] *= distance_global

            self.na = mode_na
            self.distances["NA"] = distance_na
            self.distances["Global"] = distance_global
            self.global_ = mode_global

    def scenario_impact (self):

        """
        return the impact of the transportation based on the scenario.
        
        """
        if self.scenario == "Local":
            return self.local

        if self.scenario == "Regional":
            return self.regional

        if self.scenario == "Regional_c":
            return self.regional_c

        if self.scenario == "National":
            return self.national

        if self.scenario == "NA":
            return self.na

        if self.scenario == "Global":
            return self.global_

        if self.scenario == "None":
            return self.none

    def get_distances (self):
    
        """
        return the distances of the transportation based on the scenario.
        
        """
        return self.distances


    def get_local_impact (self):

        """
        return the impact of the transportation based on the local scenario.
        
        """
        return self.local

    def get_regional_impact (self):
        
        """
        return the impact of the transportation based on the regional scenario.
        
        """
        return self.regional

    def get_regional_c_impact (self):

        """
        return the impact of the transportation based on the regional_c scenario.
        
        """
        return self.regional_c

    def get_national_impact (self):

        """
        return the impact of the transportation based on the national scenario.
        
        """
        return self.national

    def get_na_impact (self):

        """
        return the impact of the transportation based on the north america scenario.
        
        """
        return self.na

    def get_global_impact (self):

        """
        return the impact of the transportation based on the global scenario.
        
        """
        return self.global_


if __name__ == '__main__':

    pass