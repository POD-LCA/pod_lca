import matplotlib.pyplot as plt
import numpy as np

class Calculator():

    def __init__(self, project):
        self.project = project
        self.conversions = [{'m': 1000.0, 'km': 1.0, 'mi': 0.621371},
                            {'g': 1000.0, 'kg': 1.0, 't': 0.001, 'lb': 2.20462},
                            {'l': 1.0, 'm3': 0.01, 'gal':0.264172},
                            {'J': 1000.0, 'kJ': 1.0, 'MJ': 0.001, 'kWh': 2.77778e-4, 'MWh': 2.77778e-7},
                            {'kgkm': 1.0, 'tkm': 0.001, 'lbmi':1.369887}]
 
    def __reduce__(self):
        
        return (self.__class__, (None,), {"project": self.project})
    
    def __setstate__(self, state):
        self.__dict__.update(state)
    
    def convert_units(self, from_unit, to_unit, amount):

        for group in self.conversions:
            if from_unit in group:
                if to_unit in group:
                    return amount * group[to_unit] / group[from_unit]
            
        return None
            
    def conversion_factor(self, from_unit, to_unit):

        return self.convert_units(from_unit, to_unit, amount=1.0)

    def get_units_list(self):

        units = []
        for items in self.conversions:
            units.extend(list(items.keys()))

        return units
    
    def is_mass_unit(self, unit):

        if self.conversion_factor(unit, 'kg') == None:
            return False
        else:
            return True
        
    def get_data_by_LCstage(self, impact_category, model_name='Model_0'):

        impacts_dict = self.project.get_model(model_name).get_impacts()

        vals = {}
        for stage in impacts_dict.keys():
            impact_lst = impacts_dict[stage]
            vals[stage] = 0.0
            for impact in impact_lst:
                vals[stage] += impact.get_impact(impact_category)

        return vals  

    def Barchart (self, impact_category, model_name='Model_0'):

        project = self.project.get_model(model_name).get_project()
        calcualtor = project.get_calculator()
        data_dict = calcualtor.get_data_by_LCstage(impact_category)
        plt_data = [data_dict["A1"], data_dict["A2"], data_dict["A3"]]
        data_dict= data_dict.keys()

        fig, ax = plt.subplots()
        bar_labels = ['A1', 'A2', 'A3']
        bar_colors = ['tab:red', 'tab:blue', 'tab:orange']

        ax.bar(data_dict, plt_data, label=bar_labels, color=bar_colors)

        ax.set_ylabel(f'{impact_category} Impact')
        ax.set_title('Life cycle stages')
        ax.legend(title='Life cycle stage color')

        plt.show()
        
    def Multi_bar_chart (self,impact_category):

        labels = ['A1', 'A2', 'A3']
        title='Environmental Impacts by Stage'
        project = self.project.get_model().get_project()
        calcualtor = project.get_calculator()

        data=[]
        for i in impact_category:

            globals()['data_dict_' + i] = calcualtor.get_data_by_LCstage(i)
            globals()['plt_data_' + i] = [globals()['data_dict_' + i]["A1"], globals()['data_dict_' + i]["A2"], globals()['data_dict_' + i]["A3"]]
            data.append(globals()['plt_data_' + i])

        impact_by_stage = {labels[i]: np.array([row[i] for row in data]) for i in range(len(labels))}

        width = 0.6  
        fig, ax = plt.subplots()
        bottom = np.zeros(len(impact_category)) 

        for stage, impacts in impact_by_stage.items():
            p = ax.bar(impact_category, impacts, width, label=stage, bottom=bottom)
            bottom += impacts  
            ax.bar_label(p, label_type='center')

        ax.set_title(title)
        ax.legend()
        plt.show()
    
    def barchart_by_parts (self,impact_category):

        data_name=[]
        data_qty=[]
        data_len=[]

        project = self.project.get_model().get_project()
        model = project.get_model()

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

        stages = ('A1', 'A2', 'A3')
        width = 0.6  # the width of the bars: can also be len(x) sequence

        fig, ax = plt.subplots()
        bottom = np.zeros(3)

        for stage, impact in impacts.items():
            p = ax.bar(stages, impact, width, label=stage, bottom=bottom)
            bottom += impact
            ax.bar_label(p, label_type='center')

        ax.set_title('Life cycle stages')
        ax.legend()
        plt.show()