import pandas as pd
import numpy as np
from lca_modules.transportation.transport_mode import TransportMode
from geopy.distance import geodesic
from lca_modules.location.data import CFS_DATA_PATH, FAF_city_representation, FAF_DOMESTIC_REGION
from lca_modules.location.location import Location
from lca_modules.transportation.modes_mapping import cfs_mapping
import json

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


        self.pre_us_processing()
        # self.pre_global_processing()


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
        cfs = cfs[cfs["SCTG"] == sctg].copy()
        cfs_state_code = pd.read_csv(CFS_DATA_PATH)


        if self.mode is not None:

            cfs_filterd = cfs[cfs["MODE"].isin(self.mode.get_cfs_mode()[1] [self.mode.get_name()])]
            cfs = cfs_filterd if not cfs_filterd.empty else cfs
        else:
            major_mode = cfs["MODE"].mode()

            cfs = cfs[cfs["MODE"] == major_mode[0]]
            for key, value in cfs_mapping.items():
                if major_mode[0] in value:
                    self.mode = TransportMode(key, self.project.get_links()[0].get_efficiency(), self.project)
            

        if self.shipping_dest is not None:
            cfs_filtered = cfs[cfs["DEST_STATE"] == self.shipping_dest.get_cfs_area()]
            cfs = cfs_filtered if not cfs_filtered.empty else cfs


            if cfs_filtered.empty:
                major_dest = cfs["DEST_STATE"].mode()[0]
                cfs = cfs[cfs["DEST_STATE"] == major_dest]

                for code in cfs_state_code["Code"].tolist():
                    if code == major_dest:
                        shipping_dest = cfs_state_code[cfs_state_code["Code"] == code]["State"].values[0]
                        self.shipping_dest = Location.from_str(shipping_dest)
        # else:
        #     major_dest = cfs["DEST_STATE"].mode()[0]
        #     cfs = cfs[cfs["DEST_STATE"] == major_dest]

        #     for code in cfs_state_code["Code"].tolist():
        #         if code == major_dest:
        #             shipping_dest = cfs_state_code[cfs_state_code["Code"] == code]["State"].values[0]
        #             self.shipping_dest = Location.from_str(shipping_dest)

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
        
        """
        scenarios = ["NA","Global","None"]
        emission = self.project.get_subdataset("Emission")
        faf = self.project.get_subdataset("FAF561_cleaned")
        cfaf = self.project.get_subdataset("cfaf_cleaned")
        marine = self.project.get_subdataset("Marine_cleaned")
        sctg = self.get_sctg(2)
        
        faf = faf[faf["sctg2"] == sctg].copy()
        cfaf = cfaf[cfaf["SCTG_2digits"] == sctg].copy()
        print (sctg)

        if self.mode is not None:
            faf_filtered = faf[faf["fr_inmode"] == self.mode.get_faf_mode()]
            faf = faf_filtered if not faf_filtered.empty else faf
        else:
            self.mode = TransportMode("Barge", self.project.get_links()[0].get_efficiency(), self.project)
            faf_filtered = faf[faf["fr_inmode"] == self.mode.get_faf_mode()]
            faf = faf_filtered if not faf_filtered.empty else faf


        if self.shipping_dest is not None:

            marine_location = self.shipping_dest.us_coast
            dms_domestic_faf = self.shipping_dest.get_faf_domestic_region()
            dms_coordinates = self.shipping_dest.get_cordinates()

            marine_filtered = marine[marine["Coast"] == marine_location]
            faf_filtered = faf[faf["dms_dest"].isin(dms_domestic_faf)]
        
            # check if the filtered data is empty
            faf = faf_filtered if not faf_filtered.empty else faf
            marine = marine_filtered if not marine_filtered.empty else marine

        else:
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

            marine_filtered = marine[marine["Coast"] == marine_location]
            faf_filtered = faf[faf["dms_dest"].isin(dms_domestic_faf)]

            # check if the filtered data is empty
            faf = faf_filtered if not faf_filtered.empty else faf
            marine = marine_filtered if not marine_filtered.empty else marine


        if self.shipping_org is not None:

            marine_location = self.shipping_org.get_marine_region()
            fr_origin_faf = self.shipping_org.get_faf_foreign_region()
            fr_coordinates = self.shipping_org.get_cordinates()

            marine_filtered = marine[marine["Region"] == marine_location]
            faf_filtered = faf[faf["fr_orig"] == fr_origin_faf]
            # check if the filtered data is empty
            faf = faf_filtered if not faf_filtered.empty else faf
            marine = marine_filtered if not marine_filtered.empty else marine



        if self.mode_domestic is not None:

            faf_filtered = faf[faf["dms_mode"] == self.mode_domestic.get_faf_mode()]
            faf = faf_filtered if not faf_filtered.empty else faf
        else:
            self.mode_domestic = TransportMode("Truck", self.project.get_links()[0].get_efficiency(), self.project)
            faf_filtered = faf[faf["dms_mode"] == self.mode_domestic.get_faf_mode()]
            faf = faf_filtered if not faf_filtered.empty else faf

        if self.mode is not None:

            faf_filterd = faf[faf["fr_inmode"] == self.mode.get_faf_mode()]
            faf = faf_filterd if not faf_filterd.empty else faf
        

            if self.mode.get_name() == "Truck":
                
                for scenario in scenarios:

                    if scenario == "NA":
                        faf_filtered_na = faf[faf["fr_orig"].isin([801, 802])]
                        faf_na = faf_filtered_na if not faf_filtered_na.empty else faf
                        domestic_total = self.mode.get_impacts() * faf_na["avr_dom_dist_km"].mean()
                        foreign_total = self.mode.get_impacts() * 200
                        total_impact = domestic_total + foreign_total

                        self.na = total_impact
                        self.distances["NA"] = 200 + faf_na["avr_dom_dist_km"].mean()

                    elif scenario == "Global":
                        faf_filtered_global = faf[faf["fr_orig"].isin([801, 802]) == False]
                        faf_global = faf_filtered_global if not faf_filtered_global.empty else faf
                        domestic_total = self.mode.get_impacts() * faf_global["avr_dom_dist_km"].mean()
                        foreign_total = self.mode.get_impacts() * 200
                        total_impact = domestic_total + foreign_total

                        self.global_ = total_impact
                        self.distances["Global"] = 200 + faf_global["avr_dom_dist_km"].mean()

                    elif scenario == "None":
                        domestic_total = self.mode.get_impacts() * faf["avr_dom_dist_km"].mean()
                        foreign_total = self.mode.get_impacts() * 200
                        total_impact = domestic_total + foreign_total
    
                        self.none = total_impact
                        self.distances["None"] = 200 + faf["avr_dom_dist_km"].mean()

            if self.mode.get_name() == "Rail":

                distance = cfaf["Average_Distance_per_Shipment"].mean()
                total_impacts = self.mode.get_impacts()* distance
                
                self.na = total_impacts
                self.distances["NA"] = distance
                self.global_ = total_impacts
                self.distances["Global"] = distance
                self.none = total_impacts
                self.distances["None"] = distance
                

            if self.mode.get_name() == "Barge" or "Ocean":
                
                for scenario in scenarios:

                    if scenario == "NA":
                        faf_filtered_na = faf[faf["fr_orig"].isin([801, 802])]
                        marine_flitered_na = marine[marine["Region"].isin(["Canada", "Mexico"])]
                        faf_na = faf_filtered_na if not faf_filtered_na.empty else faf
                        marine_na = marine_flitered_na if not marine_flitered_na.empty else marine
                        domestic_na_dis = faf_na["avr_dom_dist_km"].mean()
                        domestic_total = self.mode_domestic.get_impacts() * domestic_na_dis
                        marine_na_dis = marine_na["Distance_km"].mean()
                        marine_na_impacts = self.mode.get_impacts() * marine_na_dis

                        self.distances["NA"] = marine_na_dis + domestic_na_dis
                        self.na = marine_na_impacts + domestic_total

                    elif scenario == "Global":
                        faf_filtered_global = faf[faf["fr_orig"].isin([801, 802]) == False]
                        marine_filtered_global = marine[marine["Region"].isin(["Canada", "Mexico"]) == False]
                        faf_global = faf_filtered_global if not faf_filtered_global.empty else faf
                        marine_global = marine_filtered_global if not marine_filtered_global.empty else marine
                        domestic_global_dis = faf_global["avr_dom_dist_km"].mean()
                        domestic_total = self.mode_domestic.get_impacts() * domestic_global_dis
                        marine_global_dis = marine_global["Distance_km"].mean()
                        marine_global_impacts = self.mode.get_impacts() * marine_global_dis

                        self.global_ = marine_global_impacts + domestic_total
                        self.distances["Global"] = marine_global_dis + domestic_global_dis

                    
                    elif scenario == "None":

                        marine_none_dis = marine["Distance_km"].mean()
                        marine_none_impacts = self.mode.get_impacts() * marine_none_dis
                        domestic_none_dis = faf["avr_dom_dist_km"].mean()
                        domestic_total = self.mode_domestic.get_impacts() * domestic_none_dis

                        self.distances["None"] = marine_none_dis + domestic_none_dis
                        self.none = marine_none_impacts + domestic_total



            if self.mode.get_name() == "Air":
                
                for scenario in scenarios:
                    if scenario == "NA":
                        faf_filtered_na = faf[faf["fr_orig"].isin([801, 802])]
                        faf_na_mode = faf_filtered_na ["fr_orig"].mode (0)[0]

                        for key, value in FAF_city_representation.items():
                            if faf_na_mode == key:
                                faf_na_mode = value
                                self.shipping_org = Location.from_str(faf_na_mode)
                        
                        fr_coordinates_na = self.shipping_org.get_cordinates()
                        air_na_dist = geodesic(fr_coordinates_na, dms_coordinates).km


                        self.distances["NA"] = air_na_dist
                        self.na = air_na_dist * self.mode.get_impacts()

                    elif scenario == "Global":
                        faf_filtered_global = faf[faf["fr_orig"].isin([801, 802]) == False]
                        faf_global_mode = faf_filtered_global ["fr_orig"].mode (0)[0]

                        for key, value in FAF_city_representation.items():
                            if faf_global_mode == key:
                                faf_global_mode = value
                                self.shipping_org = Location.from_str(faf_global_mode)
                        
                        fr_coordinates_global = self.shipping_org.get_cordinates()
                        air_global_dist = geodesic(fr_coordinates_global, dms_coordinates).km


                        self.global_ = air_global_dist* self.mode.get_impacts()
                        self.distances["Global"] = air_global_dist
                        
                    elif scenario == "None":
                        
                        if self.shipping_org is not None:
                            fr_coordinates = self.shipping_org.get_cordinates()
                            air_none_dist = geodesic(fr_coordinates, dms_coordinates).km

                        else:
                            faf_none_mode = faf["fr_orig"].mode (0)[0]
                            for key, value in FAF_city_representation.items():
                                if faf_none_mode == key:
                                    faf_none_mode = value
                                    self.shipping_org = Location.from_str(faf_none_mode)

                            fr_coordinates = self.shipping_org.get_cordinates()
                            air_none_dist = geodesic(fr_coordinates, dms_coordinates).km

                        self.distances["None"] = air_none_dist
                        self.none = air_none_dist * self.mode.get_impacts()
                    


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