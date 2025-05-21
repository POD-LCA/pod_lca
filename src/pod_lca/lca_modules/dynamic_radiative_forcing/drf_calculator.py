
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from numpy import exp as np_exp
from numpy import arange as np_arange

from math import exp

from ...utilities import config
from ...utilities import DataImporter
from ...utilities import MathFuncs

class DynamicRadiativeForcing:

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
                    return radiative_efficiency * (molecular_weight/molecular_weight_air_mean) * (mass_atmosphere_total/ (10 ** 9))
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
        else:
            return None
    
    @staticmethod
    def get_atmospheric_concentration(greenhouse_gas, at_year, cumulative=False):
        """ Get the concentration of the greenhouse gas in the atmosphere at a given year, given that a 1kg of gas emitted on start of year 0.

        Notes
        -----
        1. For CO2, calculation based on Joos, F., et al., 2013: Carbon dioxide and climate impulse response functions for the computation of greenhouse gas metrics: A multi-model analysis. Atmos. Chem. Phys., 13, 2793–2825
        
        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O' 
        at_year : int or array
            Year(s) at which concentration computed, given that a 1kg of gas emitted on start of year 0.
        cumulative : bool
            Cumulative values if true, else instantaneous values.   

        Returns
        -------
        float
            Concentration of the greenhouse gas, in kg.       
        """
        if cumulative: # TODO: Double check integration functions
            if greenhouse_gas == 'CO2':
                term_1 = 0.2173 *  at_year
                term_2 = MathFuncs.integrate_exp(a=0, b=at_year, coeff=0.2240, pow_coeff=-1 / 394.4)
                term_3 = MathFuncs.integrate_exp(a=0, b=at_year, coeff=0.2824, pow_coeff=-1 / 36.54)
                term_4 = MathFuncs.integrate_exp(a=0, b=at_year, coeff=0.2763, pow_coeff=-1 / 4.304)
                return (term_1 + term_2 + term_3 + term_4)
            else:
                life_time = DynamicRadiativeForcing.get_pertubation_lifetime(greenhouse_gas)
                return MathFuncs.integrate_exp(a=0, b=at_year, coeff=1.0, pow_coeff=-1 / life_time)
        else:
            if greenhouse_gas == 'CO2':
                term_1 = 0.2173
                term_2 = 0.2240 * np_exp(-1 * at_year / 394.4)
                term_3 = 0.2824 * np_exp(-1 * at_year / 36.54)
                term_4 = 0.2763 * np_exp(-1 * at_year / 4.304)
                return (term_1 + term_2 + term_3 + term_4)
            else:
                life_time = DynamicRadiativeForcing.get_pertubation_lifetime(greenhouse_gas)
                return np_exp(-1 * at_year / life_time)

    @staticmethod
    def get_radiative_forcing(greenhouse_gas, at_year, cumulative=False):
        """ Get the radiative forcing of the greenhouse gas at a given year, given that a 1kg of gas emitted on start year.
        
        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O' 
        at_year : int or array
            Year(s) at which concentration computed, given that a 1kg of gas emitted on start of year 0.
        cumulative : bool
            Cumulative values if true, else instantaneous values.  

        Returns
        -------
        float
            radiative forcing, in W/m2.       
        """
        return DynamicRadiativeForcing.get_radiative_efficiency(greenhouse_gas, ref_unit="Wm-2kg-1") * DynamicRadiativeForcing.get_atmospheric_concentration(greenhouse_gas, at_year, cumulative)

    @staticmethod
    def get_concentration_time_series(greenhouse_gas, time_horizon, time_step, cumulative=False):
        """ Get the concentration of the greenhouse gas in the atmosphere as a time-series.

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
        years = np_arange(0, time_horizon, time_step)
        concentrations = DynamicRadiativeForcing.get_atmospheric_concentration(greenhouse_gas, years + time_step, cumulative) # TODO: check the at_years variable
        return years, concentrations
        
    @staticmethod
    def get_radiative_forcing_time_series(greenhouse_gas, time_horizon, time_step, cumulative=True):
        """ Get the daynamic radiative forcing values as a time-series.

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
        radiative_efficiency = DynamicRadiativeForcing.get_radiative_efficiency(greenhouse_gas, ref_unit="Wm-2kg-1")
        years, concentrations = DynamicRadiativeForcing.get_concentration_time_series(greenhouse_gas, time_horizon, time_step, cumulative)
        return years, radiative_efficiency * concentrations

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
        pass # TODO
    # TODO convolution


if __name__ == '__main__':
    pass
