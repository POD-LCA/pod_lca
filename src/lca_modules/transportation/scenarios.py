import pandas as pd
from lca_modules.transportation.transport_mode import TransportMode
from geopy.distance import geodesic

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

        """
        cfs = self.project.get_subdataset("cfs_2017_cleaned")
        emission = self.project.get_subdataset("Emission")
        sctg = self.get_sctg(2)
        cfs = cfs[cfs["SCTG"] == str(sctg)].copy()
        
        if self.mode is not None:
            cfs = cfs[cfs["MODE"].isin(self.mode.get_cfs_mode()[1] [self.mode.get_name()])]

        if self.shipping_org is not None:
            cfs = cfs[cfs["ORIG_STATE"] == shipping_org.get_cfs_area()]

        if self.shipping_dest is not None:
            cfs = cfs[cfs["DEST_STATE"] == shipping_dest.get_cfs_area()]

            
        cfs_mapping = self.mode.get_cfs_mode()[1]
        reverse_mapping = {mode: key for key, modes in cfs_mapping.items() for mode in modes}
        cfs["mode_name"] = cfs["MODE"].map(reverse_mapping)
        merged_data = pd.merge(cfs, emission, on="mode_name", how="inner")

        merged_data = merged_data[ merged_data["eff"] == self.mode.get_efficiency()]
        merged_data.iloc[:, -5:] *= merged_data["SHIPMT_DIST_ROUTED"].values[:, None]

        self.local = merged_data[merged_data["quartile"] == "Q1"].iloc[:, -5:].mean().to_dict()
        self.regional = merged_data[merged_data["quartile"] == "Q2"].iloc[:, -5:].mean().to_dict()
        self.regional_c = merged_data[merged_data["quartile"] == "Q3"].iloc[:, -5:].mean().to_dict()
        self.national = merged_data[merged_data["quartile"] == "Q4"].iloc[:, -5:].mean().to_dict()


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
            pass
            # location = self.shipping_dest.get_faf_domestic_region()
            # faf = faf[faf["dms_dest"] == location]

        if self.mode_domestic is not None:
            faf = faf[faf["dms_mode"] == self.mode_domestic.get_faf_mode()]

        if self.mode is not None:
            faf = faf[faf["fr_inmode"] == self.mode.get_faf_mode()]

        # Truck------------------------------------
        if self.mode is not None: 

            if self.mode.get_name() == "Truck":
                
                distance = faf["avr_dom_dist_km"].mean()
                
                total_impacts = {}
                
                for key, value in self.mode.get_impacts().items():
                    domestic_total = value * distance
                    foreign_total = value * 200  
                    total_impacts[key] = domestic_total + foreign_total
                
                self.na = total_impacts

        #Rail------------------------------------
            elif self.mode.get_name() == "Rail":
                distance = cfaf["Average_Distance_per_Shipment"].mean()
                
                total_impacts = {}
                
                for key, value in self.mode.get_impacts().items():
                    total_impacts[key] = value * distance
                
                self.na = total_impacts

        #Water------------------------------------
            elif self.mode.get_name() == "Water":

                domestic_total = {}
                foreign_total = {}

                if self.mode_domestic is not None:
                    distance = faf["avr_dom_dist_km"].mean()
                    for key, value in self.mode_domestic.get_impacts().items():
                        domestic_total[key] = value * distance

                else:
                    faf = faf[faf["dms_mode"] == 1]
                    distance = faf["avr_dom_dist_km"].mean()

                    for key, value in TransportMode ("Truck", 1, self.project).get_impacts().items():
                        domestic_total[key] = value * distance
                    
                for key, value in self.mode.get_impacts().items():
                    if self.shipping_org is not None:
                        marine_dis = marine[marine["Region"] == self.shipping_org.get_location()]["Distance_km"].mean()
                    else:
                        marine_dis = marine["Distance_km"].mean()
                    
                    foreign_total[key] = value * marine_dis
                
                self.global_ = {key: domestic_total[key] + foreign_total[key] for key in domestic_total}

        #Air------------------------------------
            elif self.mode.get_name() == "Air":

                if self.shipping_dest is not None:
                    dest_location = self.shipping_dest.get_cordinates()
                else:
                    dest_location = (39.8283, -98.5795) #USA middle

                if self.shipping_org is not None:
                    org_location = self.shipping_org.get_cordinates()
                else:
                    org_location = (31.2304, 121.4737) #Shanghai

                distance = geodesic(org_location, dest_location).km
                total_impacts = {}

                for key, value in self.mode.get_impacts().items():
                    total_impacts[key] = value * distance

                self.global_ = total_impacts
        
        else:
            
            self.na = None
            self.global_ = None

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