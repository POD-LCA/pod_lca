
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu; etel5501@uw.edu"
__version__ = "0.1.0"

import os

from numpy import arange as np_arange
from numpy import exp as np_exp
from numpy import convolve
from numpy import flip

from ...utilities import config
from ...utilities import DataImporter
from ...utilities import MathFuncs


class ARXCalculation:
    """ Computation methods related to dynamic radiative forcing methods.

    Attributes
    ----------
    _ipcc_annual_report : {'AR4', 'AR5', 'AR6'}
        The IPCC report version
    """
    _ipcc_annual_report = None

    @staticmethod
    def get_radiative_efficiency(greenhouse_gas, ref_unit="Wm-2ppb-1", adjust_for_indirect_effects=True):
        """ Get the radiative efficiency of given greenhouse_gas.
         
        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g.,'CO2', 'CH4'. 'N2O'
        ref_unit: str
            Output unit: 'Wm-2ppb-1', 'Wm-2kg-1'
        adjust_for_indirect_effects: bool
            Adjust radiative efficiency to account for indirect effects
        
        Returns
        -------
        float
            Radiative efficiency, in reference unit
        """
        pass

    @classmethod
    def get_pertubation_lifetime(cls, greenhouse_gas):
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
        root, ext = os.path.splitext(config['file_paths']['drf']['PERTUBATION_LIFETIMES'])

        pertubation_lifetimes_dict = DataImporter.json_to_dict(root + '_' + cls._ipcc_annual_report + ext)
        if greenhouse_gas in pertubation_lifetimes_dict:
            return pertubation_lifetimes_dict[greenhouse_gas]
        else:
            return None
    
    @classmethod
    def get_atmospheric_concentration(cls, greenhouse_gas, at_year, cumulative=False):
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
            Concentration of the greenhouse gas, in kg (if not cumulative) or in kg-yrs (if cumulative). 
        """
        root, ext = os.path.splitext(config['file_paths']['drf']['CO2_IRF_PARAMETERS'])
        params = DataImporter.json_to_dict(root + '_' + cls._ipcc_annual_report + ext)

        if cumulative:
            if greenhouse_gas == 'CO2':
                term_1 = params['a_0'] *  at_year
                term_2 = MathFuncs.integrate_exp(a=0, b=at_year, coeff=params['a_1'], pow_coeff=-1 / params['tau_1'])
                term_3 = MathFuncs.integrate_exp(a=0, b=at_year, coeff=params['a_2'], pow_coeff=-1 / params['tau_2'])
                term_4 = MathFuncs.integrate_exp(a=0, b=at_year, coeff=params['a_3'], pow_coeff=-1 / params['tau_3'])
                return (term_1 + term_2 + term_3 + term_4)
            else:
                life_time = cls.get_pertubation_lifetime(greenhouse_gas)
                return MathFuncs.integrate_exp(a=0, b=at_year, coeff=1.0, pow_coeff=-1 / life_time)
            
        else:
            if greenhouse_gas == 'CO2':
                term_1 = params['a_0']
                term_2 = params['a_1'] * np_exp(-1 * at_year / params['tau_1'])
                term_3 = params['a_2'] * np_exp(-1 * at_year / params['tau_2'])
                term_4 = params['a_3'] * np_exp(-1 * at_year / params['tau_3'])

                return (term_1 + term_2 + term_3 + term_4)
            
            else:
                life_time = cls.get_pertubation_lifetime(greenhouse_gas)
                return np_exp(-1 * at_year / life_time)

    @classmethod
    def get_radiative_forcing(cls, greenhouse_gas, at_year, cumulative=False, CH4_oxidation=False, alpha=0.5, convolution_time_step = 0.01):
        """ Get the radiative forcing (in W/m^2) of the greenhouse gas at a given year, given that a 1kg of gas emitted on start year.
        
        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O' 
        at_year : int or array
            Year(s) at which concentration computed, given that a 1kg of gas emitted on start of year 0.
        cumulative : bool
            Cumulative values if true, else instantaneous values.
        CH4_oxidation : bool
            If true, account for oxidation of CH4 to CO2
        alpha : float
            Fraction of CH4 oxidized: 0.5-1.0
        convolution_time_step : float
            Time step for CH4 oxidation.    

        Returns
        -------
        float
            radiative forcing, in W/m2.       
        """
        if greenhouse_gas == 'CH4':
            molecular_weight_dict = DataImporter.json_to_dict(config['file_paths']['drf']['MOLECULER_WEIGHT'])
            if molecular_weight_dict['_ref_unit'] in ['gmol-1', 'kg kmol-1', 'amu']:
                molecular_weight_CH4 = molecular_weight_dict['CH4']
                molecular_weight_CO2 = molecular_weight_dict['CO2']
            else:
                raise ValueError(f"Reference unit {molecular_weight_dict['_ref_unit']} not recognized.")
        
            RF_CH4 = cls.get_radiative_efficiency('CH4', ref_unit="Wm-2kg-1") * cls.get_atmospheric_concentration('CH4', at_year, cumulative)
            
            if CH4_oxidation:
                pertubation_life_time_CH4 = cls.get_pertubation_lifetime('CH4')

                _, CH4_concentration = cls.get_concentration_time_series('CH4', at_year, convolution_time_step, cumulative=False)
                _, CO2_concentration_unit_pulse = cls.get_concentration_time_series('CO2', at_year, convolution_time_step, cumulative)
                CO2_concentration_from_CH4 = sum(alpha * (molecular_weight_CO2/ molecular_weight_CH4) * (1 / pertubation_life_time_CH4) * CO2_concentration_unit_pulse * flip(CH4_concentration)) * convolution_time_step

                return RF_CH4 + cls.get_radiative_efficiency('CO2', ref_unit="Wm-2kg-1") * CO2_concentration_from_CH4

            return RF_CH4
        else:
            return cls.get_radiative_efficiency(greenhouse_gas, ref_unit="Wm-2kg-1") * cls.get_atmospheric_concentration(greenhouse_gas, at_year, cumulative)

    @classmethod
    def get_dynamic_characterization_factor(cls, greenhouse_gas, time_horizon, cumulative=False):
        pass

    @classmethod
    def get_concentration_time_series(cls, greenhouse_gas, time_horizon, time_step, cumulative=False):
        """ Get the concentration of the greenhouse gas in the atmosphere as a time-series.

        Note
        ----
        1. Noting the behaviour of numpy.arange with floats, the end value of years is checked against time horizon. 

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

        Returns
        -------
        numpy.array
            years of the time series
        numpy.array
            concentration values at the end of the year #TODO: double check this    
        """
        years = np_arange(0, time_horizon + time_step, time_step)
        if years[-1] > time_horizon:
            years = years[:-1]
        concentrations = cls.get_atmospheric_concentration(greenhouse_gas, years, cumulative) # TODO: check the at_years variable
        return years, concentrations
        
    @classmethod
    def get_radiative_forcing_time_series(cls, greenhouse_gas, time_horizon, time_step, cumulative=True, CH4_oxidation=False, alpha=0.5):
        """ Get the daynamic radiative forcing values (in W/m^2) as a time-series, given that a 1kg of gas emitted on start year.

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
        CH4_oxidation : bool
            If true, account for oxidation of CH4 to CO2
        alpha : float
            Fraction of CH4 oxidized: 0.5-1.0

        Returns
        -------
        numpy.array
            Years of the time series
        numpy.array
            Atmospheric concentration values at the end of the year #TODO: double check this 
        numpy.array
            Radiative forcing values at the end of the year
        """
        radiative_efficiency = cls.get_radiative_efficiency(greenhouse_gas, ref_unit="Wm-2kg-1")
        years, concentrations = cls.get_concentration_time_series(greenhouse_gas, time_horizon, time_step, cumulative)

        if greenhouse_gas == 'CH4':
            molecular_weight_dict = DataImporter.json_to_dict(config['file_paths']['drf']['MOLECULER_WEIGHT'])
            if molecular_weight_dict['_ref_unit'] in ['gmol-1', 'kg kmol-1', 'amu']:
                molecular_weight_CH4 = molecular_weight_dict['CH4']
                molecular_weight_CO2 = molecular_weight_dict['CO2']
            else:
                raise ValueError(f"Reference unit {molecular_weight_dict['_ref_unit']} not recognized.")
        
            RF_CH4 = radiative_efficiency * concentrations
            if CH4_oxidation:
                pertubation_life_time_CH4 = cls.get_pertubation_lifetime('CH4')

                _, CH4_concentration = cls.get_concentration_time_series('CH4', time_horizon, time_step, cumulative=False)
                _, CO2_concentration_unit_pulse = cls.get_concentration_time_series('CO2', time_horizon, time_step, cumulative)
                CO2_concentration_from_CH4 = alpha * (molecular_weight_CO2/ molecular_weight_CH4) * (1 / pertubation_life_time_CH4) * convolve(CO2_concentration_unit_pulse, CH4_concentration)[:len(years)] * time_step
                
                RF_CO2 = cls.get_radiative_efficiency('CO2', ref_unit="Wm-2kg-1") * CO2_concentration_from_CH4

                return years, concentrations, RF_CH4 + RF_CO2

            return years, concentrations, RF_CH4
        else:
            return years, concentrations, radiative_efficiency * concentrations

    @classmethod
    def get_AGWP(cls, greenhouse_gas, time_horizon):
        """ Get the Absolute Global Warming Potential (AGWP) of a greenhouse gas, for the given time_horizon.

        Note
        ----
        1. For the calculation fo CH4 fossil, oxidation factor (alpha) of 0.5, and convolution time step of 0.01 is used.
        
        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O' 
        time_horizon : int
            Time horizon in years.        
        """
        root, ext = os.path.splitext(config['file_paths']['drf']['INDIRECT_EFFECTS_FACTORS'])

        indirect_factors = DataImporter.json_to_dict(root + '_' + cls._ipcc_annual_report + ext)

        if greenhouse_gas in ['CH4fossil', 'CH4_fossil', 'CH4 fossil']:
            agwp = cls.get_radiative_forcing('CH4', time_horizon, cumulative=True, CH4_oxidation=True, alpha=indirect_factors['alpha'], convolution_time_step=0.01)
        else:
            agwp = cls.get_radiative_forcing(greenhouse_gas, time_horizon, cumulative=True)
        
        return agwp
    
    @classmethod
    def get_GWP(cls, greenhouse_gas, time_horizon):
        """ Get the Global Warming Potential (GWP) of a greenhouse gas, for the given time_horizon.

        Note
        ----
        1. For the calculation fo CH4 fossil, oxidation factor (alpha) of 0.5, and convolution time step of 0.01 is used.
        
        Parameters
        ----------
        greenhouse_gas: str
            Name of the gas: e.g., 'CO2', 'CH4'. 'N2O' 
        time_horizon : int
            Time horizon in years.        
        """
        agwp_CO2 = cls.get_AGWP('CO2', time_horizon)
        agwp_gas = cls.get_AGWP(greenhouse_gas, time_horizon)
        
        return agwp_gas / agwp_CO2


if __name__ == '__main__':
    pass
