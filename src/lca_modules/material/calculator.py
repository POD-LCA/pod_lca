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
        
    @staticmethod
    def get_impacts_by_LCstages(impact_category, model):
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
            data = {}
            for stage in impacts_dict.keys():
                impact_lst = impacts_dict[stage]
                data[stage] = 0.0
                for impact in impact_lst:
                    data[stage] += impact.get_impact(impact_category)

            return data
    
    @staticmethod
    def get_impacts_by_LCstages_models(impact_category, model_lst=['Model_0']):
        """ Returns impact data by life cycle stage for given multiple model and impact category.
            
            Parameters
            ----------
            impact_category : str
                Name of the Impact category.
            model_lst : List of Model Obj.
                List of the models.

            Returns
            -------
            dict
                Impacts dictionary where {model_name (str): { stage (str): quantity of impact (float)}}.
        """

        data ={}
        for model in model_lst:
            data[model.get_name()] = Calculator.get_impacts_by_LCstages(impact_category, model)
        
        return data
        
    @staticmethod
    def get_impacts_by_LCstages_models_items(impact_category, model_lst=['Model_0']):
        """ Returns impact data by life cycle stage for given multiple model and impact category, with impacts 
            identifieable by individaul item.
            
            Parameters
            ----------
            impact_category : str
                Name of the Impact category.
            model_lst : List of Model Obj.
                List of the models.

            Returns
            -------
            dict
                Impacts dictionary where {model_name (str): {stage (str): {item_name (str): quantity of impact (float)}}.

        """

        data ={}
        for model in model_lst:
            model_data = {}
            impacts_dict = model.get_impacts()
            for stage in impacts_dict.keys():
                stage_data = {}
                impact_lst = impacts_dict[stage]
                for impact in impact_lst:
                    stage_data[impact.get_parent().get_name()] = impact.get_impact(impact_category)
                model_data[stage] = stage_data
            data[model.get_name()] = model_data

        return data

    @staticmethod
    def get_impacts_by_LCstages_models_hotspots(impact_category, model_lst=['Model_0']):

        pass # TODO implement
    
    @staticmethod
    def get_impacts_by_impactcategorys_models_LCstage(impact_categories,  model_lst=['Model_0']):
        """ Returns data for a barchart.
            
            Parameters
            ----------
            impact_categories : List of str
                List of impact categories.
            model_lst : List of Model Obj.
                List of the models.

            Returns
            -------
            dict
                Impacts dictionary where {model_name (str): {impact_category (str): {stage (str): quantity of impact (float)}}.
        """

        data = {model.get_name(): {} for model in model_lst}
        for impact_category in impact_categories:
            for model in model_lst:
                data[model.get_name()][impact_category] = Calculator.get_impacts_by_LCstages(impact_category, model)
        
        return data

    # =================================
    # PLOT DATA METHODS
    # =================================
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
                model_data, _ = Calculator.get_impacts_by_LCstages(impact, model)
                impact_data[model.get_name()] = model_data  

            if stage == 'all':
                stage_values = {model: sum(impact_data[model].values()) for model in impact_data}
            else:
                stage_values = {model: values[stage] for model, values in impact_data.items()}
            data[impact] = stage_values

        return data
    

if __name__ == '__main__':
    pass