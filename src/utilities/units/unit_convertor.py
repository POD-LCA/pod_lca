
import csv 


class Unit:

    def __init__(self, name, standard_notation, type, is_metric):
        self.name = name
        self.standard_notation = standard_notation
        self.base_unit = None
        self.prefix = None
        self.type = type
        self.is_compund_unit = False
        self.is_metric = is_metric
        self.components = {}

    def get_name(self):

        return self.name
    
    def get_standard_notation(self):

        return self.standard_notation
    
    def get_type(self):

        return self.type

    def convert(self, from_unit, to_unit):

        if Unit.is_type(to_unit, from_unit.type):
            if from_unit.is_compund_unit:
                pass
                # for each component do conversion, and combine back
            else:
                if from_unit.base_unit == from_unit.base_unit:
                    pass
                    # do prefix convert
                else:
                    pass
                    # get conversion factor to convert
                
        else:
            raise TypeError
        
    def prefix_convert(self, from_prefix, to_prefix):

        pass

class UnitCalculator:

    def __init__(self):
        self.base_units_path = r'data\base_units.csv'
        self.metric_prefixes_path = r'data\metric_prefixes.csv'
        self.units = {}


    @staticmethod
    def is_type(unit, type):

        if unit.type == type:
            return True
        else:
            return False 
   
    def create_base_units_from_database(self):

        with open(self.base_units_path, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader) # TODO: check rows are correct order
            for row in csv_reader:
                is_metric = True if row[3] == 'TRUE' else False
                new_unit = Unit(row[0], row[1], row[2], is_metric)
                new_unit.is_compund_unit = row[4]
                if new_unit.is_compund_unit:
                    new_unit.components = row[5].split(',')

                self.units[new_unit.name] = new_unit

    def create_compound_units(self):

        self.units.update(self.create_metrix_prefixed_units())
        # create areas (replace square meter)
        # creart volumes
        # create transportation conjugates (distance time mass)
        # create energy conjugates
    
    def create_metrix_prefixed_units(self):

        new_units = {}
        skip = ['cubic meter', 'square meter'] # skip these base units

        with open(self.metric_prefixes_path, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader) # TODO: check rows are correct order
            if not (header[0] == "name" and header[1] == "symbol" and header[3] == "Common"):
                raise ImportError(f"Headers of import file not compatible.")
            for row in csv_reader:
                if row[3] == "Yes": # prefix is common
                    for unit in self.units:
                        base_unit = self.units[unit]
                        if base_unit.is_metric and base_unit.get_name() not in skip:
                            name = row[0] + base_unit.get_name()
                            standard_notation = row[1] + base_unit.get_standard_notation()
                            new_unit = Unit(name, standard_notation, base_unit.type, True)
                            self.base_unit = base_unit
                            self.prefix = row[0]

                            new_units[new_unit.name] = new_unit
        
        return new_units
    
    def print_all(self):

        for unit in self.units:
            print(self.units[unit].name + "(" + self.units[unit].standard_notation + ")")

    @staticmethod
    def create_conversion_matrices():

        pass


if __name__ == "__main__":
    unit_calculator =  UnitCalculator()
    unit_calculator.create_base_units_from_database()

    unit_calculator.create_compound_units()

    unit_calculator.print_all()
