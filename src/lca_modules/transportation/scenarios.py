__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"



class Scenario:
    
    def __init__(self, scenario):

        self.scenario = scenario
        self.modes = []
        self.report = None

    def pre_proccesing (self):

        data_material = self.project.get_subdataset("EC3 Category to CFS Group mapping")
        cfs = self.project.get_subdataset("cfs_2017")
        faf = self.project.get_subdataset("FAF561")
        emission = self.project.get_subdataset("Emission")
        PODlLCA_file_path = self.project.get_subdataset("PODlLDA_transport_dataset")
        dist_fr = PODlLCA_file_path.parse(sheet_name="MOT")
        sensitive_material = PODlLCA_file_path.parse(sheet_name="sensitive_material")
        faf_dist_band = PODlLCA_file_path.parse(sheet_name="faf_dist_band")
        cfaf = self.project.get_subdataset ("CFAF_C2011-2017_Code_E")
        

        dist_fr['fr_inmode'] = dist_fr['fr_inmode'].astype(float)
        dist_fr['fr_orig'] = dist_fr['fr_orig'].astype(float)




    def scenario_impact (self):

        if self.scenario == "Local":







            return {'GWP': 7650.0, 'AP': 3450.0, 'EP': 7200.0, 'ODP': 7950.0, 'SFP': 8100.0}

        if self.scenario == "Regional":

            return {'GWP': 7650.0, 'AP': 3450.0, 'EP': 7200.0, 'ODP': 7950.0, 'SFP': 8100.0}

        if self.scenario == "Regional_c":

            return {'GWP': 7650.0, 'AP': 3450.0, 'EP': 7200.0, 'ODP': 7950.0, 'SFP': 8100.0}

        if self.scenario == "National":

            return {'GWP': 7650.0, 'AP': 3450.0, 'EP': 7200.0, 'ODP': 7950.0, 'SFP': 8100.0}