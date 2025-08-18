
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu; etel5501@uw.edu"
__version__ = "0.1.0"

import os

from . import ARXCalculation
from ...utilities import config
from ...utilities import DataImporter


class AR4Calculations(ARXCalculation):
    """ Computation methods related to dynamic radiative forcing methods.
    """
    _ipcc_annual_report = 'AR4'

    @classmethod
    def get_radiative_efficiency(cls, greenhouse_gas, ref_unit="Wm-2ppb-1", adjust_for_indirect_effects=True):
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
                    radiative_efficiency *= (1 + indirect_factors['f1'] + indirect_factors['f2'])
                elif greenhouse_gas == 'N2O':
                    radiative_efficiency *= (1 - abs(indirect_factors['factor_CH4_to_N20']) * cls.get_radiative_efficiency('CH4', 'Wm-2ppb-1') / 
                                             cls.get_radiative_efficiency('N2O', 'Wm-2ppb-1', adjust_for_indirect_effects=False))

            if not adjust_for_indirect_effects and radiative_efficiency_dict["_corrected"]:
                if greenhouse_gas == 'CH4':
                    radiative_efficiency /= (1 + indirect_factors['f1'] + indirect_factors['f2'])
                elif greenhouse_gas == 'N2O':
                    radiative_efficiency /= (1 -  abs(indirect_factors['factor_CH4_to_N20']) * cls.get_radiative_efficiency('CH4', 'Wm-2ppb-1') / 
                                             cls.get_radiative_efficiency('N2O', 'Wm-2ppb-1'))
            
            return radiative_efficiency
        else:
            return None


if __name__ == '__main__':
    pass
