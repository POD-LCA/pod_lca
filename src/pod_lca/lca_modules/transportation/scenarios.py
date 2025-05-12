from utilities.data_imports.data_importer import Data_Importer
from lca_modules.transportation.transport_mode import TransportMode, cfs_mapping
from geopy.distance import geodesic
from lca_modules.location import CFS_DATA_PATH, FAF_CITY_REPRESENTATION, FAF_DOMESTIC_REGION
from lca_modules.location.location import Location

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"


class Scenario:
    """
    Scenario object compute the impact of transportation based on different scenarios.

    Attributes
    ----------
    project : obj.
        Refers to the main project.
    scenario : str.
        Name of the transportation scenario.
        - Scenario can be Local, Regional, Regional_c, National, NA, Global.
        - Local, Regional, Regional_c, National are for US scenarios.
        - NA is for North America scenario.
        - Global is for Global scenario.
        **None** is for the default scenario and shows the average impact of the transportation in the US.
    material : str.
        Name of the material.
    mode : obj.
        Refers to the TransportMode object.
    mode_domestic : obj.
        Refers to the TransportMode object.
    """

    def __init__(self, project ,scenario, material, mode, mode_domestic):
        self.scenario = scenario
        self.project = project
        self.material = material
        self.sctg = None
        self.foreign_dis = 0
        self.domestic_dis = 0
        self.mode = mode
        self.mode_domestic = mode_domestic
        self.shipping_dest = project.get_shipping_dest()
        self.shipping_org = project.get_shipping_org()
        self.scenario_impact = None

        # TODO: create constructor method, and move these to the same place
        self.set_sctg(material)

        if self.scenario in ["Local", "Regional", "Regional_c", "National", "None", "Known_us"]:
            self.pre_us_processing()
        elif self.scenario in ["NA", "Global", "Known"]:
            self.pre_global_processing()

    def set_sctg(self, material ,digit=2):
        """ Get the SCTG code based on the material category.

            Parameters
            ----------
            material : #TODO: add...

            digit: int
                the digit of the SCTG code to retrieve.

            Returns
            -------
            int
                The SCTG code of the material. 
        """
        # TODO: Set the path with a variable in config and refer
        data_material = Data_Importer.csv_to_pandas(r"data\transportation_podlca_material.csv")
        try:
            if material not in data_material["material"].values:
                raise ValueError("material not found in the dataset")
            sctg = data_material[data_material["material"] == material].iloc[0, 1]
            sctg = int(str(sctg)[:digit])

        except Exception as e:
            print("Error:", e)

        self.sctg = sctg
        return self #TODO: Not returning an SCTG code as docstring notes. 
                    #TODO: can this be a static method? only place the self is used is to set the SCTG code.

    @staticmethod
    def faf_region_to_cfs_area_mapping(region):
        """ Map the FAF region to CFS area.

            Parameters
            ----------
            region: str
                The FAF region to map.

            Returns
            -------
            int
                the CFS area code.
        """
        cfs_state_code = Data_Importer.csv_to_pandas(CFS_DATA_PATH)
        faf_domestic_data = Data_Importer.json_to_dict(FAF_DOMESTIC_REGION)

        for key, value in faf_domestic_data.items():
            if region in value:
                state_name = key
                break
        else:
            raise ValueError(f"Region '{region}' not found in FAF data.")

        cfs_code = cfs_state_code[cfs_state_code["State"] == state_name]["Code"].values[0]

        return cfs_code

    @staticmethod
    def cfs_area_to_faf_region_mapping(area):
        """
        Map the CFS area to FAF region.

        Parameters:
        - area: int, the CFS area code to map.

        Returns:
        - str, the FAF region.
        """

        cfs_state_code = Data_Importer.csv_to_pandas(CFS_DATA_PATH)
        faf_domestic_data = Data_Importer.json_to_dict(FAF_DOMESTIC_REGION)

        state_row = cfs_state_code[cfs_state_code["Code"] == area]
        if state_row.empty:
            raise ValueError(f"CFS area code '{area}' not found.")
        state_name = state_row["State"].values[0]

        for key, value in faf_domestic_data.items():
            if key == state_name:
                region = value
                break
        else:
            raise ValueError(f"State '{state_name}' not found in FAF data.")

        return region

    def filter_faf(self, sctg=None, destination=None, origin=None, mode=None, domestic_mode=None, scenario=None):

        cfs_state_code = Data_Importer.csv_to_pandas(CFS_DATA_PATH)
        faf  = Data_Importer.csv_to_pandas(r"data\transportation_faf_dataset.csv")
        Faf_city_representation = Data_Importer.json_to_dict(FAF_CITY_REPRESENTATION)
        failed = False
        
        # SCTG
        try:
            if sctg is not None:
                faf = faf[faf["sctg2"] == sctg]
                if faf.empty:
                    raise ValueError("no data for the selected SCTG code in FAF561 dataset")
        except Exception as e:
            print("Error:", e)
            failed = True
        
        # Destination
        try:
            faf_without_dest = faf.copy()
            if destination is not None:
                faf = faf[faf["dms_dest"].isin(destination.get_faf_domestic_region())]
                
                if faf.empty:

                    faf_region_list = faf["dms_dest"].tolist()
                    faf_to_cfs_code = []
                    for region in faf_region_list:
                        faf_to_cfs_code.append(Scenario.faf_region_to_cfs_area_mapping(region))

                    cfs_lat = []
                    cfs_lon = []

                    for state in faf_to_cfs_code:
                        lat = cfs_state_code[cfs_state_code["Code"] == state]["lat"].values
                        lon = cfs_state_code[cfs_state_code["Code"] == state]["lon"].values

                        if len(lat) > 0 and len(lon) > 0:
                            cfs_lat.append(lat[0])
                            cfs_lon.append(lon[0])

                    coords = list(zip(cfs_lat, cfs_lon))
                    dest_to_org = []
                    
                    for coord in coords:
                        distance = geodesic(coord, self.shipping_dest.get_cordinates()).km
                        dest_to_org.append(distance)

                    cfs_dist = dict(zip(faf_to_cfs_code, dest_to_org))
                    sorted_cfs_dist = dict(sorted(cfs_dist.items(), key=lambda item: item[1]))

                    while faf.empty:
                        closest_state = list(sorted_cfs_dist.keys())[0]
                        faf_region = Scenario.cfs_area_to_faf_region_mapping(closest_state) 
                        faf = faf[faf["dms_dest"].isin(faf_region)] 
                        del sorted_cfs_dist[closest_state]
                        print(f"No location for destination found in FAF, The value shows the closest shipping to the selected destination {closest_state}")
                        for key, value in faf_domestic_data.items():
                            if closest_state in value:
                                closest_state = key
                        self.shipping_dest = Location.from_str(closest_state)
            
            else:
                major_domes = faf["dms_dest"].mode()[0]

                faf_domestic_data = Data_Importer.json_to_dict(FAF_DOMESTIC_REGION)     
                for key, value in faf_domestic_data.items():
                    if major_domes in value:
                        major_domes = key
                self.shipping_dest = Location.from_str(major_domes)

        except Exception as e:
            print("Error:", e)
            failed = True
        
        # Origin
        try:
            if origin is not None:
                faf = faf[faf["fr_orig"] == float(origin.get_faf_foreign_region())]
                faf_without_dest = faf_without_dest[faf_without_dest["fr_orig"] == float(origin.get_faf_foreign_region())]

                if faf.empty:

                    faf_region_list =  faf_without_dest["dms_dest"].tolist()

                    faf_to_cfs_code = []
                    for region in faf_region_list:
                        faf_to_cfs_code.append(Scenario.faf_region_to_cfs_area_mapping(region))

                    cfs_lat = []
                    cfs_lon = []

                    for state in faf_to_cfs_code:
                        lat = cfs_state_code[cfs_state_code["Code"] == state]["lat"].values
                        lon = cfs_state_code[cfs_state_code["Code"] == state]["lon"].values

                        if len(lat) > 0 and len(lon) > 0:
                            cfs_lat.append(lat[0])
                            cfs_lon.append(lon[0])

                    coords = list(zip(cfs_lat, cfs_lon))
                    dest_to_dest = []

                    for coord in coords:
                        distance = geodesic(coord, self.shipping_dest.get_cordinates()).km
                        dest_to_dest.append(distance)

                    cfs_dist = dict(zip(faf_to_cfs_code, dest_to_dest))
                    sorted_cfs_dist = dict(sorted(cfs_dist.items(), key=lambda item: item[1]))

                    while faf.empty:
                        closest_state = list(sorted_cfs_dist.keys())[0]
                        faf_region = Scenario.cfs_area_to_faf_region_mapping(closest_state)
                        faf = faf[faf["dms_dest"].isin(faf_region)]
                        del sorted_cfs_dist[closest_state]
                        print(f"No location for origin and selected destination found in FAF, The value shows the closest shipping to the selected destination with datapoint to the selected origin {closest_state}")
                        for key, value in faf_domestic_data.items():
                            if closest_state in value:
                                closest_state = key
                                self.shipping_dest = Location.from_str(closest_state)
            else:
                
                if scenario == "NA":
                    faf = faf[faf["fr_orig"].isin([801, 802])]
                    faf = faf[faf["fr_orig"] == faf["fr_orig"].mode()[0]]
                    self.shipping_org = Location.from_str(Faf_city_representation[str(int(faf["fr_orig"].mode()[0]))])
                elif scenario == "Global":
                    faf = faf[faf["fr_orig"].isin([801, 802]) == False]
                    faf = faf[faf["fr_orig"] == faf["fr_orig"].mode()[0]]
                    self.shipping_org = Location.from_str(Faf_city_representation[str(int(faf["fr_orig"].mode()[0]))])
            
        except Exception as e:
            print("Error:", e)
            failed = True


        # Mode
        try:
            if mode is not None:
                faf = faf[faf["fr_inmode"] == mode.get_faf_mode()]
                if faf.empty:
                    self.mode = TransportMode("Barge", self.project.get_links()[0].get_efficiency(), self.project)
                    faf = faf[faf["fr_inmode"] == self.mode.get_faf_mode()]
                    print ("No datapoint for selected mode of transportation.Using Barge as the default mode of transportation instead.")
            else:

                self.mode = TransportMode("Barge", self.project.get_links()[0].get_efficiency(), self.project)
                faf = faf[faf["fr_inmode"] == self.mode.get_faf_mode()]
                if faf.empty:
                    raise ValueError("no data for Barge as a mode in FAF561 dataset")

        except Exception as e:
            print("Error:", e)
            failed = True
        
        
        # Domestic Mode
        try:
            if domestic_mode is not None:
                faf = faf[faf["dms_mode"] == domestic_mode.get_faf_mode()]
                if faf.empty:
                    raise ValueError("no data for the selected domestic mode in FAF561 dataset")
            else:
                self.mode_domestic = TransportMode("Truck", self.project.get_links()[0].get_efficiency(), self.project)
                faf = faf[faf["dms_mode"] == self.mode_domestic.get_faf_mode()]
                if faf.empty:
                    raise ValueError("no data for Truck as a domestic mode in FAF561 dataset")

        except Exception as e:
            print("Error:", e)
            failed = True

        return faf, failed

    def filter_cfaf(self, sctg=None):

        cfaf = Data_Importer.csv_to_pandas(r"data\transportation_cfaf_dataset.csv")
        try:
            if sctg is not None:
                cfaf = cfaf[cfaf["SCTG_2digits"] == sctg]
                if cfaf.empty:
                    raise ValueError("no data for the selected SCTG code in cfaf dataset")
        except Exception as e:
            print("Error:", e)

        return cfaf

    def filter_marine(self, destination=None, origin=None, scenario=None):
        
        marine = Data_Importer.csv_to_pandas(r"data\transportation_podlca_marine.csv")
        failed = False
        # Destination
        try:
            if destination is not None:
                marine = marine[marine["Coast"] == destination.us_coast]
                if marine.empty:
                    raise ValueError("no data for the selected destination in Marine dataset")
            else:
                pass

        except Exception as e:
            print("Error:", e)
            failed = True

        # Origin
        try:
            if origin is not None:
                marine = marine[marine["Region"] == origin.get_marine_region()]
                if marine.empty:
                    raise ValueError("no data for the selected origin in Marine dataset")
                
            else:
                if scenario == "NA":
                    marine = marine[marine["Region"].isin(["Canada", "Mexico"])]
                    marine = marine[marine["Region"] == origin.get_marine_region()]

                elif scenario == "Global":
                    marine = marine[marine["Region"].isin(["Canada", "Mexico"]) == False]
                    marine = marine[marine["Region"] == origin.get_marine_region()]
        
        except Exception as e:
            print("Error:", e)

        return marine, failed

    def filter_cfs(self, sctg=None, destination=None, origin=None, mode=None):

        cfs = Data_Importer.csv_to_pandas(r"data\transportation_cfs_dataset.csv")  
        cfs_state_code = Data_Importer.csv_to_pandas(CFS_DATA_PATH)  

        failed = False

        # SCTG
        try:
            if sctg is not None:
                cfs_filtered = cfs[cfs["SCTG"] == sctg]
                if cfs_filtered.empty:
                    raise ValueError("no data for the selected SCTG code in CFS dataset")
                cfs = cfs_filtered
        except Exception as e:
            print("Error:", e)
            failed = True
        
        # Destination
        try:
            if destination is not None:
                cfs_filtered = cfs[cfs["DEST_STATE"] == destination.get_cfs_area()]

                if cfs_filtered.empty:
                    cfs_list = cfs["DEST_STATE"].tolist()
                    cfs_lat = []
                    cfs_lon = []

                    for state in cfs_list:
                        lat = cfs_state_code[cfs_state_code["Code"] == state]["lat"].values
                        lon = cfs_state_code[cfs_state_code["Code"] == state]["lon"].values

                        if len(lat) > 0 and len(lon) > 0:
                            cfs_lat.append(lat[0])
                            cfs_lon.append(lon[0])

                    coords = list(zip(cfs_lat, cfs_lon))
                    dest_to_org = []
                    
                    for coord in coords:
                        distance = geodesic(coord, self.shipping_dest.get_cordinates()).km
                        dest_to_org.append(distance)

                    cfs_dist = dict(zip(cfs_list, dest_to_org))
                    sorted_cfs_dist = dict(sorted(cfs_dist.items(), key=lambda item: item[1]))

                    while cfs_filtered.empty:
                        closest_state = list(sorted_cfs_dist.keys())[0]
                        cfs_filtered = cfs[cfs["DEST_STATE"] == closest_state]
                        del sorted_cfs_dist[closest_state]
                        print(f"No location for destination found in cfs, The value shows the closest shipping to the selected destination {closest_state}")
                        cfs = cfs_filtered
                else:
                    cfs = cfs_filtered
            else:
                pass

        except Exception as e:
            print("Error:", e)
            failed = True

        
        # Origin
        try:
            if origin is not None:
                cfs_filtered = cfs[cfs["ORIG_STATE"] == origin.get_cfs_area()]

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
                        cfs = cfs_filtered
                else:
                    cfs = cfs_filtered
        except Exception as e:
            print("Error:", e)
            failed = True


        # Mode
        try:
            if mode is not None:
                cfs_filtered = cfs[cfs["MODE"].isin(mode.get_cfs_mode())]
                
                if cfs_filtered.empty:
                    self.mode = TransportMode("Truck", self.project.get_links()[0].get_efficiency(), self.project)
                    cfs_filtered = cfs[cfs["MODE"].isin(self.mode.get_cfs_mode())]
                    cfs = cfs_filtered
                    print ("Using Truck as the default mode of transportation instead.")

                else:
                    cfs = cfs_filtered  
            else:
                self.mode = TransportMode("Truck", self.project.get_links()[0].get_efficiency(), self.project)
                cfs_filtered = cfs[cfs["MODE"].isin(self.mode.get_cfs_mode())]
                cfs = cfs_filtered
                print ("Using Truck as the default mode of transportation instead.")       
        except Exception as e:
            print("Error:", e)
            failed = True


        return cfs, failed

    def pre_us_processing(self):
        """
        process the data for the US scenarios.

        This function is used to process the data for the US scenarios.

        1. it filters the data based on the shipping destination.
            - if there is no shipping destination it will select the closest shipping destination.
            - if the shipping destination is note defined it will selcet the average shipping destination.

        2. it filters the data based on the shipping origin.
            - if there is no shipping origin it will select the closest shipping origin.
            - if the shipping origin is note defined it will selcet the average shipping origin.
        
        3. it filters the data based on the mode of transportation.
            - if the mode is not selected, it will select the most frequent mode of transportation.

        4. it calculates the distance of the shipping based on the quartiles of the shipping distance.

        """

        
        cfs = self.filter_cfs(self.sctg, self.shipping_dest, self.shipping_org, self.mode)
        if cfs[1] == True:
            print (" An error occurred while filtering the data, please check the data and try again.")
            self.scenario_impact = 0* self.mode.get_impacts()

        else:
            cfs = cfs[0]

            try:
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


                if self.scenario == "Local":
                    self.domestic_dis = cfs[cfs["quartile"] == "Q1"]["SHIPMT_DIST_ROUTED"].mean()
                    self.scenario_impact = self.domestic_dis * impact

                elif self.scenario == "Regional":
                    self.domestic_dis = cfs[cfs["quartile"] == "Q2"]["SHIPMT_DIST_ROUTED"].mean()
                    self.scenario_impact = self.domestic_dis * impact
                
                elif self.scenario == "Regional_c":
                    self.domestic_dis = cfs[cfs["quartile"] == "Q3"]["SHIPMT_DIST_ROUTED"].mean()
                    self.scenario_impact = self.domestic_dis * impact
                
                elif self.scenario == "National":
                    self.domestic_dis = cfs[cfs["quartile"] == "Q4"]["SHIPMT_DIST_ROUTED"].mean()
                    self.scenario_impact = self.domestic_dis * impact
                
                elif self.scenario == "None" or self.scenario == "Known_us":
                    self.domestic_dis = cfs["SHIPMT_DIST_ROUTED"].mean()
                    self.scenario_impact = self.domestic_dis * impact
            except:
                self.scenario_impact = 0* self.mode.get_impacts()
                
    def pre_global_processing (self):
        """
        process the data for the North America and Global scenarios.

        This function is used to process the data for the North America and Global scenarios.


        1. it filters the data based on the shipping destination.
            - if there is no shipping destination it will select the most frequent shipping destination.

        2. it filters the data based on the shipping origin.

        3. it filters the data based on the mode of transportation.
            - if the mode is not defined it will select Barge as the mode of transportation.

        4. it filters the data based on the domestic mode of transportation.
            - if the mode is not defined it will select Truck as the domestic mode of transportation.
            
        """
        faf = self.filter_faf(self.sctg, self.shipping_dest, self.shipping_org, self.mode, self.mode_domestic, self.scenario)
        marine = self.filter_marine(self.shipping_dest, self.shipping_org, self.scenario)
        cfaf = self.filter_cfaf(self.sctg)

        if faf[1] == True:
            print (" An error occurred while filtering the FAF data, please check the data and try again.")
            self.scenario_impact = 0* self.mode.get_impacts()
        else:
            faf = faf[0]

        if marine[1] == True:
            print (" An error occurred while filtering the Marine data, please check the data and try again.")
        else:
            marine = marine[0]

        try:
            if self.mode.get_name() == "Truck":
                self.domestic_dis = faf["avr_dom_dist_km"].mean()
                self.foreign_dis = 200
                domestic_dis = self.domestic_dis + self.foreign_dis
                self.scenario_impact = domestic_dis * self.mode.get_impacts()
            
            elif self.mode.get_name() == "Rail":
                self.foreign_dis = cfaf["Average_Distance_per_Shipment"].mean()
                self.scenario_impact = self.foreign_dis * self.mode.get_impacts()

            elif self.mode.get_name() in ("Barge", "Ocean"):
                self.domestic_dis = faf["avr_dom_dist_km"].mean()
                self.foreign_dis = marine["Distance_km"].mean()
                domestic_dis = self.domestic_dis + self.foreign_dis
                self.scenario_impact = domestic_dis * self.mode.get_impacts()
            
            elif self.mode.get_name() == "Air":

                dms_coordinates = self.shipping_dest.get_cordinates()
                fr_coordinates = self.shipping_org.get_cordinates()
                self.foreign_dis = geodesic(dms_coordinates, fr_coordinates).km
                self.scenario_impact = self.foreign_dis * self.mode.get_impacts()
        except:

            self.foreign_dis = 0
            self.domestic_dis = 0
            self.scenario_impact = 0* self.mode.get_impacts()

    def get_scenario_impact (self):
        """ Return the impact of the transportation based on the scenario.
        """
        return self.scenario_impact

    def get_distances (self):
        """ Return the distances of the transportation based on the scenario.
        """
        if self.scenario in ["Local", "Regional", "Regional_c", "National", "None", "NA", "Global", "Known", "Known_us"]:
            return self.domestic_dis, self.foreign_dis



if __name__ == '__main__':
    
    pass