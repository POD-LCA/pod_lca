
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from .logistics_link import LogisticLink
from ..location import Location
from ..transportation import TransportMode
from ...units import KILOMETER
from ...units import MILE
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class DomesticLink(LogisticLink):
    """ A link of domestic US transportation.
    """
    # ================================
    # Setters and Getters
    # ================================  
    def set_travel_dist(self, 
                        travel_dist, 
                        travel_dist_unit:(str) = KILOMETER, 
                        return_trip_factor:(float) = None):
        """ Set the travel distance of the transportation link.

        Parameters
        ----------
        travel_dist : float or str
            travel distance of the transportation link.
        travel_dist_unit : str, optional
            Distance unit of the travel distance (default is "km").
        return_trip_factor : float, optional
            Return trip factor of the transportation link (default is None).
        """
        self.travel_dist_unit = travel_dist_unit

        if isinstance(travel_dist, (float, int)):
            self.travel_dist = travel_dist

        elif travel_dist is None:
            transport_scenario = self.get_transport_scenario()
            if transport_scenario in ["Local", "Regional", "Regional_c", "National", "None", "Known_us", None]:
                try:
                    self.travel_dist = self.get_distance_from_cfs(transport_scenario)
                except ValueError as e:
                    if str(e) == "Transportation mode in CFS dataset":
                        log(f"Transportation mode not found in CFS dataset. Using default mode 'Truck'.", "Warn")
                        self.set_mode('Truck', self.get_mode().get_fuel_type(), self.get_mode().get_efficiency())
                        self.travel_dist = self.get_distance_from_cfs(transport_scenario)

                if self.get_next() is not None:
                    self.get_next().set_travel_dist(0, travel_dist_unit, return_trip_factor)

            elif transport_scenario in ["North_america", "Global", "Known"]:
                pass
                # TODO: create foreign link if it does not exist
                # TODO: update the lengths
            else:
                raise ValueError("Transport scenario not recognized.")
            
        else:
            raise ValueError("Either travel distance or transport scenario must be provided.")
        
        self.return_trip_factor = return_trip_factor

        return self

    def get_return_trip_factor(self):   
        """ Retrieve the return trip factor of the transportation link.

        Returns
        -------
        float
            The return trip factor of the transportation link.
        """
        if self.return_trip_factor is None: # Default return trip factor
            dist = self.get_travel_dist()
            convertion_factor = self.get_dist_unit().get_conversion_factor(MILE)

            return 1.5 if dist * convertion_factor < 500 else 1.0
        
        else: # user set value
            return self.return_trip_factor

    # ================================
    # CFS Methods
    # ================================
    def get_distance_from_cfs(self, transport_scenario):
        """ Get the average distance from the CFS dataset based on the scenario.

        Parameters
        ----------
        scenario : str
            The scenario to filter the distances by.

        Returns
        -------
        float
            The distance estimate for the specified scenario.
        """
        convertion_factor = self.get_dist_unit().get_conversion_factor(KILOMETER)
        sctg_code = CFSDataset.get_sctg_code(self.get_material().get_name())
        cfs_filtered = CFSDataset.filter_datasets(sctg_code, self.get_shipping_dest(), self.get_shipping_org(), self.get_mode())
        travel_dist = CFSDataset.get_distance_estimate(cfs_filtered, transport_scenario) * convertion_factor

        return travel_dist


