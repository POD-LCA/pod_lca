import pandas

class DatabaseManager:

    def __init__(self, project):
        self.project = project
        self.data = None
        self.impact_categories = {'GWP':0.0, 'acid_pot':0.0, 'eutro_pot':0.0, 'ozone_dep':0.0, 'smog':0.0}

    def __reduce__(self):
        
        return (self.__class__, (None,), {"project": self.project, "data": self.data, 
                                         "impact_categories": self.impact_categories})
    
    def __setstate__(self, state):
        self.__dict__.update(state)

    def set_data(self, data):

        self.data = data

    def set_impact_categories(self, impact_cats):

        self.impact_categories = dict.fromkeys(impact_cats, 0.0)

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

    def import_data_from_CSV(self, file_path, order=None):

        impacts = pandas.read_csv(filepath_or_buffer=file_path)

        impact_headers_list = list(self.get_impact_categories().keys())

        headers_list = ['Flow', 'Units'] + impact_headers_list
        new_order = list(range(len(headers_list))) if order is None else order
        impact_headers_ordered = [headers_list[i] for i in new_order]

        impacts.columns = impact_headers_ordered
        self.set_data(impacts)
