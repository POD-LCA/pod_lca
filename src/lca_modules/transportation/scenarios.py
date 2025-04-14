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
        self.distances = {"Local": 0, "Regional": 0, "Regional_c": 0, "National": 0, "NA": 0, "Global": 0, "None": 0, "Known": 0}
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
        self.Known = None

        self.pre_us_processing()
        self.pre_global_processing()

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

        cfs = self.project.get_subdataset("cfs_2017_cleaned")
        sctg = self.get_sctg(2)
        cfs = cfs[cfs["SCTG"] == sctg].copy()
        cfs_state_code = pd.read_csv(CFS_DATA_PATH)

        print (sctg)

        if self.shipping_dest is not None:
            cfs_filtered = cfs[cfs["DEST_STATE"] == self.shipping_dest.get_cfs_area()]
            cfs = cfs_filtered if not cfs_filtered.empty else cfs

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
                    print (f"No location for destination found in cfs, The value shows the closest shipping to the selected destination {closest_state}")


        if self.shipping_org is not None:

            cfs_filtered = cfs[cfs["ORIG_STATE"] == self.shipping_org.get_cfs_area()]
            cfs = cfs_filtered if not cfs_filtered.empty else cfs

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

            cfs = cfs_filtered if not cfs_filtered.empty else cfs

        if self.mode is not None:

            cfs_filtered = cfs[cfs["MODE"].isin(self.mode.get_cfs_mode()[1] [self.mode.get_name()])]
            cfs = cfs_filtered if not cfs_filtered.empty else cfs
        else:
            major_mode = cfs["MODE"].mode()
            cfs = cfs[cfs["MODE"] == major_mode[0]]
            for key, value in cfs_mapping.items():
                if major_mode[0] in value:
                    mode_cfs_t = TransportMode(key, self.project.get_links()[0].get_efficiency(), self.project)



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

        if self.mode is not None:
            impact = self.mode.get_impacts()
        else:
            impact = mode_cfs_t.get_impacts()


        self.local = cfs[cfs["quartile"] == "Q1"]["SHIPMT_DIST_ROUTED"].mean()* impact
        self.distances["Local"] = cfs[cfs["quartile"] == "Q1"]["SHIPMT_DIST_ROUTED"].mean()

        self.regional = cfs[cfs["quartile"] == "Q2"]["SHIPMT_DIST_ROUTED"].mean()* impact
        self.distances["Regional"] = cfs[cfs["quartile"] == "Q2"]["SHIPMT_DIST_ROUTED"].mean()

        self.regional_c = cfs[cfs["quartile"] == "Q3"]["SHIPMT_DIST_ROUTED"].mean() * impact
        self.distances["Regional_c"] = cfs[cfs["quartile"] == "Q3"]["SHIPMT_DIST_ROUTED"].mean()

        self.national = cfs[cfs["quartile"] == "Q4"]["SHIPMT_DIST_ROUTED"].mean()* impact
        self.distances["National"] = cfs[cfs["quartile"] == "Q4"]["SHIPMT_DIST_ROUTED"].mean()

        self.none = cfs["SHIPMT_DIST_ROUTED"].mean()* impact
        self.distances["None"] = cfs["SHIPMT_DIST_ROUTED"].mean()


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
        scenarios = ["NA","Global"]
        emission = self.project.get_subdataset("Emission")
        faf = self.project.get_subdataset("FAF561_cleaned")
        cfaf = self.project.get_subdataset("cfaf_cleaned")
        marine = self.project.get_subdataset("Marine_cleaned")
        sctg = self.get_sctg(2)
        
        faf = faf[faf["sctg2"] == sctg].copy()
        cfaf = cfaf[cfaf["SCTG_2digits"] == sctg].copy()



        if self.shipping_dest is not None:
            
            try:
                marine_location = self.shipping_dest.us_coast
                dms_domestic_faf = self.shipping_dest.get_faf_domestic_region()
                dms_coordinates = self.shipping_dest.get_cordinates()

                marine = marine[marine["Coast"] == marine_location]
                faf = faf[faf["dms_dest"].isin(dms_domestic_faf)]

                if faf.empty or marine.empty:
                    raise ValueError("no destination found in the dataset")

            except Exception as e:
                print("Error:", e)
                marine = 0
                faf = 0

        else:

            try:
                major_domes = faf["dms_dest"].mode()[0]
                with open (FAF_DOMESTIC_REGION, "r") as f:
                    faf_domestic_data = json.load(f)
                    for key, value in faf_domestic_data.items():
                        if major_domes in value:
                            major_domes = key

                self.shipping_dest = Location.from_str(major_domes)
                marine_location = self.shipping_dest.us_coast
                dms_domestic_faf = self.shipping_dest.get_faf_domestic_region()
                dms_coordinates = self.shipping_dest.get_cordinates()
                marine = marine[marine["Coast"] == marine_location]
                faf = faf[faf["dms_dest"].isin(dms_domestic_faf)]
                
                print (f"destination is the most frequent shipping destination {major_domes}")

                if faf.empty or marine.empty:
                    raise ValueError("no destination found in the dataset")

            except Exception as e:
                print("Error:", e)
                marine = 0
                faf = 0


        if self.shipping_org is not None:

            try:
                marine_location = self.shipping_org.get_marine_region()
                fr_origin_faf = self.shipping_org.get_faf_foreign_region()
                fr_coordinates = self.shipping_org.get_cordinates()

                marine = marine[marine["Region"] == marine_location]
                faf = faf[faf["fr_orig"] == fr_origin_faf]

                if faf.empty or marine.empty:
                    raise ValueError("no origin found in the dataset")

            except Exception as e:
                print("Error:", e)
                marine = 0
                faf = 0

        else:

            try:
                faf_na_mode = faf[faf["fr_orig"].isin([801, 802])]["fr_orig"].mode()[0]
                faf_na = faf[faf["fr_orig"] == faf_na_mode]

                if faf_na.empty:
                    raise ValueError("no origin found in North America")
            except Exception as e:
                print("Error:", e)
                faf_na = 0

            try:
                faf_global_mode = faf[faf["fr_orig"].isin([801, 802]) == False]["fr_orig"].mode()[0]
                faf_global = faf[faf["fr_orig"] == faf_global_mode]

                if faf_global.empty:
                    raise ValueError("no origin found in global")
            except Exception as e:
                print("Error:", e)
                faf_global = 0

            try:
                marine_na = marine[marine["Region"].isin(["Canada", "Mexico"])]

                for key,value in FAF_DATA.items():
                    if faf_na_mode in value:
                        marine_na_mode = key
                        break
                marine_na_mode = Location.from_str(marine_na_mode).get_marine_region()
                marine_na = marine[marine["Region"] == marine_na_mode]
                
                if marine_na.empty:
                    raise ValueError("no origin for North America scenario in marine dataset")
            except Exception as e:
                print("Error:", e)
                marine_na = 0

            try:
                marine_global_mode = marine[marine["Region"].isin(["Canada", "Mexico"]) == False]

                for key,value in FAF_DATA.items():
                    if faf_global_mode in value:
                        marine_global_mode = key
                        break
                marine_global_mode = Location.from_str(marine_global_mode).get_marine_region()
                marine_global = marine[marine["Region"] == marine_global_mode]

                if marine_global.empty:
                    raise ValueError("no origin for global scenario in marine dataset")
            except Exception as e:
                print("Error:", e)
                marine_global = 0


        if self.mode is not None:
            try:
                faf_na = faf_na[faf_na["fr_inmode"] == self.mode.get_faf_mode()]
                faf_global = faf_global[faf_global["fr_inmode"] == self.mode.get_faf_mode()]

                if faf_na.empty or faf_global.empty:
                    raise ValueError("no data for the selected mode of transportation")
            except Exception as e:
                print("Error:", e)
                faf_na = 0
                faf_global = 0

        else:
            try:
                self.mode = TransportMode("Barge", self.project.get_links()[0].get_efficiency(), self.project)
                faf_na = faf_na[faf_na["fr_inmode"] == self.mode.get_faf_mode()]
                faf_global = faf_global[faf_global["fr_inmode"] == self.mode.get_faf_mode()]

                if faf_na.empty or faf_global.empty:
                    raise ValueError("no data for the selected mode of transportation")
            except Exception as e:
                print("Error:", e)
                faf_na = 0
                faf_global = 0

        if self.mode_domestic is not None:
            try:
                faf_na = faf_na[faf_na["dms_mode"] == self.mode_domestic.get_faf_mode()]
                faf_global = faf_global[faf_global["dms_mode"] == self.mode_domestic.get_faf_mode()]

                if faf_na.empty or faf_global.empty:
                    raise ValueError("no data for the selected domestic mode of transportation")

            except Exception as e:
                print("Error:", e)
                faf_na = 0
                faf_global = 0
        else:
            try:
                self.mode_domestic = TransportMode("Truck", self.project.get_links()[0].get_efficiency(), self.project)
                faf_na = faf_na[faf_na["dms_mode"] == self.mode_domestic.get_faf_mode()]
                faf_global = faf_global[faf_global["dms_mode"] == self.mode_domestic.get_faf_mode()]

                if faf_na.empty or faf_global.empty:
                    raise ValueError("no data for the selected domestic mode of transportation")
                    
            except Exception as e:
                print("Error:", e)
                faf_na = 0
                faf_global = 0


        if self.mode is not None:

            if self.mode.get_name() == "Truck":
    
                for scenario in scenarios:

                    if scenario == "NA":

                        try:
                            domestic_total = self.mode_domestic.get_impacts() * faf_na["avr_dom_dist_km"].mean()
                            foreign_total = self.mode.get_impacts() * 200
                            total_impact = domestic_total + foreign_total

                            self.na = total_impact
                            self.distances["NA"] = 200 + faf_na["avr_dom_dist_km"].mean()
                        except:

                            print ("No data for the Truck")
                            self.distances["NA"] = 0
                            self.na = self.mode.get_impacts() * 0

                    elif scenario == "Global":

                        self.global_ = self.mode.get_impacts() * 0
                        self.distances["Global"] = 0


            elif self.mode.get_name() == "Rail":

                try:
                    distance = cfaf["Average_Distance_per_Shipment"].mean()
                    self.na = self.mode.get_impacts()* distance
                    self.distances["NA"] = distance
                    self.global_ = self.mode.get_impacts()*0
                    self.distances["Global"] = 0
                except:
                    print ("No data for the Rail")
                    self.distances["NA"] = 0
                    self.na = self.mode.get_impacts() * 0
                    self.distances["Global"] = 0
                    self.global_ = self.mode.get_impacts() * 0


            elif self.mode.get_name() in ("Barge", "Ocean"):

                for scenario in scenarios:

                    if scenario == "NA":

                        try:

                            domestic_na_dis = faf_na["avr_dom_dist_km"].mean()
                            domestic_total = self.mode_domestic.get_impacts() * domestic_na_dis
                            marine_na_dis = marine_na["Distance_km"].mean()
                            marine_na_impacts = self.mode.get_impacts() * marine_na_dis
                            self.distances["NA"] = marine_na_dis + domestic_na_dis
                            self.na = marine_na_impacts + domestic_total

                        except:

                            print ("No data for the Barge")
                            self.distances["NA"] = 0
                            self.na = self.mode.get_impacts() * 0
                            

                    elif scenario == "Global":

                        try:
                            domestic_global_dis = faf_global["avr_dom_dist_km"].mean()
                            domestic_total = self.mode_domestic.get_impacts() * domestic_global_dis
                            marine_global_dis = marine_global["Distance_km"].mean()
                            marine_global_impacts = self.mode.get_impacts() * marine_global_dis

                            self.global_ = marine_global_impacts + domestic_total
                            self.distances["Global"] = marine_global_dis + domestic_global_dis

                        except:
                            print ("No data for the Barge")
                            self.distances["Global"] = 0
                            self.global_ = self.mode.get_impacts() * 0

            elif self.mode.get_name() == "Air":

                if self.shipping_org is not None:

                    if self.shipping_org.get_faf_foreign_region() in (801, 802):
                        air_dist = geodesic(dms_coordinates, fr_coordinates).km
                        self.distances["NA"] = air_dist
                        self.na = air_dist * self.mode.get_impacts()

                    elif self.shipping_org.get_faf_foreign_region() != 803:
                        air_dist = geodesic(dms_coordinates, fr_coordinates).km
                        self.distances["Global"] = air_dist
                        self.global_ = air_dist * self.mode.get_impacts() 
                    else:
                        self.global_ = self.distances["Global"] * self.mode.get_impacts()
                        self.na = self.distances["NA"] * self.mode.get_impacts()

                else:

                    for scenario in scenarios:
                        if scenario == "NA":

                            try:
                                faf_na_mode = faf_na ["fr_orig"].mode (0)[0]
                                for key, value in FAF_city_representation.items():
                                    if faf_na_mode == key:
                                        faf_na_mode = value
                                        shipping_org = Location.from_str(faf_na_mode)
                                
                                fr_coordinates_na = shipping_org.get_cordinates()
                                air_na_dist = geodesic(fr_coordinates_na, dms_coordinates).km

                                self.distances["NA"] = air_na_dist
                                self.na = air_na_dist * self.mode.get_impacts()
                            except:
                                print ("No data for the Air")
                                self.distances["NA"] = 0
                                self.na = self.mode.get_impacts() * 0

                        elif scenario == "Global":
                            
                            try:
                                faf_global_mode = faf_global ["fr_orig"].mode (0)[0]

                                for key, value in FAF_city_representation.items():
                                    if faf_global_mode == key:
                                        faf_global_mode = value
                                        shipping_org = Location.from_str(faf_global_mode)

                                fr_coordinates_global = shipping_org.get_cordinates()
                                air_global_dist = geodesic(fr_coordinates_global, dms_coordinates).km


                                self.global_ = air_global_dist* self.mode.get_impacts()
                                self.distances["Global"] = air_global_dist
                            except:
                                print ("No data for the Air")
                                self.distances["Global"] = 0
                                self.global_ = self.mode.get_impacts() * 0


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

        if self.scenario == "Known":
            return self.Known


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