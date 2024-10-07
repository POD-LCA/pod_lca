
class Unit:

    def __init__(self, name):
        self.name = name
        self.standard_notation = None
        self.base_unit = None
        self.prefix = None
        self.type = None
        self.is_compund_unit = False
        self.components = {}

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

    @staticmethod
    def is_type(unit, type):

        if unit.type == type:
            return True
        else:
            return False 
        
    def generate_all(self):

        pass

    def print_all(self):

        pass