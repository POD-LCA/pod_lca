
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ...units import UNITS_MAP


class TemplateModels:

    @classmethod
    def from_template_model(cls, name, type, location, built_year, life_span, file_path, building_data):
        """ Build a building from a template model data given in a CSV file.
        
        Parameters
        ----------
        name : str
            Name of the building.
        type : {'Commercial', 'Residential'}
            Type of building.
        location : ~pod_lca.location.Location
            Location of the building site.
        built_year: int
            Built year of the building.
        life_span: int
            Life span of the building in years.
        file_path : int
            File path to template model bill of material list.
        building_data : dict
            Dictionary provding building data
        
        Returns
        -------
        ~pod_lca.buildings.Building
            Building built.
        """
        building = cls.new(name, type, location, built_year, life_span)
        building.set_databases()

        building.set_template_model(file_path, building_data)

        return building
    
    # ================================
    # Setters
    # ================================   
    def set_template_model(self, file_path, building_data):
        """ Set attributes to an existing building.
        
        Parameters
        ----------
        file_path : int
            File path to template model bill of material list.
        building_data : dict
            Dictionary provding building data
        """
        self.add_floors(building_data['no_floors'], 
                        building_data['f2f_height'], 
                        building_data['floor_plan'], 
                        building_data['floors_below_grade'], 
                        UNITS_MAP[building_data['geometry_units']])
        
        construction_energy_use = building_data["construction_energy_use"] if "construction_energy_use" in building_data else 0.0
        energy_units = UNITS_MAP[building_data["construction_energy_use_unit"]] if "construction_energy_use" in building_data else MEGA * WATT_HOUR
        self.set_building_level_products(logistic_type=building_data['logistic_type'], 
                                         construction_electricity_consumption=construction_energy_use, 
                                         electricity_unit=UNITS_MAP[building_data["construction_energy_use_unit"]])

        self.make_structure('from template', template_bom=file_path)
        self.make_envelope()    

        return self


if __name__ == '__main__':
    pass
