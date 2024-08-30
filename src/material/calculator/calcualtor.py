class Calculator():

    def __init__(self, project):
        self.project = project
 
    def __reduce__(self):
        
        return (self.__class__, (None), {"project": self.project})
    
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
    

    
    