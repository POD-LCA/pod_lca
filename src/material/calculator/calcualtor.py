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
    
    def get_data_by_LCstage(self, impact_category):

        impacts_dict = self.project.get_model().get_impacts()

        vals = {}
        for stage in impacts_dict.keys():
            impact_lst = impacts_dict[stage]
            vals[stage] = 0.0
            for impact in impact_lst:
                vals[stage] += impact.get_impact(impact_category)

        return vals
    
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
    