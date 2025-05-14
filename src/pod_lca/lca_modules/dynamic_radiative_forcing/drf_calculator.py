
from pod_lca.utilities import config
from pod_lca.utilities import DataImporter

class DynamicRadiativeForcing:

    def __init__(self):
        self.start_year = None
        self.emissions = []

    @staticmethod
    def get_radiative_efficiency(greenhouse_gas, ref_unit="Wm-2ppb-1"):
        """ Get the radiative efficiency of given greenhouse_gas.
         
        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g.,'CO2', 'CH4'. 'N2O'
        ref_unit: str
            Output unit: 'Wm-2ppb-1', 'Wm-2kg-1'
        
        Returns
        -------
        float
            Radiative efficiency, in reference unit
        """
        mass_atmosphere_total = 5.1352 * 10**18 # in kg
        molecular_weight_air_mean = 28.97 # in g mol−1

        radiative_efficiency_dict = DataImporter.json_to_dict(config['file_paths']['drf']['RADIATIVE_EFFICIENCY'])
        
        if greenhouse_gas in radiative_efficiency_dict:
            radiative_efficiency = radiative_efficiency_dict[greenhouse_gas]
            if radiative_efficiency_dict['_ref_unit'] == ref_unit:
                return radiative_efficiency
            else:
                molecular_weight_dict = DataImporter.json_to_dict(config['file_paths']['drf']['MOLECULER_WEIGHT'])
                if molecular_weight_dict['_ref_unit'] in ['gmol-1', 'kg kmol-1', 'amu']:
                    molecular_weight = molecular_weight_dict[greenhouse_gas]
                else:
                    raise ValueError(f"Reference unit {molecular_weight_dict['_ref_unit']} not recognized.")
                
                if ref_unit == 'Wm-2kg-1' and radiative_efficiency_dict['_ref_unit'] == 'Wm-2ppb-1':
                    return radiative_efficiency * (molecular_weight_air_mean/molecular_weight) * (10 ** 9 /mass_atmosphere_total)
                elif ref_unit == 'Wm-2ppb-1' and radiative_efficiency_dict["_ref_unit"] == 'Wm-2kg-1':
                    return radiative_efficiency / ((molecular_weight_air_mean/molecular_weight) * (10 ** 9 /mass_atmosphere_total))
                else:
                    raise ValueError(f"Reference unit {ref_unit} not recognized.")
        else:
            return None

    @staticmethod
    def get_pertubation_lifetime(greenhouse_gas):
        """ Get the pertubation lifetime of the greenhouse_gas in question.

        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O'

        Returns
        -------
        float
            Pertubation lifetime in years.
        """
        pertubation_lifetimes_dict = DataImporter.json_to_dict(config['file_paths']['drf']['PERTUBATION_LIFETIMES'])
        if greenhouse_gas in pertubation_lifetimes_dict:
            return pertubation_lifetimes_dict[greenhouse_gas]
            # NOTE: [Q-EE] CO2 values from Table 8.SM.10. Can these be called pertubation lifetimes
        else:
            return None
    
    def get_instantaneous_concentration(self, greenhouse_gas, year):
        """ Get the concentration of the greenhouse gas in the atmosphere at a given year, given that a 1kg of gas emitted on start year.
        
        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O' 
        year : int
            Year at which concentration computed.

        Returns
        -------
        float
            Concentration of the greenhouse gas, in kg.       
        """
        pass
        # NOTE: takes start_year from self

    def get_instantaneous_radiative_forcing(greenhouse_gas, year):
        """ Get the radiative forcing of the greenhouse gas at a given year, given that a 1kg of gas emitted on start year.
        
        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O' 
        year : int
            Year at which concentration computed.

        Returns
        -------
        float
            radiative forcing, in W/m2.       
        """
        pass

    def get_cumulative_radiative_forcing(self, greenhouse_gas, year):
        """ Get the cumalative radiative_forcing of the greenhouse gas at a given year, given that a 1kg of gas emitted on start year.
        
        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O' 
        year : int
            Year at which concentration computed.

        Returns
        -------
        float
            Concentration of the greenhouse gas, in kg.       
        """
        pass
        # NOTE: takes start_year from self
        # NOTE: integration methods in utilities.maths

    @staticmethod
    def get_GWP(greenhouse_gas, time_horizon):
        """ Get the Global Warming Potential of a greenhouse gas, for the given time_horizon.
        
        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O' 
        time_horizon : int
            Time horizon in years.        
        """
        pass

    def get_radiative_forcing_time_series(self, time_horizon, time_step, cumulative=True):
        """ Get the daynamic radiative forcing values as a time-series.
            Considers all emissions, with their corresponding emission years.

        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O' 
        time_horizon : int
            Time horizon in years.  
        time_step : float
            Time step in years.
        cumulative : bool
            Cumulative radiative forcing if true, else instantaneous values.       
        """
        pass
        # NOTE: this will take all the emissions from the emissions, and there corresponding emission years (see impacts.emission_invetories inheriting from impacts.records)
        # NOTE: takes start_year from self

if __name__ == '__main__':
    pass
