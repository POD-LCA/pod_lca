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
        cfs = self.project.get_subdataset("cfs_2017")
        emission = self.project.get_subdataset("Emission")
        cfs = cfs.drop(columns=["SHIPMT_ID", "QUARTER", "SHIPMT_VALUE", "TEMP_CNTL_YN", "EXPORT_CNTRY",
                                "HAZMAT", "WGT_FACTOR", "ORIG_MA", "ORIG_CFS_AREA", "DEST_MA", "DEST_CFS_AREA"])

        sctg = self.get_sctg(2)
        df = cfs[cfs["SCTG"] == str(sctg)].copy()
        quartiles = df["SHIPMT_DIST_ROUTED"].quantile([0.25, 0.5, 0.75]).values

        def assign_quartile(x, q1, q2, q3):
            if x <= q1:
                return 'Q1'
            elif x <= q2:
                return 'Q2'
            elif x <= q3:
                return 'Q3'
            else:
                return 'Q4'

        df['quartile'] = df["SHIPMT_DIST_ROUTED"].apply(assign_quartile, args=(quartiles[0], quartiles[1], quartiles[2]))

        quartile_mapping = {
            "Local": df[df['quartile'] == 'Q1'],
            "Regional": df[df['quartile'] == 'Q2'],
            "Regional_c": df[df['quartile'] == 'Q3'],
            "National": df[df['quartile'] == 'Q4']
        }
        
        def process_scenario(df, emission, mode, shipping_org, shipping_dest, eff):

            df = pd.merge(emission, df, left_on="mode_cfs", right_on="MODE")
            if shipping_org is not None:
                df = df[df["ORIG_STATE"] == shipping_org.get_cfs_area()]

            if shipping_dest is not None:
                df = df[df["DEST_STATE"] == shipping_dest.get_cfs_area()]

            if mode is not None:
                df = df[(df["mode_name"] == self.mode.get_name()) & (df["eff"] == eff)]
                    
            if df.empty:
                #print("There is no shipping for this information, the value shows the average of shipping based on CFS")
                df = pd.merge(emission, df, left_on="mode_cfs", right_on="MODE")

            impact_cols = df.columns[5:10]
            df[impact_cols] = df[impact_cols].multiply(df["SHIPMT_DIST_ROUTED"], axis=0)
            
            return df[impact_cols].mean().to_dict()

        for scenario_name, scenario_df in quartile_mapping.items():
            impact = process_scenario(scenario_df, emission, self.mode, self.shipping_org, self.shipping_dest, None if self.mode is None else self.mode.get_efficiency())
            setattr(self, scenario_name.lower(), impact)


    def pre_global_processing (self):
        """
        process the data for the North America and Global scenarios.
        
        """
        #reading the data
        emission = self.project.get_subdataset("Emission")
        faf = self.project.get_subdataset("FAF561_cleaned")
        cfaf = self.project.get_subdataset("cfaf_cleaned")
        pod_lca_dataset = self.project.get_subdataset("PODlLDA_transport_dataset")
        marine = self.project.get_subdataset("Marine_cleaned")

        #filtering the data by sctg code
        sctg = self.get_sctg(2)
        
        faf = faf[faf["sctg2"] == sctg].copy()
        cfaf = cfaf[cfaf["SCTG_2digits"] == sctg].copy()
        
        
        #filtering the data by location if is defined
        if self.shipping_dest is not None:
            pass
            # location = self.shipping_dest.get_faf_domestic_region()
            # faf = faf[faf["dms_dest"] == location]

        if self.mode_domestic is not None:
            faf = faf[faf["dms_mode"] == self.mode_domestic.get_faf_mode()]

        # Truck------------------------------------
        if self.mode is not None: 
            if self.mode.get_name() == "Truck":
                
                faf = faf[faf["fr_inmode"] == self.mode.get_faf_mode()]
                distance = faf["avr_dom_dist_km"].mean()
                
                total_impacts = {}
                
                for key, value in self.mode.get_impacts().items():
                    domestic_total = value * distance
                    foreign_total = value * 200  
                    total_impacts[key] = domestic_total + foreign_total
                
                self.na = total_impacts

        #Rail------------------------------------
        if self.mode is not None: 
            if self.mode.get_name() == "Rail":
                distance = cfaf["Average_Distance_per_Shipment"].mean()
                
                total_impacts = {}
                
                for key, value in self.mode.get_impacts().items():
                    total_impacts[key] = value * distance
                
                self.na = total_impacts

        #Water------------------------------------
        if self.mode is not None: 
            if self.mode.get_name() == "Water":

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
        if self.mode is not None: 
            if self.mode.get_name() == "Air":

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