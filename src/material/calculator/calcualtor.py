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
        
    def get_data_by_LCstage(self, impact_category):

        impacts_dict = self.project.get_model().get_impacts()

        vals = {}
        for stage in impacts_dict.keys():
            impact_lst = impacts_dict[stage]
            vals[stage] = 0.0
            for impact in impact_lst:
                vals[stage] += impact.get_impact(impact_category)

        return vals  

    def Barchart (self, impact_category):

        project = self.project.get_model().get_project()
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
            # Create a dynamic variable name for data_dict
            globals()['data_dict_' + i] = calcualtor.get_data_by_LCstage(i)
            
            # Create a dynamic variable name for plt_data
            globals()['plt_data_' + i] = [globals()['data_dict_' + i]["A1"], globals()['data_dict_' + i]["A2"], globals()['data_dict_' + i]["A3"]]

            data.append(globals()['plt_data_' + i])

        impact_by_stage = {labels[i]: np.array([row[i] for row in data]) for i in range(len(labels))}

        # Width of the bars
        width = 0.6  

        # Create the plot
        fig, ax = plt.subplots()
        bottom = np.zeros(len(impact_category))  # Initialize the bottom of the stacked bars

        # Stacked bar plot
        for stage, impacts in impact_by_stage.items():
            p = ax.bar(impact_category, impacts, width, label=stage, bottom=bottom)
            bottom += impacts  # Update the bottom for stacking
            ax.bar_label(p, label_type='center')

        # Set plot title and legend
        ax.set_title(title)
        ax.legend()

        # Show the plot
        plt.show()
    
