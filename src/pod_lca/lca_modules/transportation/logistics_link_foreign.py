
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from geopy.distance import geodesic

from . import CFSDataset
from . import DomesticLink
from . import LogisticLink
from . import TransportMode
from ..location import Location
from ...units import KILOMETER
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class ForeignLink(LogisticLink):
    """ A link of Global transportation.
    """
    # ================================
    # Setters and Getters
    # ================================
    def set_mode(self, mode:(str) , fuel_type:(str) , efficiency:(str) ):
        """ Set the transportation mode of the transportation link.

        Parameters
        ----------
        mode : str
            transportation mode of the transportation link.
        fuel_type : str, optional
            type of fuel used in the transportation mode (default is "Regular").
        efficiency : str, optional
            efficiency of the transportation mode "low, medium, high" (default is "medium").
        """
        if isinstance(mode, TransportMode):
            self.mode = mode
        
        elif isinstance(mode, str) or mode is None:
            fuel_type = "Regular" if fuel_type is None else fuel_type
            mode_efficiency = "Median" if efficiency is None else efficiency
            mode_name = "Truck" if mode is None else mode

            mode_obj = TransportMode.new(mode_name, mode_efficiency, fuel_type)

            self.mode = {'domestic': mode_obj, 'foreign': mode_obj}

        elif isinstance(mode, dict):
            domestic_mode_name = mode['domestic'] if 'domestic' in mode and isinstance(mode['domestic'], str) else 'Truck'
            foreign_mode_name = mode['foreign'] if 'foreign' in mode and isinstance(mode['foreign'], str) else 'Ocean'
            
            if isinstance(efficiency, dict):
                domestic_mode_efficiency = efficiency['domestic'] if 'domestic' in efficiency and isinstance(efficiency['domestic'], str) else 'Median'
                foreign_mode_effciency = efficiency['foreign'] if 'foreign' in efficiency and isinstance(efficiency['foreign'], str) else 'Median'
            elif isinstance(efficiency, (str, None)):
                foreign_mode_effciency = efficiency if isinstance(efficiency, str) else 'Median'
                domestic_mode_efficiency = efficiency if isinstance(efficiency, str) else 'Median'
            else:
                raise ValueError("Transport efficiency not recognized.")
            
            if isinstance(fuel_type, dict):
                domestic_mode_fuel_type = fuel_type['domestic'] if 'domestic' in fuel_type and isinstance(fuel_type['domestic'], str) else 'Regular'
                foreign_mode_fuel_type = fuel_type['foreign'] if 'foreign' in fuel_type and isinstance(fuel_type['foreign'], str) else 'Regular'
            elif isinstance(fuel_type, (str, None)):
                foreign_mode_fuel_type = fuel_type if isinstance(fuel_type, str) else 'Regular'
                domestic_mode_fuel_type = fuel_type if isinstance(fuel_type, str) else 'Regular'
            else:
                raise ValueError("Transport fuel type not recognized.")
            
            self.mode = TransportMode.new(foreign_mode_name, foreign_mode_effciency, foreign_mode_fuel_type)
            
            domestic_mode =TransportMode.new(domestic_mode_name, domestic_mode_efficiency, domestic_mode_fuel_type)
            
            if isinstance(self.get_next(), DomesticLink):
                self.get_next().set_mode(domestic_mode)
            else:
                domestic_link = DomesticLink.in_project(self.get_project(), self.get_name() + '_domestic')
                domestic_link.set_mode(domestic_mode)
                self.set_next(domestic_link)

        else:
            raise TypeError(f"Invalid type for mode: {type(mode)}. Must be a str or dict.")

        self.mode.set_parent(self)

        return self
    
    def set_shipping_org(self, shipping_org:(str)):
        """ Set the shipping origin of the project.

        Parameters
        ----------
        shipping_dest : str
            Name of the shipping origin location.
        """
        if shipping_org is None:
            if self.get_transport_scenario() in ["North_america", "Global"]: # TODO: verify this
                Faf_city_representation = DataImporter.json_to_dict(config['file_paths']['location']['FAF_CITY_REPRESENTATION'])
                faf  = DataImporter.csv_to_pandas(config['file_paths']['transportation']['FAF_DATA_PATH'])
                faf = faf[faf["fr_orig"].isin([801, 802])] if self.get_transport_scenario() == "North_america" else faf[faf["fr_orig"].isin([801, 802]) == False]
                faf = faf[faf["fr_orig"] == faf["fr_orig"].mode()[0]]

                self.shipping_org = Location.from_str(Faf_city_representation[str(int(faf["fr_orig"].mode()[0]))])
            else:
                self.shipping_org = None
        elif isinstance(shipping_org, Location):
            self.shipping_org = shipping_org
        elif isinstance(shipping_org, str):
            self.shipping_org = Location.from_str(shipping_org)
        else:
            raise ValueError("Shipping destination must be a Location object or a string representing the location.")

        return self

    def set_transport_scenario(self, transport_scenario:(str)):
        """ Set the transport scenario of the transportation link.

        Parameters
        ----------
        transport_scenario : str
            Transport scenario of the transportation link (e.g., "North_america", "Global", "Known").
        """
        super().set_transport_scenario(transport_scenario)
        self.get_next().set_transport_scenario(transport_scenario)

        return self
     
    def set_travel_dist(self, 
                        travel_dist, 
                        travel_dist_unit=None, 
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
        self.travel_dist_unit = KILOMETER if travel_dist_unit is None else travel_dist_unit
        
        if isinstance(travel_dist, (float, int)):
            self.travel_dist = travel_dist
        
        elif travel_dist is None:
            transport_scenario = self.get_transport_scenario()
            if isinstance(transport_scenario, str):
                if transport_scenario in ["Local", "Regional", "Regional_c", "National", "None", "Known_us", None]:
                    pass
                    # TODO: set travel distnace of the associated domestic links to zero
                elif transport_scenario in ["North_america", "Global", "Known"]:
                    domestic_dis, foreign_dis = self.get_distance_from_datasets(transport_scenario)
                    self.travel_dist = foreign_dis
                    self.get_next().set_travel_dist(domestic_dis, travel_dist_unit, return_trip_factor)                       
                else:
                    raise ValueError("Transport scenario not recognized.")
            else:
                raise ValueError("Either travel distance or transport scenario must be provided.")

        else:
            raise ValueError("Either travel distance or transport scenario must be provided.")
        
        self.return_trip_factor = return_trip_factor

        return self

    # ================================
    # Dataset Methods
    # ================================
    def get_distance_from_datasets(self, transport_scenario):
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
        conversion_factor = self.get_dist_unit().get_conversion_factor(KILOMETER)

        sctg_code = CFSDataset.get_sctg_code(self.get_material().get_name())
        datasets_filtered = FAFDataset.filter_datasets(sctg_code, self.get_shipping_dest(), self.get_shipping_org(), self.get_next().get_mode(), self.get_mode(), transport_scenario)
        domestic_dis, foreign_dis = FAFDataset.get_travel_dist(datasets_filtered, self.get_shipping_dest(), self.get_shipping_org(), self.get_mode().get_name())

        return domestic_dis * conversion_factor, foreign_dis * conversion_factor

class FAFDataset:
    """ A class to filter the FAF dataset based on the given parameters.
    """
    @staticmethod
    def filter_datasets(sctg=None, destination=None, origin=None, mode_domestic=None, mode_foreign=None, scenario=None):
        """ Filter all datasets corresponding to foreign travel.

        Parameters
        ----------
        sctg : int, optional
            The Standard Classification of Transported Goods (SCTG) code to filter by.
        destination : Location, optional
            The destination location to filter by.
        origin : Location, optional
            The origin location to filter by.
        mode_domestic : TransportMode, optional
            The foreign transportation mode to filter by.
        mode_foreign : TransportMode, optional
            The domestic transportation mode to filter by.
        scenario : str

        Returns
        -------
        pandas.DataFrame
            The filtered FAF dataset.
        pandas.DataFrame
            The filtered marine dataset.
        pandas.DataFrame
            The filtered cfaf dataset.     
        """
        faf = FAFDataset.filter_faf(sctg, destination, origin, mode_foreign, mode_domestic)
        marine = FAFDataset.filter_marine(destination, origin, scenario)
        cfaf = FAFDataset.filter_cfaf(sctg)

        return faf, marine, cfaf
    
    @staticmethod
    def filter_faf(sctg=None, destination=None, origin=None, mode_foreign=None, mode_domestic=None):
        """ Filter FAF data

        Parameters
        ----------
        sctg : int, optional
            The Standard Classification of Transported Goods (SCTG) code to filter by.
        destination : Location, optional
            The destination location to filter by.
        origin : Location, optional
            The origin location to filter by.
        mode_domestic : TransportMode, optional
            The foreign transportation mode to filter by.
        mode_foreign : TransportMode, optional
            The domestic transportation mode to filter by.
        scenario : str

        Returns
        -------
        pandas.DataFrame
            The filtered FAF dataset.

        Raises
        ------
        ValueError
            If no data is found for the provided SCTG code, destination, or mode.         
        """
        faf  = DataImporter.csv_to_pandas(config['file_paths']['transportation']['FAF_DATA_PATH'])
                
        # SCTG
        if sctg is not None:
            faf = faf[faf["sctg2"] == sctg]
            if faf.empty:
                raise ValueError("Material not found in FAF561 dataset")
        
        # Destination
        if isinstance(destination, Location):
            faf_filtered = faf[faf["dms_dest"].isin(destination.get_faf_domestic_region())]
            if faf_filtered.empty:
                closest_state_name, closest_faf_region_codes = Location.get_closest_regions_FAF(origin, faf["dms_dest"].tolist())
                faf_filtered = faf[faf["dms_dest"].isin(closest_faf_region_codes)]
                log(f"Closest state to {destination.get_location_name()}, {closest_state_name}, is used to estimate travel distance.", "Info")
            faf = faf_filtered
        
        # Origin
        if isinstance(origin, Location):
            faf_filtered = faf[faf["fr_orig"] == float(origin.get_faf_foreign_region())]
            if faf_filtered.empty: # TODO: if origin is foreign, the latter is redundant
                closest_state_name, closest_faf_region_codes = Location.get_closest_regions_FAF(origin, faf["fr_orig"].tolist())
                faf_filtered = faf[faf["fr_orig"].isin(closest_faf_region_codes)]
                log(f"Closest state to {origin.get_location_name()}, {closest_state_name}, is used to estimate travel distance.", "Info")
            faf = faf_filtered

        # Mode
        if isinstance(mode_foreign, TransportMode):
            faf_modes_mapping = DataImporter.json_to_dict(config['file_paths']['transportation']['FAF_MODE_CODE'])
            faf_filtered = faf[faf["fr_inmode"] == faf_modes_mapping[mode_foreign.get_name()]]
            if faf_filtered.empty:
                raise ValueError("Transportation mode in CFS dataset")
            faf = faf_filtered
        
        # Domestic Mode
        if mode_domestic is not None:
            faf_modes_mapping = DataImporter.json_to_dict(config['file_paths']['transportation']['FAF_MODE_CODE'])
            faf_filtered = faf[faf["dms_mode"] == faf_modes_mapping[mode_domestic.get_name()]]
            if faf_filtered.empty:
                raise ValueError("Transportation mode in CFS dataset")
            faf = faf_filtered

        return faf

    @staticmethod
    def filter_cfaf(sctg):
        """ Filter Canadian Freight Analysis Framework (CFAF) dataset by material SCTG code.
        
        Parameters
        ----------
        sctg : int
            Two-digit SCTG code of the material.

        Returns
        -------
        pandas.DataFrame Obj
            Filtered CFAF dataset.
        """
        cfaf = DataImporter.csv_to_pandas(config['file_paths']['transportation']['CFAF_DATA_PATH'])
        if isinstance(sctg, int):
            cfaf = cfaf[cfaf["SCTG_2digits"] == sctg]
            if cfaf.empty:
                raise ValueError("Material not found in cfaf dataset")

        return cfaf

    @staticmethod
    def filter_marine(destination=None, origin=None, scenario=None):
        """ Filter marine data.
        
        Parameters
        ----------
        destination : Location Obj.
            Final destination of the product.
        origin : Location Obj.
            Origin of the travel.
        scenario : str
            Transportation scenario considered.

        Returns
        -------
        pandas.DataFrame Obj
            Filtered marine dataset.
        """
        marine = DataImporter.csv_to_pandas(config['file_paths']['transportation']['MARINE_DATA_PATH'])
        
        # Destination
        if isinstance(destination, Location):
            marine = marine[marine["Coast"] == destination.us_coast]
            if marine.empty:
                raise ValueError("no data for the selected destination in Marine dataset")
        else:
            pass

        # Origin
        if isinstance(origin, Location):
            marine = marine[marine["Region"] == origin.get_marine_region()]
            if marine.empty:
                raise ValueError("no data for the selected origin in Marine dataset")
        else:
            if scenario == "North_america":
                marine = marine[marine["Region"].isin(["Canada", "Mexico"])]
            elif scenario == "Global":
                marine = marine[marine["Region"].isin(["Canada", "Mexico"]) == False]
            else:
                raise NotImplementedError
        
        return marine
    
    @staticmethod
    def get_travel_dist(fltered_datasets, destination, origin, mode):
        """ Get the average travel distance based on shipping destination, origin, and mode of transportation.
        
        Parameters
        ----------
        filtered_datasets : tuple
            Filtered datasets as pandas dataframes.
        destination : Location Obj.
            Final destination of the product.
        origin : Location Obj.
            Origin of the travel.
        mode : str
            Transportation mode

        Returns
        -------
        float
            Travel distance of the domestic leg of travel.
        float
            Travel distance of the foreign leg of travel.
        """
        faf, marine, cfaf = fltered_datasets

        if mode == "Truck":
            domestic_dis = faf["avr_dom_dist_km"].mean()
            foreign_dis = 200
        elif mode == "Rail":
            domestic_dis = 0
            foreign_dis = cfaf["Average_Distance_per_Shipment"].mean()
        elif mode == "Ocean":
            #TODO: revisit the management of the foreign travel destination and domestic travel origin
            domestic_dis = faf["avr_dom_dist_km"].mean()
            foreign_dis = marine["Distance_km"].mean()
        elif mode == "Air":
            dms_coordinates = destination.get_cordinates()
            fr_coordinates = origin.get_cordinates()
            domestic_dis = 0.0
            foreign_dis = geodesic(dms_coordinates, fr_coordinates).km
        else:
            raise ValueError(f"Invalid mode of transportation: {mode}. Must be one of 'Truck', 'Rail', 'Ocean', or 'Air'.")

        return domestic_dis, foreign_dis


if __name__ == '__main__':
    pass
