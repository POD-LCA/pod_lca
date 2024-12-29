import pandas as pd
from lca_modules.transportation.transport_mode import TransportMode
from geopy.distance import geodesic

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"



class Scenario:
    
    def __init__(self, project ,scenario, material, mode, mode_domestic, shipping_org):

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

        """

        self.scenario = scenario
        self.project = project
        self.material = material
        self.mode = mode
        self.mode_domestic = mode_domestic
        self.shipping_org = shipping_org
        self.local = None
        self.regional = None
        self.regional_c = None
        self.national = None
        self.na = None
        self.global_ = None

        self.pre_us_processing()
        #self.pre_global_processing()

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

        def process_scenario(df, emission, mode=None, location_org=None, location_dest=None):

            df = pd.merge(emission, df, left_on="mode_cfs", right_on="MODE")
            if location_org is not None:
                df = df[df["ORIG_STATE"] == location_org]
            if location_dest is not None:
                df = df[df["DEST_STATE"] == location_dest]
            if mode is not None:
                df = df[(df["mode_name"] == self.mode.get_name()) & (df["eff"] == self.mode.get_efficiency())]
            impact_cols = df.columns[5:10]
            df[impact_cols] = df[impact_cols].multiply(df["SHIPMT_DIST_ROUTED"], axis=0)
            return df[impact_cols].mean().to_dict()

        for scenario_name, scenario_df in quartile_mapping.items():
            impact = process_scenario(scenario_df, emission, self.mode.get_name(), self.location_org, self.location_dest)
            setattr(self, scenario_name.lower(), impact)

    

    def pre_global_processing (self):
        
        #reading the data
        emission = self.project.get_subdataset("Emission")
        faf = self.project.get_subdataset("FAF561_cleaned")
        cfaf = self.project.get_subdataset("cfaf_cleaned")
        pod_lca_dataset = self.project.get_subdataset("PODlLDA_transport_dataset")
        marine = self.project.get_subdataset("marine")

        #filtering the data by sctg code
        sctg = self.get_sctg(2)
        faf = faf[faf["sctg2"] == str(sctg)].copy()
        cfaf = cfaf[cfaf["SCTG_2digits"] == sctg].copy()

        #filtering the data by location if is defined
        if project.get_location() is not None:

            location = project.get_location()
            faf = faf[faf["dms_orig"] == location]

        #filtering the data by domestic mode if is defined
        if self.mode.domestic is not None:
            faf = faf[faf["dms_mode"] == self.mode_domestic.get_faf_mode()]

        #Truck
        if self.mode.get_name() == "Truck":

            distance = faf["avr_dom_dist_km"].mean()

            for key in self.mode.get_impacts():
                domestic = self.mode.get_impacts()[key] *= distance
            for key in self.mode.get_impacts():
                foreign = self.mode.get_impacts()[key] *= 200
            self.na = domestic + foreign

        #Rail
        if self.mode.get_name() == "Rail":
            
            distance = cfaf["Average_Distance_per_Shipment"].mean()
            for key in self.mode.get_impacts():
                self.na = self.mode.get_impacts()[key] *= distance

        #Water
        if self.mode.get_name() == "Water":

            # can be filter by truck or avrage of all modes
            distance = faf["avr_dom_dist_km"].mean()

            for key in self.mode.get_impacts():

                if self.mode_domestic is not None:
                    domestic = self.mode_domestic.get_impacts()[key] *= distance
                else:
                    domestic = emission[(emission["mode_name"] == "Truck") & (emission["eff"] == 1)][key].mean() * distance
            
            for key in self.mode.get_impacts():
                
                if self.shipping_org is not None:
                    marine_dis = marine[(marine["Region"]== self.shipping_org.get_continent())].mean()
                else:
                    marine_dis = marine[marine["Region"]].mean()

                foreign = self.mode.get_impacts()[key] *= marine_dis

            self.global_ = domestic + foreign


        #Air
        if self.mode.get_name() == "Air":

            if self.project.get_location() is not None:
                dest_location = self.project.get_location().get_cordinates()
            else:
                dest_location = (39.8283, -98.5795) #USA middle

            if self.shipping_org is not None:
                org_location = self.shipping_org.get_cordinates()
            else:
                org_location = (31.2304, 121.4737) #Shanghai

            self.global_ = geodesic(org_location, dest_location).km


    def scenario_impact (self):

        if self.scenario == "Local":
            return self.local

        if self.scenario == "Regional":
            return self.regional

        if self.scenario == "Regional_c":
            return self.regional_c

        if self.scenario == "National":
            return self.national

        if self.scenario == "Global":
            return self.global_

    def get_local_impact (self):

        return self.local

    def get_regional_impact (self):

        return self.regional

    def get_regional_c_impact (self):

        return self.regional_c

    def get_national_impact (self):

        return self.national

    def get_global_impact (self):

        return self.global_



if __name__ == '__main__':

    from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager

    data_folder = r"C:\Users\mhtaba\Desktop\pod_lca_git\pod_lca\data\transportation_dataset"
    project = ProjectLogisticManager(name="Building A", location="Seattle", data_folder=data_folder)
    project.create_link ( material="Carpet", qty=1, travel_dist="Local", return_trip_factor=1.5, dist_unit="km", mode= "Truck", eff=1)
    
    print (project.get_impact())