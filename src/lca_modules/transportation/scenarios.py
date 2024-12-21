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

        self.pre_processing()

    def pre_processing (self):

        data_material = self.project.get_subdataset("EC3 Category to CFS Group mapping")
        cfs = self.project.get_subdataset("cfs_2017")
        emission = self.project.get_subdataset("Emission")
        cfs= cfs.drop(columns=["SHIPMT_ID","QUARTER","SHIPMT_VALUE","TEMP_CNTL_YN","EXPORT_CNTRY","HAZMAT","WGT_FACTOR", "ORIG_MA","ORIG_CFS_AREA","DEST_MA","DEST_CFS_AREA"])

        sctg = data_material[data_material["material"] == self.material].iloc[0,1]
        sctg = int(str(sctg)[:2])
        df = cfs[cfs ["SCTG"] == str(sctg)].copy()
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

        df.loc[:, 'quartile'] = df["SHIPMT_DIST_ROUTED"].apply(assign_quartile, args=(quartiles[0], quartiles[1], quartiles[2]))

        local = df[df['quartile'] == 'Q1']
        regional = df[df['quartile'] == 'Q2']
        regional_c = df[df['quartile'] == 'Q3']
        national = df[df['quartile'] == 'Q4']

        if self.mode == None:

            if self.scenario == "Local":
                local = pd.merge (emission, local, on ="MODE")
                local.iloc[:,4:9] = local.iloc[:,4:9].multiply(local['SHIPMT_DIST_ROUTED'], axis=0)
                self.local = local.iloc[:,4:9].mean().to_dict()

            elif self.scenario == "Regional":
                regional = pd.merge (emission, regional, on ="MODE")
                regional.iloc[:,4:9] = regional.iloc[:,4:9].multiply(regional['SHIPMT_DIST_ROUTED'], axis=0)
                self.regional = regional.iloc[:,4:9].mean().to_dict()

            elif self.scenario == "Regional_c":
                regional_c = pd.merge (emission, regional_c, on ="MODE")
                regional_c.iloc[:,4:9] = regional_c.iloc[:,4:9].multiply(regional_c['SHIPMT_DIST_ROUTED'], axis=0)
                self.regional_c = regional_c.iloc[:,4:9].mean().to_dict()

            elif self.scenario == "National":
                national = pd.merge (emission, national, on ="MODE")
                national.iloc[:,4:9] = national.iloc[:,4:9].multiply(national['SHIPMT_DIST_ROUTED'], axis=0)
                self.national = national.iloc[:,4:9].mean().to_dict()

            else:
                print ("error")

        else:

            if self.scenario == "Local":
                local = pd.merge (emission, local, on ="MODE")
                local = local[local ["mode_name"] == self.mode]
                local.iloc[:,4:9] = local.iloc[:,4:9].multiply(local['SHIPMT_DIST_ROUTED'], axis=0)
                self.local = local.iloc[:,4:9].mean().to_dict()

            elif self.scenario == "Regional":
                regional = pd.merge (emission, regional, on ="MODE")
                regional = regional[regional ["mode_name"] == self.mode]
                regional.iloc[:,4:9] = regional.iloc[:,4:9].multiply(regional['SHIPMT_DIST_ROUTED'], axis=0)
                self.regional = regional.iloc[:,4:9].mean().to_dict()

            elif self.scenario == "Regional_c":
                regional_c = pd.merge (emission, regional_c, on ="MODE")
                regional_c = regional_c[regional_c ["mode_name"] == self.mode]
                regional_c.iloc[:,4:9] = regional_c.iloc[:,4:9].multiply(regional_c['SHIPMT_DIST_ROUTED'], axis=0)
                self.regional_c = regional_c.iloc[:,4:9].mean().to_dict()

            elif self.scenario == "National":
                national = pd.merge (emission, national, on ="MODE")
                national = national[national ["mode_name"] == self.mode]
                national.iloc[:,4:9] = national.iloc[:,4:9].multiply(national['SHIPMT_DIST_ROUTED'], axis=0)
                self.national = national.iloc[:,4:9].mean().to_dict()

        
    def scenario_impact (self):

        if self.scenario == "Local":
            return self.local

        if self.scenario == "Regional":
            return self.regional

        if self.scenario == "Regional_c":
            return self.regional_c

        if self.scenario == "National":
            return self.national

    def get_local_impact (self):

        return self.local

    def get_regional_impact (self):

        return self.regional

    def get_regional_c_impact (self):

        return self.regional_c

    def get_national_impact (self):

        return self.national



if __name__ == '__main__':

    from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager

    data_folder = r"C:\Users\mhtaba\Desktop\pod_lca_git\pod_lca\data\transportation_dataset"
    project = ProjectLogisticManager(name="Building A", location="Seattle", data_folder=data_folder)
    project.create_link ( material="Carpet", qty=200, travel_dist="Local", return_trip_factor=1.5, dist_unit="km", mode= None, eff=0.9)
    print (project.get_impact())