from pandas import DataFrame, read_csv, concat

class DatabaseManager:

    def __init__(self, project):
        self.project = project
        self.impact_categories = {'GWP':0.0, 'acid_pot':0.0, 'eutro_pot':0.0, 'ozone_dep':0.0, 'smog':0.0}
        self.data_headers = ['Flow','Unit'] + list(self.impact_categories.keys())
        self.data = DataFrame(columns=self.data_headers)

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

    def import_data_from_CSV(self, file_path, headers=None, multipliers=None):
        
        if headers == None:
            headers = self.data_headers
        header_map = dict(zip(headers, self.data_headers))

        new_data = read_csv(filepath_or_buffer=file_path)
        new_data = new_data.rename(columns=header_map)

        if not multipliers == None:
            n = len(headers)
            for i in range(n):
                if i>1:
                    new_data[header_map[headers[i]]] = new_data[header_map[headers[i]]] * multipliers[i-2]

        if self.get_data().empty:
            self.set_data(new_data)
        else:
            self.set_data(concat([self.get_data(), new_data], ignore_index=True))

    def set_custom_entry(self, flow, unit, impacts):

        tmp_data = impacts
        tmp_data['Flow'] = flow
        tmp_data['Unit'] = unit

        self.data.loc[len(self.data)] = tmp_data
