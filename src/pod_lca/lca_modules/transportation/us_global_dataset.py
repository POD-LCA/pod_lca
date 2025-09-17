
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from geopy.distance import geodesic

from . import TransportDataset
from . import TransportMode
from ..location import Location
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class USGlobalDataset(TransportDataset):
    """ A class to handle transportation of goods to US from global origins.
    
    Attributes
    ----------
    force_location : bool
        If true, when location (origin/destination) not found in the dataset, use closest location.
    faf : ~pandas.DataFrame
        Pre-processed dataset from FAF.
    cfaf : ~pandas.DataFrame
        Pre-processed dataset from CFAF.
    marine : ~pandas.DataFrame
        Marine dataset.
    """

    def __init__(self):
        self.force_location = False
        self.faf  = DataImporter.csv_to_pandas(config['file_paths']['transportation']['FAF_DATA_PATH'])
        self.marine = DataImporter.csv_to_pandas(config['file_paths']['transportation']['MARINE_DATA_PATH']) 
        self.cfaf = DataImporter.csv_to_pandas(config['file_paths']['transportation']['CFAF_DATA_PATH'])
    
    def filter_datasets(self, material=None, destination=None, origin=None, mode_domestic=None, mode_foreign=None):
        """ Filter all datasets corresponding to foreign travel.

        Parameters
        ----------
        material : ~pod_lca.materials_screening.Master
            The Standard Classification of Transported Goods (SCTG) code to filter by.
        destination : ~pod_lca.location.Location
            The destination location to filter by.
        origin : ~pod_lca.location.Location
            The origin location to filter by.
        mode_domestic : ~pod_lca.transportation.TransportMode
            The foreign transportation mode to filter by.
        mode_foreign :  ~pod_lca.transportation.TransportMode
            The domestic transportation mode to filter by.

        Returns
        -------
        :class:`pandas.DataFrame`
            The filtered FAF dataset.
        :class:`pandas.DataFrame`
            The filtered marine dataset.
        :class:`pandas.DataFrame`
            The filtered cfaf dataset.     
        """
        sctg_code = material.get_sctg_code(digits=2)

        if mode_foreign is not None:
            mode_name = mode_foreign.get_name()
            if mode_name == "Truck":
                faf = self.filter_faf(sctg_code, destination, origin, mode_foreign, mode_domestic)
                marine = None
                cfaf = None
            elif mode_name == "Rail":
                faf = None
                marine = None
                cfaf = self.filter_cfaf(sctg_code)
            elif mode_name == "Ocean":
                faf = self.filter_faf(sctg_code, destination, origin, mode_foreign, mode_domestic)
                marine = self.filter_marine(destination, origin)
                cfaf = None
            elif mode_name == "Air":
                faf = None
                marine = None
                cfaf = None
            else:
                raise ValueError(f"Invalid mode of transportation: {mode_name}. Must be one of 'Truck', 'Rail', 'Ocean', or 'Air'.")
        else:       
            faf = self.filter_faf(sctg_code, destination, origin, mode_foreign, mode_domestic)
            marine = self.filter_marine(destination, origin)
            cfaf = self.filter_cfaf(sctg_code)

        return faf, marine, cfaf
    
    def filter_faf(self, sctg=None, destination=None, origin=None, mode_foreign=None, mode_domestic=None):
        """ Filter FAF data.

        Parameters
        ----------
        sctg : int
            The Standard Classification of Transported Goods (SCTG) code to filter by.
        destination : ~pod_lca.location.Location
            The destination location to filter by.
        origin : ~pod_lca.location.Location
            The origin location to filter by.
        mode_domestic :  ~pod_lca.transportation.TransportMode
            The foreign transportation mode to filter by.
        mode_foreign :  ~pod_lca.transportation.TransportMode
            The domestic transportation mode to filter by.

        Returns
        -------
        pandas.DataFrame
            The filtered FAF dataset.

        Raises
        ------
        ValueError
            If no data is found for the provided SCTG code, destination, or mode.         
        """
        faf = self.faf
                
        # SCTG
        if sctg is not None:
            faf = faf[faf["sctg2"] == sctg]
            if faf.empty:
                raise ValueError("Material not found in FAF561 dataset")

        # Mode
        if isinstance(mode_foreign, TransportMode):
            faf_modes_mapping = DataImporter.json_to_dict(config['file_paths']['transportation']['FAF_MODE_CODE'])
            faf_filtered = faf[faf["fr_inmode"] == faf_modes_mapping[mode_foreign.get_name()]]
            if faf_filtered.empty:
                raise ValueError("Transportation mode not in FAF dataset.")
            faf = faf_filtered
        
        # Domestic Mode
        if mode_domestic is not None:
            faf_modes_mapping = DataImporter.json_to_dict(config['file_paths']['transportation']['FAF_MODE_CODE'])
            faf_filtered = faf[faf["dms_mode"] == faf_modes_mapping[mode_domestic.get_name()]]
            if faf_filtered.empty:
                raise ValueError("Transportation mode not in dataset")
            faf = faf_filtered

        # Origin
        if isinstance(origin, Location):
            faf_filtered = faf[faf["fr_orig"] == float(origin.get_faf_foreign_region())]
            if faf_filtered.empty:
                raise ValueError("Origin not in FAF dataset.")
            faf = faf_filtered

        # Destination
        if isinstance(destination, Location):
            faf_filtered = faf[faf["dms_dest"].isin(destination.get_faf_domestic_region())]
            if faf_filtered.empty:
                if self.force_location:
                    closest_state_name, closest_faf_region_codes = Location.get_closest_regions_FAF(origin, faf["dms_dest"].tolist())
                    faf_filtered = faf[faf["dms_dest"].isin(closest_faf_region_codes)]
                    log(f"Closest state to {destination.get_location_name()}, {closest_state_name}, is used to estimate travel distance.", "Info")
                else:
                    raise ValueError("Destination not in CFS Dataset.")
            faf = faf_filtered

        return faf

    def filter_cfaf(self, sctg):
        """ Filter Canadian Freight Analysis Framework (CFAF) dataset by material SCTG code.
        
        Parameters
        ----------
        sctg : int
            Two-digit SCTG code of the material.

        Returns
        -------
        pandas.DataFrame
            Filtered CFAF dataset.

        Raises
        ------
        ValueError
            Material not found in cfaf dataset.
        """
        cfaf = self.cfaf
        if isinstance(sctg, int):
            cfaf = cfaf[cfaf["SCTG_2digits"] == sctg]
            if cfaf.empty:
                raise ValueError("Material not found in cfaf dataset")

        return cfaf

    def filter_marine(self, destination=None, origin=None):
        """ Filter marine data.
        
        Parameters
        ----------
        destination : ~pod_lca.location.Location
            Final destination of the product.
        origin : ~pod_lca.location.Location
            Origin of the travel.
        scenario : str
            Transportation scenario considered.

        Returns
        -------
        pandas.DataFrame
            Filtered marine dataset.

        Raises
        ------
        ValueError
            No data for the selected origin in marine dataset
        """
        marine = self.marine
        
        # Destination
        if isinstance(destination, Location):
            marine = marine[marine["Coast"] == destination.get_us_coast()]
            if marine.empty:
                raise ValueError("No data for the selected destination in marine dataset")
        else:
            pass

        # Origin 
        if isinstance(origin, Location):
            marine = marine[marine["Region"] == origin.get_faf_foreign_region(type='name')]
            if marine.empty:
                raise ValueError("No data for the selected origin in marine dataset")
        
        return marine
    
    @staticmethod
    def get_distance_estimate(fltered_datasets, destination, origin, mode_name):
        """ Get the average travel distance based on shipping destination, origin, and mode of transportation.
        
        Parameters
        ----------
        filtered_datasets : tuple
            Filtered datasets as pandas dataframes.
        destination : ~pod_lca.location.Location
            Final destination of the product.
        origin : ~pod_lca.location.Location
            Origin of the travel.
        mode_name : {'Truck', 'Rail', 'Ocean', 'Air'}
            Transportation mode

        Returns
        -------
        :class:`float`
            Travel distance of the domestic leg of travel.
        :class:`float`
            Travel distance of the foreign leg of travel.

        Raises
        ------
        ValueError
            Invalid mode of transportation.
        """
        faf, marine, cfaf = fltered_datasets

        if mode_name == "Truck":
            domestic_dis = faf["avr_dom_dist_km"].mean()
            foreign_dis = 200.0
        elif mode_name == "Rail":
            domestic_dis = 0.0
            foreign_dis = cfaf["Average_Distance_per_Shipment"].mean()
        elif mode_name == "Ocean":
            domestic_dis = faf["avr_dom_dist_km"].mean()
            foreign_dis = marine["Distance_km"].mean()
        elif mode_name == "Air":
            if destination.get_cordinates() is None:
                destination.set_cordinates()
            dms_coordinates = destination.get_cordinates()
            if origin.get_cordinates() is None:
                origin.set_cordinates()
            fr_coordinates = origin.get_cordinates()

            domestic_dis = 0.0
            foreign_dis = geodesic(dms_coordinates, fr_coordinates).km
        else:
            raise ValueError(f"Invalid mode of transportation: {mode_name}. Must be one of 'Truck', 'Rail', 'Ocean', or 'Air'.")

        return domestic_dis, foreign_dis


if __name__ == '__main__':
    pass