class CFSDataset:
    """ A class to handle the CFS dataset for transportation links.
    """

    @staticmethod
    def get_sctg_code(material ,digit=2):
        """ Get the SCTG code based on the material category.

        Parameters
        ----------
        material : str
            The material category for which to retrieve the SCTG code.
        digit: int
            the digit of the SCTG code to retrieve.

        Returns
        -------
        int
            The SCTG code of the material.

        Raises
        ------
        ValueError
            If the material is not found in the dataset.
        """
        data_material = DataImporter.csv_to_pandas(config['file_paths']['transportation']['CFS_SCTG_CODE'])
        if material not in data_material["material"].values:
            raise ValueError("material not found in the dataset")
        
        sctg = data_material[data_material["material"] == material].iloc[0, 1]
        sctg = int(str(sctg)[:digit])

        return sctg

    @staticmethod
    def filter_datasets(sctg=None, destination=None, origin=None, mode=None):
        """ Filter the CFS dataset based on the provided parameters.
        
        Parameters
        ----------
        sctg : int, optional
            The Standard Classification of Transported Goods (SCTG) code to filter by.
        destination : Location, optional
            The destination location to filter by.
        origin : Location, optional
            The origin location to filter by.
        mode : TransportMode, optional
            The transportation mode to filter by.
        
        Returns
        -------
        pandas.DataFrame
            The filtered CFS dataset.
        
        Raises
        ------
        ValueError
            If no data is found for the provided SCTG code, destination, or mode.
        """
        cfs = DataImporter.csv_to_pandas(config['file_paths']['transportation']['CFS_DATA_PATH'])  
         
        # filter SCTG code
        if isinstance(sctg, int):
            cfs_filtered = cfs[cfs["SCTG"] == sctg]
            if cfs_filtered.empty:
                raise ValueError("Material not found in the CFS dataset")
            cfs = cfs_filtered

        # Destination
        if isinstance(destination, Location):
            cfs_filtered = cfs[cfs["DEST_STATE"] == destination.get_cfs_area()]
            if cfs_filtered.empty:
                cfs_state_list = cfs["DEST_STATE"].tolist()
                closest_state_name, closest_state_code = Location.get_closest_states(destination, cfs_state_list)
                cfs_filtered = cfs[cfs["DEST_STATE"] == closest_state_code]
                log(f"Closest state to {destination.get_location_name()}, {closest_state_name}, is used to estimate travel distance.", "Info")
            cfs = cfs_filtered

        # Origin
        if isinstance(origin, Location):
            cfs_filtered = cfs[cfs["ORIG_STATE"] == origin.get_cfs_area()]
            if cfs_filtered.empty:
                cfs_state_list = list(set(cfs["ORIG_STATE"].tolist()))
                closest_state_name, closest_state_code = Location.get_closest_states(origin, cfs_state_list)
                cfs_filtered = cfs[cfs["ORIG_STATE"] == closest_state_code]
                log(f"Closest state to {origin.get_location_name()}, {closest_state_name}, is used to estimate travel distance.", "Info")
            cfs = cfs_filtered

        # Mode
        if isinstance(mode,  TransportMode):
            cfs_filtered = cfs[cfs["MODE"].isin(mode.get_cfs_mode())]
            if cfs_filtered.empty:
                raise ValueError("Transportation mode in CFS dataset")
            
            cfs = cfs_filtered  
           
        return cfs
    
    @staticmethod
    def get_distance_estimate(dataset, scenario):
        """ Get the average distance from the CFS dataset based on the scenario.
        
        Parameters
        ----------
        dataset : pandas.DataFrame
            The filtered CFS dataset.
        scenario : str
            The scenario to filter the distances by.
        
        Returns
        -------
        float
            The average distance for the specified scenario.
        
        Raises
        ------
        ValueError
            If the scenario is not recognized or if no data is found for the scenario.
        """
        quartiles = dataset["SHIPMT_DIST_ROUTED"].quantile([0.25, 0.5, 0.75]).values
        def assign_quartile(x, q1, q2, q3):
            if x <= q1:
                return 'Q1'
            elif x <= q2:
                return 'Q2'
            elif x <= q3:
                return 'Q3'
            else:
                return 'Q4'
        dataset['quartile'] = dataset["SHIPMT_DIST_ROUTED"].apply(assign_quartile, args=(quartiles[0], quartiles[1], quartiles[2]))
        
        if scenario == "Local":
            domestic_dis = dataset[dataset["quartile"] == "Q1"]["SHIPMT_DIST_ROUTED"].mean()
        elif scenario == "Regional":
            domestic_dis = dataset[dataset["quartile"] == "Q2"]["SHIPMT_DIST_ROUTED"].mean()
        elif scenario == "Regional_c":
            domestic_dis = dataset[dataset["quartile"] == "Q3"]["SHIPMT_DIST_ROUTED"].mean()
        elif scenario == "National":
            domestic_dis = dataset[dataset["quartile"] == "Q4"]["SHIPMT_DIST_ROUTED"].mean()
        elif scenario == "None" or scenario == "Known_us" or scenario == None:
            domestic_dis = dataset["SHIPMT_DIST_ROUTED"].mean()

        return domestic_dis

if __name__ == '__main__':
    pass
