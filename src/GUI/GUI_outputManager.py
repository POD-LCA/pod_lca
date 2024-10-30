

class GUIOutputManager():

    @staticmethod
    def get_output_data(project, impact_categories, model):

        data = {}
        for impact in impact_categories:
            data[impact] = project.get_calculator().get_data_by_LCstage(impact_category=impact, model_name=model)
        
        return data

    @staticmethod
    def get_hotspots(project, model, impact_category="GWP"):

        return  project.get_calculator().hot_spot_analysis(model, impact_category, printout=False)

