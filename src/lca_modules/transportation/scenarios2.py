import pandas as pd
import numpy as np
from lca_modules.transportation.transport_mode import TransportMode
from geopy.distance import geodesic
from lca_modules.location.data import CFS_DATA_PATH, FAF_city_representation, FAF_DOMESTIC_REGION, FAF_DATA
from lca_modules.location.location import Location
from lca_modules.transportation.modes_mapping import cfs_mapping
import json

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
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
            - Scenario can be Local, Regional, Regional_c, National, NA, Global.
            - Local, Regional, Regional_c, National are for US scenarios.
            - NA is for North America scenario.
            - Global is for Global scenario.

            **None** is for the default scenario and shows the average impact of the transportation in the US.

        material : str.
            name of the material.

        mode : obj.
            Refers to the TransportMode object.

        mode_domestic : obj.
            Refers to the TransportMode object.

        """

        self.scenario = scenario
        self.project = project
        self.material = material
        self.sctg = None
        self.domestic_dis = None
        self.foreign_dis = None
        self.total_dis = None
        self.mode = mode
        self.mode_domestic = mode_domestic
        self.shipping_dest = project.get_shipping_dest()
        self.shipping_org = project.get_shipping_org()
        self.scenario_impact = None

        self.set_sctg(material)

        if self.scenario in ["Local", "Regional", "Regional_c", "National", "None", "Known_us"]:
            self.pre_us_processing()
        elif self.scenario in ["NA", "Global", "Known"]:
            self.pre_global_processing()

    def set_sctg(self, material ,digit=2):
        """
        Get the SCTG code based on the material category.

        Parameters:
        - digit: int, the digit of the SCTG code to retrieve.

        Returns:
        - int, the SCTG code.
        """
        data_material = pd.read_csv(r"data\transportation_dataset\EC3 Category to CFS Group mapping.csv")
        
        try:
            if material not in data_material["material"].values:
                raise ValueError("material not found in the dataset")
            sctg = data_material[data_material["material"] == material].iloc[0, 1]
            sctg = int(str(sctg)[:digit])

        except Exception as e:
            print("Error:", e)

        self.sctg = sctg
        return self
    
    def filter_faf(self, sctg=None, destination=None, origin=None, mode=None, domestic_mode=None, scenario=None):
        faf = pd.read_csv(r"data\transportation_dataset\FAF561_cleaned.csv")
        failed = False

        # SCTG
        try:
            if sctg is not None:
                faf = faf[faf["sctg2"] == sctg]
                if faf.empty:
                    raise ValueError("no data for the selected SCTG code in FAF561 dataset")
        except Exception as e:
            print("Error:", e)
            failed = True

        # Destination
        try:
            if destination is not None:
                faf = faf[faf["dms_dest"].isin(destination.get_faf_domestic_region())]
                if faf.empty:
                    raise ValueError("no data for the selected destination in FAF561 dataset")
            
            else:
                major_domes = faf["dms_dest"].mode()[0]
                with open (FAF_DOMESTIC_REGION, "r") as f:
                    faf_domestic_data = json.load(f)
                    for key, value in faf_domestic_data.items():
                        if major_domes in value:
                            major_domes = key
                self.shipping_dest = Location.from_str(major_domes)
                faf = faf[faf["dms_dest"].isin(destination.get_faf_domestic_region())]
                print (f"destination is the most frequent shipping destination {major_domes}")

        except Exception as e:
            print("Error:", e)
            failed = True

        # Origin
        try:
            if origin is not None:
                faf = faf[faf["fr_orig"] == origin.get_faf_foreign_region()]
                if faf.empty:
                    raise ValueError("no data for the selected origin in FAF561 dataset")

            else:
                if scenario == "NA":
                    faf = faf[faf["fr_orig"].isin([801, 802])]
                    faf = faf[faf["fr_orig"] == faf["fr_orig"].mode()[0]]
                    self.shipping_org = Location.from_str(FAF_city_representation[faf["fr_orig"].mode()[0]])
                elif scenario == "Global":
                    faf = faf[faf["fr_orig"].isin([801, 802]) == False]
                    faf = faf[faf["fr_orig"] == faf["fr_orig"].mode()[0]]
                    self.shipping_org = Location.from_str(FAF_city_representation[faf["fr_orig"].mode()[0]])
            
        except Exception as e:
            print("Error:", e)
            failed = True

        # Mode
        try:
            if mode is not None:
                faf = faf[faf["fr_inmode"] == mode.get_faf_mode()]
                if faf.empty:
                    raise ValueError("no data for the selected mode in FAF561 dataset")
            else:

                self.mode = TransportMode("Barge", self.project.get_links()[0].get_efficiency(), self.project)
                faf = faf[faf["fr_inmode"] == self.mode.get_faf_mode()]
                if faf.empty:
                    raise ValueError("no data for Barge as a mode in FAF561 dataset")

        except Exception as e:
            print("Error:", e)
            failed = True
        # Domestic Mode
        try:
            if domestic_mode is not None:
                faf = faf[faf["dms_mode"] == domestic_mode.get_faf_mode()]
                if faf.empty:
                    raise ValueError("no data for the selected domestic mode in FAF561 dataset")
            else:
                self.mode_domestic = TransportMode("Truck", self.project.get_links()[0].get_efficiency(), self.project)
                faf = faf[faf["dms_mode"] == self.mode_domestic.get_faf_mode()]
                if faf.empty:
                    raise ValueError("no data for Truck as a domestic mode in FAF561 dataset")

        except Exception as e:
            print("Error:", e)
            failed = True

        return faf, failed

    def filter_cfaf(self, sctg=None):
        cfaf = pd.read_csv(r"data\transportation_dataset\cfaf_cleaned.csv")
        try:
            if sctg is not None:
                cfaf = cfaf[cfaf["SCTG_2digits"] == sctg]
                if cfaf.empty:
                    raise ValueError("no data for the selected SCTG code in cfaf dataset")
        except Exception as e:
            print("Error:", e)

        return cfaf

    def filter_marine(self, destination=None, origin=None, scenario=None):

        marine = self.project.get_subdataset("Marine_cleaned")
        failed = False
        # Destination
        try:
            if destination is not None:
                marine = marine[marine["Coast"] == destination.us_coast]
                if marine.empty:
                    raise ValueError("no data for the selected destination in Marine dataset")
        except Exception as e:
            print("Error:", e)
            failed = True

        # Origin
        try:
            if origin is not None:
                marine = marine[marine["Region"] == origin.get_marine_region()]
                if marine.empty:
                    raise ValueError("no data for the selected origin in Marine dataset")
                
            else:
                if scenario == "NA":
                    marine = marine[marine["Region"].isin(["Canada", "Mexico"])]
                    marine = marine[marine["Region"] == origin.get_marine_region()]

                elif scenario == "Global":
                    marine = marine[marine["Region"].isin(["Canada", "Mexico"]) == False]
                    marine = marine[marine["Region"] == origin.get_marine_region()]
        
        except Exception as e:
            print("Error:", e)

        return marine, failed

    def filter_cfs(self, sctg=None, destination=None, origin=None, mode=None):
        cfs = pd.read_csv(r"data\transportation_dataset\cfs_2017_cleaned.csv")
        cfs_state_code = pd.read_csv(CFS_DATA_PATH)
        failed = False

        # SCTG
        try:
            if sctg is not None:
                cfs_filtered = cfs[cfs["SCTG"] == sctg]
                if cfs_filtered.empty:
                    raise ValueError("no data for the selected SCTG code in CFS dataset")
                cfs = cfs_filtered
        except Exception as e:
            print("Error:", e)
            failed = True
        
        # Destination
        try:
            if destination is not None:
                cfs_filtered = cfs[cfs["DEST_STATE"] == destination.get_cfs_area()]

                if cfs_filtered.empty:
                    cfs_list = cfs["DEST_STATE"].tolist()
                    cfs_lat = []
                    cfs_lon = []

                    for state in cfs_list:
                        lat = cfs_state_code[cfs_state_code["Code"] == state]["lat"].values
                        lon = cfs_state_code[cfs_state_code["Code"] == state]["lon"].values

                        if len(lat) > 0 and len(lon) > 0:
                            cfs_lat.append(lat[0])
                            cfs_lon.append(lon[0])

                    coords = list(zip(cfs_lat, cfs_lon))
                    dest_to_org = []
                    
                    for coord in coords:
                        distance = geodesic(coord, self.shipping_dest.get_cordinates()).km
                        dest_to_org.append(distance)

                    cfs_dist = dict(zip(cfs_list, dest_to_org))
                    sorted_cfs_dist = dict(sorted(cfs_dist.items(), key=lambda item: item[1]))

                    while cfs_filtered.empty:
                        closest_state = list(sorted_cfs_dist.keys())[0]
                        cfs_filtered = cfs[cfs["DEST_STATE"] == closest_state]
                        del sorted_cfs_dist[closest_state]
                        print(f"No location for destination found in cfs, The value shows the closest shipping to the selected destination {closest_state}")
                
            else:
                cfs = cfs_filtered
        except Exception as e:
            print("Error:", e)
            failed = True
        
        # Origin
        try:
            if origin is not None:
                cfs_filtered = cfs[cfs["ORIG_STATE"] == origin.get_cfs_area()]

            if cfs_filtered.empty:
                cfs_list = cfs["ORIG_STATE"].tolist()
                cfs_lat = []
                cfs_lon = []

                for state in cfs_list:
                    lat = cfs_state_code[cfs_state_code["Code"] == state]["lat"].values
                    lon = cfs_state_code[cfs_state_code["Code"] == state]["lon"].values

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

                while cfs_filtered.empty:
                    closest_state = list(sorted_cfs_dist.keys())[0]
                    cfs_filtered = cfs[cfs["ORIG_STATE"] == closest_state]
                    del sorted_cfs_dist[closest_state]
                    print (f"No location for origin found in cfs, The value shows the closest shipping to the selected origin {closest_state}")
            
            else:
                cfs = cfs_filtered
        except Exception as e:
            print("Error:", e)
            failed = True

        # Mode
        try:
            if mode is not None:
                cfs_filtered = cfs[cfs["MODE"].isin(mode.get_cfs_mode()[1][mode.get_name()])]
                cfs = cfs_filtered if not cfs_filtered.empty else cfs
                if cfs_filtered.empty:
                    print("No data for the selected mode of transportation in CFS dataset, using the most frequent mode of transportation instead.")
            else:
                major_mode = cfs["MODE"].mode()
                cfs = cfs[cfs["MODE"] == major_mode[0]]
                for key, value in cfs_mapping.items():
                    if major_mode[0] in value:
                        self.mode = TransportMode(key, self.project.get_links()[0].get_efficiency(), self.project)
                    print ("Using the most frequent mode of transportation instead.")       
        except Exception as e:
            print("Error:", e)

        return cfs, failed

    def pre_us_processing(self):
        """
        process the data for the US scenarios.

        This function is used to process the data for the US scenarios.

        1. it filters the data based on the shipping destination.
            - if there is no shipping destination it will select the closest shipping destination.
            - if the shipping destination is note defined it will selcet the average shipping destination.

        2. it filters the data based on the shipping origin.
            - if there is no shipping origin it will select the closest shipping origin.
            - if the shipping origin is note defined it will selcet the average shipping origin.
        
        3. it filters the data based on the mode of transportation.
            - if the mode is not selected, it will select the most frequent mode of transportation.

        4. it calculates the distance of the shipping based on the quartiles of the shipping distance.

        """

        
        cfs = self.filter_cfs(self.sctg, self.shipping_dest, self.shipping_org, self.mode)
        if cfs[1] == True:
            print (" An error occurred while filtering the data, please check the data and try again.")
        else:
            cfs = cfs[0]

            quartiles = cfs["SHIPMT_DIST_ROUTED"].quantile([0.25, 0.5, 0.75]).values
            def assign_quartile(x, q1, q2, q3):
                if x <= q1:
                    return 'Q1'
                elif x <= q2:
                    return 'Q2'
                elif x <= q3:
                    return 'Q3'
                else:
                    return 'Q4'
            cfs['quartile'] = cfs["SHIPMT_DIST_ROUTED"].apply(assign_quartile, args=(quartiles[0], quartiles[1], quartiles[2]))
            impact = self.mode.get_impacts()


            if self.scenario == "Local":
                self.total_dis = cfs[cfs["quartile"] == "Q1"]["SHIPMT_DIST_ROUTED"].mean()
                self.scenario_impact = self.total_dis * impact

            elif self.scenario == "Regional":
                self.total_dis = cfs[cfs["quartile"] == "Q2"]["SHIPMT_DIST_ROUTED"].mean()
                self.scenario_impact = self.total_dis * impact
            
            elif self.scenario == "Regional_c":
                self.total_dis = cfs[cfs["quartile"] == "Q3"]["SHIPMT_DIST_ROUTED"].mean()
                self.scenario_impact = self.total_dis * impact
            
            elif self.scenario == "National":
                self.total_dis = cfs[cfs["quartile"] == "Q4"]["SHIPMT_DIST_ROUTED"].mean()
                self.scenario_impact = self.total_dis * impact
            
            elif self.scenario == "None" or self.scenario == "Known_us":
                self.total_dis = cfs["SHIPMT_DIST_ROUTED"].mean()
                self.scenario_impact = self.total_dis * impact
                
    def pre_global_processing (self):
        """
        process the data for the North America and Global scenarios.

        This function is used to process the data for the North America and Global scenarios.


        1. it filters the data based on the shipping destination.
            - if there is no shipping destination it will select the most frequent shipping destination.

        2. it filters the data based on the shipping origin.

        3. it filters the data based on the mode of transportation.
            - if the mode is not defined it will select Barge as the mode of transportation.

        4. it filters the data based on the domestic mode of transportation.
            - if the mode is not defined it will select Truck as the domestic mode of transportation.
            
        """
        faf = self.filter_faf(self.sctg, self.shipping_dest, self.shipping_org, self.mode, self.mode_domestic, self.scenario)

        marine = self.filter_marine(self.shipping_dest, self.shipping_org, self.scenario)
        cfaf = self.filter_cfaf(self.sctg)

        if faf[1] == True:
            print (" An error occurred while filtering the FAF data, please check the data and try again.")
        else:
            faf = faf[0]

        if marine[1] == True:
            print (" An error occurred while filtering the Marine data, please check the data and try again.")
        else:
            marine = marine[0]

        if self.mode.get_name() == "Truck":
            self.domestic_dis = faf["avr_dom_dist_km"].mean()
            self.foreign_dis = 200
            self.total_dis = self.domestic_dis + self.foreign_dis
            self.scenario_impact = total_dis * self.mode.get_impacts()
        
        elif self.mode.get_name() == "Rail":
            self.total_dis = cfaf["Average_Distance_per_Shipment"].mean()
            self.scenario_impact = self.total_dis * self.mode.get_impacts()

        elif self.mode.get_name() in ("Barge", "Ocean"):
            self.domestic_dis = faf["avr_dom_dist_km"].mean()
            self.foreign_dis = marine["Distance_km"].mean()
            self.total_dis = self.domestic_dis + self.foreign_dis
            self.scenario_impact = self.total_dis * self.mode.get_impacts()
        
        elif self.mode.get_name() == "Air":

            dms_coordinates = self.shipping_dest.get_cordinates()
            fr_coordinates = self.shipping_org.get_cordinates()
            self.total_dis = geodesic(dms_coordinates, fr_coordinates).km
            self.scenario_impact = self.total_dis * self.mode.get_impacts()

    def get_scenario_impact (self):

        """
        return the impact of the transportation based on the scenario.
        
        """
        return self.scenario_impact

    def get_distances (self):

        """
        return the distances of the transportation based on the scenario.
        
        """
        if self.scenario in ["Local", "Regional", "Regional_c", "National", "None", "NA", "Global", "Known"]:
            return self.domestic_dis, self.foreign_dis, self.total_dis



if __name__ == '__main__':

    pass