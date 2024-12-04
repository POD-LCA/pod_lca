
from lca_modules.uncertainity.hotspots import HotSpotAnalysis
from utilities.objects.array_methods import get_attribute_as_list, sort_by_attribute

import numpy as np

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu; mhtaba@uw.edu"
__version__ = "0.1.0"


class Calculator():
    """
    Calculator object carries varies calculations on the project data.
    This include, conversion of units of measurements and generating data for visualization.

    Attributes
    ----------
    project : Project Obj.
        Project on which the calculator operates.
    conversions : list of dict
        Each dictionary contains {unit (str): value (float)} entries where all such entries are equivalent.
    """

    def __init__(self, project):
        self.project = project
        self.conversions = [{'m': 1000.0, 'km': 1.0, 'mi': 0.621371},
                            {'g': 1000.0, 'kg': 1.0, 't': 0.001, 'lb': 2.20462},
                            {'l': 1.0, 'm3': 0.01, 'gal':0.264172},
                            {'J': 1000.0, 'kJ': 1.0, 'MJ': 0.001, 'kWh': 2.77778e-4, 'MWh': 2.77778e-7},
                            {'kgkm': 1.0, 'tkm': 0.001, 'lbmi':1.369887, 'kgmi': 0.621371}]
 
    def __reduce__(self):
        
        return (self.__class__, (None,), {"project": self.project})
    
    def __setstate__(self, state):
        self.__dict__.update(state)

    def get_project(self):
        """ Get the project linked to the calculator.
        
        Retruns
        -------
        Project Obj.
            Project linked to the calculator.
        """

        return self.project
    
    def get_units_list(self):
        """ Retrieve all units of measurements in the calculator database.

            Returns
            -------
            list of str
                All the units of measurements in the calculator.

        """

        units = []
        for items in self.conversions:
            units.extend(list(items.keys()))

        return units
    
    def get_total_impact(self, model_name, impact_cat):
        """ Calculate the total impact of the products and processes in the model.
        
            Parameters
            ----------
            model_name : str
                Name of the model
            impact_cat : str
                Impact category considered, including 'weighted'.

            Returns
            -------
            float
                Total impact value.
        """

        impacts_dict = self.project.get_model(model_name).get_impacts()
        impacts_lst = []
        for key, list in impacts_dict.items():
            impacts_lst.extend(list)

        if impact_cat not in self.get_project().get_database().get_impact_categories() + ['weighted']:
            raise AttributeError(f"{impact_cat} does not exist in the current project.")
        else:
            if impact_cat == 'weighted':
                val_lst = [impact.get_weighted_impact() for impact in impacts_lst]
            else:
                val_lst = [impact.get_impact(impact_cat) for impact in impacts_lst]

            return sum(val_lst)
    
    # =================================
    # UNIT CONVERSION
    # =================================
    
    def convert_units(self, from_unit, to_unit, qty):
        """ Converts a quantity from one unit to another, if they both the units measure the same property
            (e.g., volume, mass, distance).
            None will be returned if (a) either of the units are not in the units data of the calculator, or 
            (b) the units are incompatible (i.e., measures different properties). Note that the method does not
            distinguish between (a) and (b) above.

            Parameters
            ----------
            from_unit : str
                Original unit of measurement.
            to_unit : str
                New unit of measurement.
            qty : float
                Original quantity.

            Returns
            -------
            float
                Quantity in the new unit of measurement.
                (None, if units are incompatible)
        """

        for group in self.conversions:
            if from_unit in group:
                if to_unit in group:
                    return qty * group[to_unit] / group[from_unit]
            
        return None
            
    def conversion_factor(self, from_unit, to_unit):
        """ Calculate conversion factor from first unit to the second unit
            (i.e., what quantity of second unit is equal to a unit of the first).
            
            Parameters
            ----------
            from_unit : str
                Original unit of measurement.
            to_unit : str
                New unit of measurement.

            Returns
            -------
            float
                Conversion factor.
                (None, if units are incompatible)
        """

        return self.convert_units(from_unit, to_unit, qty=1.0)

    # =================================
    # CHECK METHODS
    # =================================
  
    def is_mass_unit(self, unit):
        """ Checks if a given unit is unit of measurement of mass.

            Parameters
            ----------
            unit : str
                Unit of measurement considered
            
            Retruns
            -------
            bool
                True, if the input unit measures mass.
                False, otherwise.
        
        """

        if self.conversion_factor(unit, 'kg') == None:
            return False
        else:
            return True
    
    def is_length_unit(self, unit):
        """ Checks if a given unit is unit of measurement of length/distance.

            Parameters
            ----------
            unit : str
                Unit of measurement considered
            
            Retruns
            -------
            bool
                True, if the input unit measures mass.
                False, otherwise.
        
        """

        if self.conversion_factor(unit, 'm') == None:
            return False
        else:
            return True

    def is_energy_unit(self, unit):
        """ Checks if a given unit is unit of measurement of energy.

            Parameters
            ----------
            unit : str
                Unit of measurement considered
            
            Retruns
            -------
            bool
                True, if the input unit measures mass.
                False, otherwise.
        
        """

        if self.conversion_factor(unit, 'kJ') == None:
            return False
        else:
            return True
        
    # =================================
    # PLOT DATA METHODS
    # =================================

    def get_data_by_LCstage(self, impact_category, model_name='Model_0'):
        """ Returns impact data by life cycle stage for given model and impact category.

            Parameters
            ----------
            impact_category : str
                Name of impact category.
            model_name : str
                Name of the model considered.

            Returns
            -------
            dict
                Impacts dictionary where {Life Cycle stage (str) : quantity of impact (float)}.

            Raises
            ------
                AttributeError : impact category doe not exist in the current project
        
        """

        impacts_dict = self.project.get_model(model_name).get_impacts()

        if impact_category not in self.get_project().get_database().get_impact_categories():
            raise AttributeError(f"{impact_category} does not exist in the current project.")
        else:
            vals = {}
            for stage in impacts_dict.keys():
                impact_lst = impacts_dict[stage]
                vals[stage] = 0.0
                for impact in impact_lst:
                    vals[stage] += impact.get_impact(impact_category)

            return vals, impacts_dict.keys()
    

    def get_barchart_data(self, impact_category, model_lst=['Model_0']):
        """ Returns data for a barchart.
            
            Parameters
            ----------
            impact_category : str
                Name of the Impact category.
            model_lst : List of str.
                Names of the models.

            Returns
            -------
            dict_keys
                x-labels.
            dict
                Heights of bars: { model_name (str): { stage (str): height (float)}}.
        """

        data_dict ={}
        for model_name in model_lst:
            data_dict[model_name], stages = self.get_data_by_LCstage(impact_category, model_name)
        
        return  stages, data_dict
        

    def get_barchart2_data (self, impact_category, model_name='Model_0'):
        """ Returns data for a barchart.
            
            Parameters
            ----------
            impact_category : str
                Name of the Impact category.
            model : str.
                Names of the model.

            Returns
            -------
            list
                List of names of items.
            list
                List of qtys.
            list
                List of ints (no of items).
            dict
                #TODO: update.

        """
        hotspot_analysis = HotSpotAnalysis(self.get_project())
        hot_spots = hotspot_analysis.run(model_name=model_name, impact_category= impact_category, printout=False)
        hot_spots_impacts = get_attribute_as_list(hot_spots, 'impacts')

        data_name=[]
        data_qty=[]
        data_len=[]

        model = self.get_project().get_model(model_name)
        for lc_stage in model.get_impacts():
            item_count = 0
            impacts_lst = model.get_impacts()[lc_stage]
            impacts_lst_sorted = sort_by_attribute(impacts_lst, impact_category, descending=True)
            for impact in impacts_lst_sorted:
                other_qty = 0.0
                if impact in hot_spots_impacts:
                    data_qty.append(impact.get_impact(impact_category))
                    data_name.append(impact.get_parent().get_name() + f'({model_name})')
                    item_count += 1
                else:
                    other_qty += impact.get_impact(impact_category)
            if other_qty > 0.0:
                data_qty.append(other_qty)
                data_name.append('Other' + f'({model_name})')
                item_count += 1
            data_len.append(item_count)

        impacts = {}
        other_dict = {'Other'  + f'({model_name})': np.array([0.] * len(data_len))}
        start_index = 0
        for lc_stage, length in enumerate(data_len):
            end_index = start_index + length
            for impact in range(start_index, end_index):
                if data_name[impact] == 'Other' + f'({model_name})':
                    other_dict['Other' + f'({model_name})'] += np.array([0] * lc_stage + [data_qty[impact]] + [0] * (len(data_len) - lc_stage - 1))
                else:
                    impacts[data_name[impact]] = np.array([0] * lc_stage + [data_qty[impact]] + [0] * (len(data_len) - lc_stage - 1))
            start_index = end_index
        
        impacts.update(other_dict)

        return data_name, data_qty, data_len, impacts

    def get_barchart3_data(self, impact_category, model= 'Model_0'):
        """ Returns data for a barchart.
            
            Parameters
            ----------
            impact_category : str
                Name of the Impact category.
            model : str.
                Names of the model.

            Returns
            -------
            dict
                #TODO: update.
        """

        labels = ['A1', 'A2', 'A3']
        data=[]
        for category in impact_category:
            tmp_dict, _ = self.get_data_by_LCstage(category, model)
            plt_data = [tmp_dict["A1"], tmp_dict["A2"], tmp_dict["A3"]]
            data.append(plt_data)

        impact_by_stage = {labels[i]: np.array([row[i] for row in data]) for i in range(len(labels))}
        
        return impact_by_stage

    def get_spider_chart_data (self, impact_category, model_lst=['Model_0'], stage='all'):
        """ Returns data for a barchart.
            
            Parameters
            ----------
            impact_category : List
                List of impact categories.
            model_lst : List of str.
                Names of the models.
            stage : str
                Life Cycle Stage considered.

            Returns
            -------
            dict
                #TODO: update.
        """

        data={}
        for impact in impact_category:
            impact_data = {}

            for model_name in model_lst:
                model_data, _ = self.get_data_by_LCstage(impact, model_name)
                impact_data[model_name] = model_data  

            if stage == 'all':
                stage_values = {model: sum(impact_data[model].values()) for model in impact_data}
            else:
                stage_values = {model: values[stage] for model, values in impact_data.items()}
            data[impact] = stage_values

        return data
    

if __name__ == '__main__':
    pass