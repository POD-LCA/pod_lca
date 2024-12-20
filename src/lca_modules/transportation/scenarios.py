import pandas as pd

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"



class Scenario:
    
    def __init__(self, project ,scenario, qty, material, mode):

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
        self.qty = qty
        self.material = material
        self.mode = mode
        self.local = None
        self.regional = None
        self.regional_c = None
        self.national = None
        self.na = None
        self.global_ = None

        self.pre_proccesing()

    def pre_proccesing (self):

        data_material = self.project.get_subdataset("EC3 Category to CFS Group mapping")
        cfs = self.project.get_subdataset("cfs_2017")
        #faf = self.project.get_subdataset("FAF561")
        emission = self.project.get_subdataset("Emission")
        #PODlLCA_file_path = self.project.get_subdataset("PODlLDA_transport_dataset")
        # dist_fr = PODlLCA_file_path.parse(sheet_name="MOT")
        # sensitive_material = PODlLCA_file_path.parse(sheet_name="sensitive_material")
        # faf_dist_band = PODlLCA_file_path.parse(sheet_name="faf_dist_band")
        # cfaf = self.project.get_subdataset ("CFAF_C2011-2017_Code_E")
        # dist_fr['fr_inmode'] = dist_fr['fr_inmode'].astype(float)
        # dist_fr['fr_orig'] = dist_fr['fr_orig'].astype(float)

        sctg = data_material[data_material["material"] == self.material].iloc[0,1]

        sctg = int(str(sctg)[:2])
        df = cfs[cfs ["SCTG"] == str(sctg)]

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

            elif self.scenario == "regional_c":
                regional_c = pd.merge (emission, regional_c, on ="MODE")
                regional_c.iloc[:,4:9] = regional_c.iloc[:,4:9].multiply(regional_c['SHIPMT_DIST_ROUTED'], axis=0)
                self.regional_c = regional_c.iloc[:,4:9].mean().to_dict()

            elif self.scenario == "national":
                national = pd.merge (emission, national, on ="MODE")
                national.iloc[:,4:9] = national.iloc[:,4:9].multiply(national['SHIPMT_DIST_ROUTED'], axis=0)
                self.national = national.iloc[:,4:9].mean().to_dict()

            else:
                Print ("error")

        else:

            if self.scenario == "Local":
                local = pd.merge (emission, local, on ="MODE")
                local[local ["mode_name"] == self.mode]
                local.iloc[:,4:9] = local.iloc[:,4:9].multiply(local['SHIPMT_DIST_ROUTED'], axis=0)
                self.local = local.iloc[:,4:9].mean().to_dict()

            elif self.scenario == "Regional":
                regional = pd.merge (emission, regional, on ="MODE")
                regional[regional ["mode_name"] == self.mode]
                regional.iloc[:,4:9] = regional.iloc[:,4:9].multiply(regional['SHIPMT_DIST_ROUTED'], axis=0)
                self.regional = regional.iloc[:,4:9].mean().to_dict()

            elif self.scenario == "Regional_c":
                regional_c = pd.merge (emission, regional_c, on ="MODE")
                regional_c[regional_c ["mode_name"] == self.mode]
                regional_c.iloc[:,4:9] = regional_c.iloc[:,4:9].multiply(regional_c['SHIPMT_DIST_ROUTED'], axis=0)
                self.regional_c = regional_c.iloc[:,4:9].mean().to_dict()

            elif self.scenario == "National":
                national = pd.merge (emission, national, on ="MODE")
                national[national ["mode_name"] == self.mode]
                national.iloc[:,4:9] = national.iloc[:,4:9].multiply(national['SHIPMT_DIST_ROUTED'], axis=0)
                self.national = national.iloc[:,4:9].mean().to_dict()

        
    def scenario_impact (self):

        if self.scenario == "Local":

            return self.local

        if self.scenario == "Regional":

            return self.regional

        if self.scenario == "Regional_c":

            return regional_c

        if self.scenario == "National":

            return national



if __name__ == '__main__':

    scenario = Scenario ("Local", 43.3, "steel", None)