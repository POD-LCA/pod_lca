import pandas as pd

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"



class Scenario:
    
    def __init__(self, project ,scenario, material, mode):

        """
        Scenario object compute the impact of transportation based on different scenarios.

        Attributes
        ----------
        scenario : str.
            name of the transportation scenario.

        material : str.
            name of the material.

        qty : str.
            quantity of the of the material.

        travel_dist : float.
            transportation distance.

        return_trip_factor : float.
            transportation return trip factor.

        dist_unit : str.
            transportation distance unit.

        mode : str.
            transportation mode (ex: truck, rail).

        eff : str.
            transportation mode efficiency (ex: high, medium).

        shipping_org : str.
            origin of the transportation.

        """

        self.scenario = scenario
        self.project = project
        self.material = material
        self.mode = mode
        self.local = None
        self.regional = None
        self.regional_c = None
        self.national = None
        self.na = None
        self.global_ = None

        self.pre_us_processing()
        #self.pre_global_processing()

    def pre_us_processing(self):


        data_material = self.project.get_subdataset("EC3 Category to CFS Group mapping")
        cfs = self.project.get_subdataset("cfs_2017")
        emission = self.project.get_subdataset("Emission")
        cfs = cfs.drop(columns=["SHIPMT_ID", "QUARTER", "SHIPMT_VALUE", "TEMP_CNTL_YN", "EXPORT_CNTRY",
                                "HAZMAT", "WGT_FACTOR", "ORIG_MA", "ORIG_CFS_AREA", "DEST_MA", "DEST_CFS_AREA"])

        sctg = data_material[data_material["material"] == self.material].iloc[0, 1]
        sctg = int(str(sctg)[:2])
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

        def process_scenario(df, emission, mode=None):
            df = pd.merge(emission, df, left_on="mode_cfs", right_on="MODE")
            if mode:
                df = df[df["mode_name"] == mode]
            impact_cols = df.columns[4:9]
            df[impact_cols] = df[impact_cols].multiply(df["SHIPMT_DIST_ROUTED"], axis=0)
            return df[impact_cols].mean().to_dict()

        # Process all scenarios dynamically
        for scenario_name, scenario_df in quartile_mapping.items():
            impact = process_scenario(scenario_df, emission, mode=self.mode)
            setattr(self, scenario_name.lower(), impact)

    

    # def pre_global_processing (self):

    #     data_material = self.project.get_subdataset("EC3 Category to CFS Group mapping")
    #     emission = self.project.get_subdataset("Emission")
    #     faf = pd.read_csv (r"temp\transportation_dataset\FAF561.csv")
    #     PODlLCA_file_path = self.project.get_subdataset("PODlLDA_transport_dataset")
    #     dist_fr = PODlLCA_file_path.parse(sheet_name="MOT")
    #     sensitive_material = PODlLCA_file_path.parse(sheet_name="sensitive_material")
    #     faf_dist_band = PODlLCA_file_path.parse(sheet_name="faf_dist_band")
    #     cfaf = self.project.get_subdataset ("CFAF_C2011-2017_Code_E")

    #     faf = faf[faf['tons_2017'] != 0]
    #     faf.dropna(subset=['fr_orig'], inplace=True)
    #     faf_filtered = faf[faf['trade_type'] == 2]

    #     #Remove unrelated columns
    #     columns_to_remove = ["fr_dest", "fr_outmode"]
    #     columns_to_remove += faf.columns[18:]

    #     faf_cleaned = faf.drop(columns=columns_to_remove)
    #     faf_merged = faf_cleaned.merge(faf_dist_band, on='dist_band', how='left')
    #     faf_merged['min_dom_dist_km'] = faf_merged['min_dom_dist'] * 1.60934
    #     faf_merged['max_dom_dist_km'] = faf_merged['max_dom_dist'] * 1.60934
    #     faf_merged = faf_merged.merge(mot[['dms_mode', 'gwp_mean']].rename(columns={'gwp_mean': 'dom_mot_emi'}), on='dms_mode', how='left')
    #     faf_merged['min_dom_emi'] = faf_merged['min_dom_dist_km'] * faf_merged['dom_mot_emi']
    #     faf_merged['max_dom_emi'] = faf_merged['max_dom_dist_km'] * faf_merged['dom_mot_emi']

    #     faf_merged['ave_dom_emi'] = (faf_merged['min_dom_emi'] + faf_merged['max_dom_emi']) / 2
    #     faf_merged.dropna(subset=['dom_mot_emi'], inplace=True)
    #     faf_merged = faf_merged[faf_merged['max_dom_emi'].notna()]
    #     faf_merged.drop(columns=['min_dom_dist', 'max_dom_dist', 'min_dom_dist_km', 'max_dom_dist_km'], inplace=True)
    #     faf = faf_merged
    #     faf = faf.merge(mot[['fr_inmode', 'gwp_mean']].rename(columns={'gwp_mean': 'fr_mot_emi'}), on='fr_inmode', how='left')
    #     faf['fr_orig'] = faf['fr_orig'].astype(int)
    #     dist_fr['fr_orig'] = dist_fr['fr_orig'].astype(int)
    #     faf = faf.merge(dist_fr[['fr_orig', 'fr_inmode', 'fr_dist']], on=['fr_orig', 'fr_inmode'], how='left')
    #     faf = faf.dropna(subset=['fr_dist'])
    #     faf['fr_in_emi']= faf['fr_dist'] * faf['fr_mot_emi']
    #     faf['fr_emi']=faf['fr_in_emi'] +faf["ave_dom_emi"]




    #     sctg = data_material[data_material["material"] == self.material].iloc[0,1]
    #     sctg = int(str(sctg)[:2])



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
    #project.create_link ( material="Carpet", qty=1, travel_dist="Global", return_trip_factor=1.5, dist_unit="km", mode= "Truck", eff=0.9)
    
    scenario = Scenario(project, "Local", "Carpet", None)
    print (scenario.get_regional_impact())
    #print (project.get_impact())