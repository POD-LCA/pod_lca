__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"



class Scenario:
    
    def __init__(self, scenario, qty, material, mode):

        self.scenario = scenario
        self.qty = qty
        self.material = material
        self.mode = mode
        self.local = None
        self.regional = None
        self.regional_c = None
        self.national = None
        self.na = None
        self.global_ = None
        self.report = None

        pre_proccesing()

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

        sctg = data_material[data_material["material"] == self.material].loc[0,"SCTG"]
        sctg = int(str(sctg)[:2])
        df = cfs[cfs ["SCTG"] == sctg]

        df = df["SHIPMT_DIST_ROUTED"].quantile([0.25, 0.5, 0.75]).values

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


        local_dis = local["distance"].mean()
        regional_dis = regional["distance"].mean()
        regional_c_dis = regional_c["distance"].mean()
        national_dis = national["distance"].mean()

        else:
            
            local = local[local['MODE'] == self.mode].mean()
            regional = regional[regional['MODE'] == self.mode].mean()
            regional_c = regional_c[regional['MODE'] == self.mode].mean()
            national = national[regional['MODE'] == self.mode].mean()


    def scenario_impact (self):

        if self.scenario == "Local":

            if self.mode == None:
                
                for mode in 
                


            return {'GWP': 7650.0, 'AP': 3450.0, 'EP': 7200.0, 'ODP': 7950.0, 'SFP': 8100.0}

        if self.scenario == "Regional":

            return {'GWP': 7650.0, 'AP': 3450.0, 'EP': 7200.0, 'ODP': 7950.0, 'SFP': 8100.0}

        if self.scenario == "Regional_c":

            return {'GWP': 7650.0, 'AP': 3450.0, 'EP': 7200.0, 'ODP': 7950.0, 'SFP': 8100.0}

        if self.scenario == "National":

            return {'GWP': 7650.0, 'AP': 3450.0, 'EP': 7200.0, 'ODP': 7950.0, 'SFP': 8100.0}



if __name__ == '__main__':

    scenario = Scenario ("Local", 43.3, "steel", None)