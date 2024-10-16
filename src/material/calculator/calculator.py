
import matplotlib.pyplot as plt
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
    
    # =================================
    # UNIT CONVERSION/CHECK METHODS
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
        """ Returns heights and x-labels for a barchart.
        """

        project = self.get_project()
        calcualtor = project.get_calculator()
        data_dict ={}
        for model_name in model_lst:
            data_dict[model_name], stages = calcualtor.get_data_by_LCstage(impact_category, model_name)
        
        return  stages, data_dict
        

    def get_barchart2_data (self,impact_category, model_lst= ['Model_0']):

        data_name=[]
        data_qty=[]
        data_len=[]

        project = self.project.get_model(model_lst[0]).get_project()
        model = project.get_model(model_lst[0])

        for i in model.get_impacts():
            data_len.append(len(model.get_impacts()[i]))
            for j in model.get_impacts()[i]:
                data_qty.append(j.get_impact(impact_category))
                data_name.append(j.get_parent().__reduce__()[1][1])

        impacts = {}
        start_index = 0

        for i, length in enumerate(data_len):
            end_index = start_index + length

            for j in range(start_index, end_index):
                impacts[data_name[j]] = np.array([0] * i + [data_qty[j]] + [0] * (len(data_len) - i - 1))
            start_index = end_index

        return data_name, data_qty, data_len, impacts


    def get_barchart3_data (self, impact_category, model_lst= ['Model_0']):

        labels = ['A1', 'A2', 'A3']
        title='Environmental Impacts by Stage'
        project = self.project.get_model(model_lst[0]).get_project()
        calcualtor = project.get_calculator()

        data=[]
        for i in impact_category:

            globals()['data_dict_' + i] = calcualtor.get_data_by_LCstage(i)[0]
            globals()['plt_data_' + i] = [globals()['data_dict_' + i]["A1"], globals()['data_dict_' + i]["A2"], globals()['data_dict_' + i]["A3"]]
            data.append(globals()['plt_data_' + i])


        impact_by_stage = {labels[i]: np.array([row[i] for row in data]) for i in range(len(labels))}
        
        return impact_by_stage

    # =================================
    # ANALYSIS METHODS
    # =================================

    def hot_spot_analysis(self, model='Model_0', impact_category="GWP", printout=False):
        """ Determines the hotspot of the model.
            The hotspots are the largest group out of (a) top 20% contributors to the impact or (b) the smallest group of contributors to the 80% (or more) of GWP.

            Parameters
            ----------
            model : str
                Name of the model considered.
            impact_category : str
                Impact category considered.
            printout : bool
                Printout the results if true.
            
            Retrurn
            -------
            List of Master Obj.
                Hotspot objects.
        """

        impacts = self.get_project().get_model(model).get_impacts()

        impacts_lst = []
        for key, list in impacts.items():
            impacts_lst.extend(list)

        if len(impacts_lst) > 0:
            val_lst = [impact.get_impact(impact_category) for impact in impacts_lst]
            total_impact = sum(val_lst)
            no_contributors = len(val_lst)

            hot_spots =[]
            
            biggest_contribution = max(val_lst)
            if biggest_contribution == 0.0:
                return None
            max_index = val_lst.index(biggest_contribution)
            hot_spots.append(impacts_lst[max_index].get_parent())
            contributions_in_hotspots = biggest_contribution

            all_found = True if len(hot_spots) >= 0.2 * no_contributors and contributions_in_hotspots >= 0.8 * total_impact else False
            
            while not all_found:
                val_lst[max_index] = 0.0

                biggest_contribution = max(val_lst)
                if biggest_contribution == 0.0:
                    break
                max_index = val_lst.index(biggest_contribution)
                hot_spots.append(impacts_lst[max_index].get_parent())
                contributions_in_hotspots += biggest_contribution

                all_found = True if len(hot_spots) >= 0.2 * no_contributors and contributions_in_hotspots > 0.8 * total_impact else False

            if printout:
                print("*"*50 + "\nHOTSPOTS\n" + "*"*50)
                for obj in hot_spots:
                    print(obj, "Impact ({}):".format(impact_category), obj.get_impacts().get_impact(impact_category))

            return hot_spots


if __name__ == '__main__':
    pass