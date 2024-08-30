import pandas

class DatabaseManager:

    def __init__(self, project):
        self.project = project
        self.data = None
        self.impact_categories = ['GWP', 'acid_pot', 'eutro_pot', 'ozone_dep', 'smog']

    def __reduce__(self):
        
        return (self.__class__, (None), {"project": self.project, "data": self.data, 
                                         "impact_categories": self.impact_categories})
    
    def __setstate__(self, state):
        self.__dict__.update(state)

    def set_data(self, data):

        self.data = data

    def get_data(self):

        return self.data
    
    def get_impact_categories(self):

        return self.impact_categories    

    def get_impact_data(self, row):

        if self.data is not None:
            row_id = self.data.index[self.data['Flow'] == row][0]
            return self.data.iloc[row_id]
    
    # =================================
    # DATA IMPORT METHODS
    # =================================

    def import_data_from_JSON(self, file_path):

        impacts = pandas.read_csv(filepath_or_buffer=file_path)
        # TODO: Update to asign columns by impact category
        self.set_data(impacts)
