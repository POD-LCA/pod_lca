
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu; etel5501@uw.edu"
__version__ = "0.1.0"

import os

from numpy import flip
from numpy import convolve

from . import ARXCalculation
from ...utilities import config
from ...utilities import DataImporter


class AR6Calculations(ARXCalculation):
    """ Computation methods related to dynamic radiative forcing methods, following IPCC AR6.
    """
    _ipcc_annual_report = 'AR6'

    @classmethod
    def get_radiative_efficiency(cls, greenhouse_gas, ref_unit="Wm-2ppb-1", adjust_for_indirect_effects=True):
        """ Get the radiative efficiency of given greenhouse_gas.
         
        Parameters
        ----------
        greenhouse_gas: {'CO2', 'CH4', 'N2O'}
            Name of the gas.
        ref_unit: {'Wm-2ppb-1', 'Wm-2kg-1'}
            Output unit.
        adjust_for_indirect_effects: bool
            Adjust radiative efficiency to account for indirect effects
        
        Returns
        -------
        float
            Radiative efficiency, in reference unit
        """
        mass_atmosphere_total = 5.1352 * 10 ** 18 # in kg
        molecular_weight_air_mean = 28.97 # in g mol−1

        root, ext = os.path.splitext(config['file_paths']['drf']['INDIRECT_EFFECTS_FACTORS'])
        indirect_factors = DataImporter.json_to_dict(root + '_' + cls._ipcc_annual_report + ext)

        root, ext = os.path.splitext(config['file_paths']['drf']['RADIATIVE_EFFICIENCY'])
        radiative_efficiency_dict = DataImporter.json_to_dict(root + '_' + cls._ipcc_annual_report + ext)
        
        if greenhouse_gas in radiative_efficiency_dict:
            radiative_efficiency = radiative_efficiency_dict[greenhouse_gas]['val']

            # Adjust units
            RE_unit = radiative_efficiency_dict[greenhouse_gas]['unit']
            if RE_unit != ref_unit:
                molecular_weight_dict = DataImporter.json_to_dict(config['file_paths']['drf']['MOLECULER_WEIGHT'])
                if molecular_weight_dict['_ref_unit'] in ['gmol-1', 'kg kmol-1', 'amu']:
                    molecular_weight = molecular_weight_dict[greenhouse_gas]
                else:
                    raise ValueError(f"Reference unit {molecular_weight_dict['_ref_unit']} not recognized.")
                
                if ref_unit == 'Wm-2kg-1' and RE_unit == 'Wm-2ppb-1':
                    radiative_efficiency *=  (molecular_weight_air_mean/molecular_weight) * (10 ** 9 /mass_atmosphere_total)
                elif ref_unit == 'Wm-2ppb-1' and RE_unit == 'Wm-2kg-1':
                    radiative_efficiency *= (molecular_weight/molecular_weight_air_mean) * (mass_atmosphere_total/ (10 ** 9))
                else:
                    raise ValueError(f"Reference unit {ref_unit} not recognized.")
            
            # account for indirect effects
            if adjust_for_indirect_effects and not radiative_efficiency_dict["_corrected"]:
                if greenhouse_gas == 'CH4':
                    if ref_unit == 'Wm-2ppb-1':
                        radiative_efficiency += (indirect_factors['f1'] + indirect_factors['f2'])
                    elif ref_unit == 'Wm-2kg-1':
                        molecular_weight = 16.04
                        radiative_efficiency += (indirect_factors['f1'] + indirect_factors['f2']) * (molecular_weight_air_mean/molecular_weight) * (10 ** 9 /mass_atmosphere_total) #FIXME
                    else:
                        ValueError(f"Reference unit {ref_unit} not recognized.")
                elif greenhouse_gas == 'N2O':
                    radiative_efficiency *= (1 - abs(indirect_factors['factor_CH4_to_N20']) * cls.get_radiative_efficiency('CH4', 'Wm-2ppb-1') / 
                                             cls.get_radiative_efficiency('N2O', 'Wm-2ppb-1', adjust_for_indirect_effects=False))

            if not adjust_for_indirect_effects and radiative_efficiency_dict["_corrected"]:
                if greenhouse_gas == 'CH4':
                    if ref_unit == 'Wm-2ppb-1':
                        radiative_efficiency -= (indirect_factors['f1'] + indirect_factors['f2'])
                    elif ref_unit == 'Wm-2kg-1':
                        molecular_weight = 16.04
                        radiative_efficiency -= (indirect_factors['f1'] + indirect_factors['f2']) * (molecular_weight_air_mean/molecular_weight) * (10 ** 9 /mass_atmosphere_total) #FIXME
                    else:
                        ValueError(f"Reference unit {ref_unit} not recognized.")

                elif greenhouse_gas == 'N2O':
                    radiative_efficiency /= (1 - abs(indirect_factors['factor_CH4_to_N20']) * cls.get_radiative_efficiency('CH4', 'Wm-2ppb-1') / 
                                             cls.get_radiative_efficiency('N2O', 'Wm-2ppb-1'))
            
            return radiative_efficiency
        else:
            return None

    @classmethod
    def get_radiative_forcing(cls, greenhouse_gas, at_year, cumulative=False, CH4_oxidation=False, alpha=0.75, convolution_time_step = 0.01):
        """ Get the radiative forcing (in W/m^2) of the greenhouse gas at a given year, given that a 1kg of gas emitted on start year.
        
        Parameters
        ----------
        greenhouse_gas: {'CO2', 'CH4', 'N2O'}
            Name of the gas. 
        at_year : int or array
            Year(s) at which concentration computed, given that a 1kg of gas emitted on start of year 0.
        cumulative : bool
            Cumulative values if true, else instantaneous values.
        CH4_oxidation : bool
            If true, account for oxidation of CH4 to CO2.
        alpha : float
            Fraction of CH4 oxidized: 0.5-1.0.
        convolution_time_step : float
            Time step for CH4 oxidation.    

        Returns
        -------
        float
            radiative forcing, in W/m2.       
        """
        root, ext = os.path.splitext(config['file_paths']['drf']['INDIRECT_EFFECTS_FACTORS'])
        indirect_factors = DataImporter.json_to_dict(root + '_' + cls._ipcc_annual_report + ext)

        if greenhouse_gas == 'CH4':
            molecular_weight_dict = DataImporter.json_to_dict(config['file_paths']['drf']['MOLECULER_WEIGHT'])
            if molecular_weight_dict['_ref_unit'] in ['gmol-1', 'kg kmol-1', 'amu']:
                molecular_weight_CH4 = molecular_weight_dict['CH4']
                molecular_weight_CO2 = molecular_weight_dict['CO2']
            else:
                raise ValueError(f"Reference unit {molecular_weight_dict['_ref_unit']} not recognized.")
        
            RF_CH4 = cls.get_radiative_efficiency('CH4', ref_unit="Wm-2kg-1") * cls.get_atmospheric_concentration('CH4', at_year, cumulative)
            
            if CH4_oxidation:
                pertubation_life_time_CH4 = indirect_factors["CH4_oxidation_life_time"]

                _, CH4_concentration = cls.get_concentration_time_series('CH4', at_year, convolution_time_step, cumulative=False)
                _, CO2_concentration_unit_pulse = cls.get_concentration_time_series('CO2', at_year, convolution_time_step, cumulative)
                CO2_concentration_from_CH4 = sum(alpha * (molecular_weight_CO2/ molecular_weight_CH4) * (1 / pertubation_life_time_CH4) * CO2_concentration_unit_pulse * flip(CH4_concentration)) * convolution_time_step

                return RF_CH4 + cls.get_radiative_efficiency('CO2', ref_unit="Wm-2kg-1") * CO2_concentration_from_CH4

            return RF_CH4
        else:
            return cls.get_radiative_efficiency(greenhouse_gas, ref_unit="Wm-2kg-1") * cls.get_atmospheric_concentration(greenhouse_gas, at_year, cumulative)

    @classmethod
    def get_radiative_forcing_time_series(cls, greenhouse_gas, time_horizon, time_step, cumulative=True, CH4_oxidation=False, alpha=0.5):
        """ Get the daynamic radiative forcing values (in W/m^2) as a time-series, given that a 1kg of gas emitted on start year.

        Parameters
        ----------
        greenhouse_gas: {'CO2', 'CH4', 'N2O'}
            Name of the gas.
        time_horizon : int
            Time horizon in years.  
        time_step : float
            Time step in years.
        cumulative : bool
            Cumulative radiative forcing if true, else instantaneous values.
        CH4_oxidation : bool
            If true, account for oxidation of CH4 to CO2.
        alpha : float
            Fraction of CH4 oxidized: 0.5-1.0.

        Returns
        -------
        numpy.array
            Years of the time series
        numpy.array
            Atmospheric concentration values at the end of the year
        numpy.array
            Radiative forcing values at the end of the year
        """
        root, ext = os.path.splitext(config['file_paths']['drf']['INDIRECT_EFFECTS_FACTORS'])
        indirect_factors = DataImporter.json_to_dict(root + '_' + cls._ipcc_annual_report + ext)

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
                pertubation_life_time_CH4 = indirect_factors["CH4_oxidation_life_time"]

                _, CH4_concentration = cls.get_concentration_time_series('CH4', time_horizon, time_step, cumulative=False)
                _, CO2_concentration_unit_pulse = cls.get_concentration_time_series('CO2', time_horizon, time_step, cumulative)
                CO2_concentration_from_CH4 = alpha * (molecular_weight_CO2/ molecular_weight_CH4) * (1 / pertubation_life_time_CH4) * convolve(CO2_concentration_unit_pulse, CH4_concentration)[:len(years)] * time_step
                
                RF_CO2 = cls.get_radiative_efficiency('CO2', ref_unit="Wm-2kg-1") * CO2_concentration_from_CH4

                return years, concentrations, RF_CH4 + RF_CO2

            return years, concentrations, RF_CH4
        else:
            return years, concentrations, radiative_efficiency * concentrations
        

if __name__ == '__main__':
    pass
