
class DatabaseManager:

    def __init__(self, project):
        self.project = project
        self.data = None
        self.impact_categories = ['GWP', 'acid_pot', 'eutro_pot', 'ozone_dep', 'smog']

    def set_data(self, data):

        self.data = data

    def get_data(self):

        return self.data
    
    def get_impact_categories(self):

        return self.impact_categories    

    @staticmethod
    def import_data_from_JSON(file_path):

        pass

    def get_impact_data(self, row):

        if self.data is not None:
            row_id = self.data.index[self.data['Flow'] == row][0]
            return self.data.iloc[row_id]
        # check the data type with line 20 of process.py