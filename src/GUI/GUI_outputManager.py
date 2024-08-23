from material.projectManager.outputManager import OutputManager

class GUIOutputManager(OutputManager):

    @staticmethod
    def get_output_data(project, impact_category):

        return project.get_calculator().get_data_by_LCstage(impact_category='GWP')