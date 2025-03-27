import pandas as pd
import numpy as np
from lca_modules.transportation.transport_mode import TransportMode
from geopy.distance import geodesic
from lca_modules.location.data import CFS_DATA_PATH, FAF_city_representation, FAF_DOMESTIC_REGION
from lca_modules.location.location import Location
from lca_modules.transportation.modes_mapping import cfs_mapping

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
        cfs = cfs[cfs["SCTG"] == sctg].copy()
        df = pd.read_csv(CFS_DATA_PATH)

        if self.mode is not None:
            cfs_c = cfs.copy()
 
            cfs = cfs[cfs["MODE"].isin(self.mode.get_cfs_mode()[1] [self.mode.get_name()])]
            if cfs.empty:
                cfs = cfs_c
                print ("No mode found in cfs, value shows the avarage distance of the modes")
        else:
            major_mode = cfs["MODE"].mode()
            cfs = cfs[cfs["MODE"] == major_mode[0]]

            for key, value in cfs_mapping.items():
                if major_mode[0] in value:
                    self.mode = TransportMode(key, self.project.get_links()[0].get_efficiency(), self.project)
                    
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
                
                distance_na = faf["avr_dom_dist_km"].mean()
                total_impacts = {}
                
                domestic_total = self.mode.get_impacts() * distance
                foreign_total = self.mode.get_impacts() * 200
                total_impact = domestic_total + foreign_total
                

                self.na = total_impacts
                self.distances["NA"] = distance
                self.global_ = total_impacts
                self.distances["Global"] = distance
                self.distances["None"] = distance
                self.none = total_impacts


            if self.mode.get_name() == "Rail":
                distance = cfaf["Average_Distance_per_Shipment"].mean()
                
                total_impacts = {}
                total_impacts = self.mode.get_impacts()* distance
                
                self.na = total_impacts
                self.distances["NA"] = distance
                self.global_ = total_impacts
                self.distances["Global"] = distance
                self.distances["None"] = distance
                self.none = total_impacts


            if self.mode.get_name() == "Barge" or "Ocean":

                if self.mode_domestic is not None:
                    distance = faf["avr_dom_dist_km"].mean()
                    domestic_total = self.mode_domestic.get_impacts() * distance

                else:
                    faf = faf[faf["dms_mode"] == 1] #Truck as default
                    distance = faf["avr_dom_dist_km"].mean()
                    domestic_total = TransportMode ("Truck", 1, self.project).get_impacts() * distance
                
                marine_none_dis = marine["Distance_km"].mean()
                marine_none_impacts = self.mode.get_impacts() * marine_none_dis

                marine_na = marine[(marine["Region"] == "Canada") | (marine["Region"] == "Mexico")]
                marine_na_dis = marine_na["Distance_km"].mean()
                marine_na_impacts = self.mode.get_impacts() * marine_na_dis

                marine_global = marine [(marine["Region"] != "Canada") & (marine["Region"] != "Mexico")]
                marine_global_dis = marine["Distance_km"].mean()
                marine_global_impacts = self.mode.get_impacts() * marine_global_dis

                self.global_ = marine_global_impacts + domestic_total
                self.distances["Global"] = marine_global_dis + distance
                self.distances["NA"] = marine_na_dis + distance
                self.distances["None"] = marine_none_dis + distance
                self.na = marine_na_impacts + domestic_total
                self.none = marine_none_impacts + domestic_total


            if self.mode.get_name() == "Air":

                if self.shipping_dest is not None:
                    dest_location = self.shipping_dest.get_cordinates()
                else:
                    major_domes = faf["dms_dest"].mode()[0]
                    with open (FAF_DOMESTIC_REGION, "r") as f:
                        FAF_DOMESTIC_REGION = json.load(f)

                        for key, value in FAF_DOMESTIC_REGION.items():
                            if major_domes == value:
                                major_domes = key

                    dest_location = Location.from_str(major_domes).get_cordinates()

                if self.shipping_org is not None:
                    org_location = self.shipping_org.get_cordinates()
                    air_none_dist = geodesic(org_location, dest_location).km

                else:
                    air_none_dist = None
                    major_cities = faf["fr_orig"].mode()[0]
                    for key, value in FAF_city_representation.items():
                        if major_cities == key:
                            major_cities = value
                            major_cities = Location.from_str(major_cities).get_cordinates()

                    air_global_dist = geodesic(major_cities, dest_location).km
                    air_na_dist = (geodesic((50.000678, -86.000977), dest_location).km + geodesic((19.4326296, -99.1331785), dest_location).km) / 2
                    
                
                self.global_ = air_global_dist* self.mode.get_impacts()
                self.distances["Global"] = air_global_dist
                self.distances["NA"] = air_na_dist
                self.na = air_na_dist * self.mode.get_impacts()
                self.distances["None"] = air_none_dist
                self.none = None if air_none_dist is None else air_none_dist* self.mode.get_impacts()

        else:

            mode_na = emission[emission["eff"] == self.project.get_links()[0].get_efficiency()].iloc[:, -5:].mean().to_dict()
            mode_global = emission[emission["eff"] == self.project.get_links()[0].get_efficiency()].iloc[:, -5:].mean().to_dict()

            if self.shipping_dest is None:
                
                major_domes = faf["dms_dest"].mode()[0]
                with open (FAF_DOMESTIC_REGION, "r") as f:
                    FAF_DOMESTIC_REGION = json.load(f)

                    for key, value in FAF_DOMESTIC_REGION.items():
                        if major_domes == value:
                            major_domes = key

                    shipping_dest_coords = Location.from_str(major_domes).get_cordinates()
            else:
                shipping_dest_coords = self.shipping_dest.get_cordinates()

            major_cities = faf["fr_orig"].mode()[0]
            for key, value in FAF_city_representation.items():
                if major_cities == key:
                    major_cities = value
                    major_cities = Location.from_str(major_cities).get_cordinates()


            rail_global_na_distance = (cfaf["Average_Distance_per_Shipment"].mean())/4
            rail_global_na_impact = rail_global_na_distance *TransportMode("Rail", self.project.get_links()[0].get_efficiency() , self.project).get_impacts()

            marine_na_distance = marine[(marine["Region"] == "Canada") | (marine["Region"] == "Mexico")]
            marine_na_distance = (marine_na_distance ["Distance_km"].mean())/4
            marine_na_impact = marine_na_distance*TransportMode("Ocean", self.project.get_links()[0].get_efficiency() , self.project).get_impacts()

            truck_global_na_distance = 200 /4
            truck_global_na_impact = truck_global_na_distance * TransportMode("Truck", self.project.get_links()[0].get_efficiency() , self.project).get_impacts()

            air_na_distance = ((geodesic((50.000678, -86.000977), shipping_dest_coords).km + geodesic((19.4326296, -99.1331785), shipping_dest_coords).km) / 2 )/4
            air_na_impact = air_na_distance * TransportMode("Air", self.project.get_links()[0].get_efficiency() , self.project).get_impacts()

            marine_global_distance = (marine["Distance_km"].mean())/4
            marine_global_impact = marine_global_distance * TransportMode("Ocean", self.project.get_links()[0].get_efficiency() , self.project).get_impacts()

            air_global_dist = (geodesic(major_cities, shipping_dest_coords).km)/4
            air_global_impact = air_global_dist * TransportMode("Air", self.project.get_links()[0].get_efficiency() , self.project).get_impacts()


            self.na = rail_global_na_impact + marine_na_impact + truck_global_na_impact + air_na_impact
            self.distances["NA"] = rail_global_na_distance + marine_na_distance + truck_global_na_distance + air_na_distance
            self.distances["Global"] = rail_global_na_distance + truck_global_na_distance + marine_global_distance + air_global_dist
            self.global_ = rail_global_na_impact + truck_global_na_impact + marine_global_impact + air_global_impact

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