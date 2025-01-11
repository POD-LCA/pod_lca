from lca_modules.impacts.impact_categories import IMPACT_CATEGOREIS
from utilities.objects.array_methods import get_attribute_as_list, sort_by_attribute

import numpy as np

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu; mhtaba@uw.edu"
__version__ = "0.1.0"


class Calculator():
    """
    Calculator object carries out varies calculations on the project data.
    """
 
    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls):
        """ Create new calculator.
        """

        return cls()
    
    # ================================
    # Calcualotror methods
    # ================================
    @staticmethod
    def get_total_impact(model, impact_cat):
        """ Calculate the total impact of the products and processes in the model.
        
            Parameters
            ----------
            model: Model Obj.
                Model in which the impacts are calculated.
            impact_cat : str
                Impact category considered, including 'weighted'.

            Returns
            -------
            float
                Total impact value.
        """

        impacts_dict = model.get_impacts()
        impacts_lst = []
        for key, lst in impacts_dict.items():
            impacts_lst.extend(lst)

        if impact_cat not in list(IMPACT_CATEGOREIS.keys()) + ['weighted']:
            raise AttributeError(f"{impact_cat} does not exist in the current project.")
        else:
            if impact_cat == 'weighted':
                val_lst = [impact.get_weighted_impact() for impact in impacts_lst]
            else:
                val_lst = [impact.get_impact(impact_cat) for impact in impacts_lst]

            return sum(val_lst)
        
    # =================================
    # PLOT DATA METHODS
    # =================================
    @staticmethod
    def get_data_by_LCstage(impact_category, model):
        """ Returns impact data by life cycle stage for given model and impact category.

            Parameters
            ----------
            impact_category : str
                Name of impact category.
            model : Model Obj
                The model considered.

            Returns
            -------
            dict
                Impacts dictionary where {Life Cycle stage (str) : quantity of impact (float)}.

            Raises
            ------
                AttributeError : impact category doe not exist in the current project
        
        """

        impacts_dict = model.get_impacts()

        if impact_category not in IMPACT_CATEGOREIS.keys():
            raise AttributeError(f"{impact_category} does not exist in the current project.")
        else:
            vals = {}
            for stage in impacts_dict.keys():
                impact_lst = impacts_dict[stage]
                vals[stage] = 0.0
                for impact in impact_lst:
                    vals[stage] += impact.get_impact(impact_category)

            return vals, impacts_dict.keys()
    
    @staticmethod
    def get_barchart_data(impact_category, model_lst=['Model_0']):
        """ Returns data for a barchart.
            
            Parameters
            ----------
            impact_category : str
                Name of the Impact category.
            model_lst : List of Model Obj.
                List of the models.

            Returns
            -------
            dict_keys
                x-labels.
            dict
                Heights of bars: { model_name (str): { stage (str): height (float)}}.
        """

        data_dict ={}
        for model in model_lst:
            data_dict[model.get_name()], stages = Calculator.get_data_by_LCstage(impact_category, model)
        
        return  stages, data_dict
        
    @staticmethod
    def get_barchart2_data (impact_category, model):
        """ Returns data for a barchart.
            
            Parameters
            ----------
            impact_category : str
                Name of the Impact category.
            model : Model Obj.
                Model.

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
        data_name=[]
        data_qty=[]
        data_len=[]

        model_name = model.get_name()

        for lc_stage in model.get_impacts():
            item_count = 0
            other_qty = 0.0
            impacts_lst = model.get_impacts()[lc_stage]
            impacts_lst_sorted = sort_by_attribute(impacts_lst, impact_category, descending=True)
            for impact in impacts_lst_sorted:
                if impact.get_parent().is_hotspot:
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

    @staticmethod
    def get_barchart3_data(impact_category, model= 'Model_0'):
        """ Returns data for a barchart.
            
            Parameters
            ----------
            impact_category : str
                Name of the Impact category.
            model : Model Obj.
                The model considered.

            Returns
            -------
            dict
                #TODO: update.
        """

        labels = ['A1', 'A2', 'A3']
        data=[]
        for category in impact_category:
            tmp_dict, _ = Calculator.get_data_by_LCstage(category, model)
            plt_data = [tmp_dict["A1"], tmp_dict["A2"], tmp_dict["A3"]]
            data.append(plt_data)

        impact_by_stage = {labels[i]: np.array([row[i] for row in data]) for i in range(len(labels))}
        
        return impact_by_stage

    @staticmethod
    def get_spider_chart_data (impact_category, model_lst=['Model_0'], stage='all'):
        """ Returns data for a barchart.
            
            Parameters
            ----------
            impact_category : List
                List of impact categories.
            model_lst : List of Model Obj.
                List of the models.
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

            for model in model_lst:
                model_data, _ = Calculator.get_data_by_LCstage(impact, model)
                impact_data[model.get_name()] = model_data  

            if stage == 'all':
                stage_values = {model: sum(impact_data[model].values()) for model in impact_data}
            else:
                stage_values = {model: values[stage] for model, values in impact_data.items()}
            data[impact] = stage_values

        return data
    

if __name__ == '__main__':
    pass