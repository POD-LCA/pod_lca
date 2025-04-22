from lca_modules.impacts.impacts import Impacts
from lca_modules.impacts.impact_categories  import IMPACT_CATEGOREIS

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class WasteProcess:
    """ Waste process a waste object is subjected to.

        Attributes
        ----------
        parent : Waste Obj.
            Waste object for which the waste processing belong.
        name : str
            Name to identifying the waste process and parent.
        process_name : str.
            Name of the process: e.g., 'Landfill', 'Recycle', 'Compost'.
        qty : float.
            Quantity of the parent object subjected to this process.
        unit : Unit Obj.
            Unit of measurement.
        life_cycle_stage : str.
            Life cycle stage of this process: e.g., 'C3', 'C4'.
        unit_impacts : Impact Obj.
            Unit impacts of the process.
        location : Location Obj.
            Location where the process occurs.
        transporation_link : Link Obj.
            Transportation of the waste object from parent's location to process location.
        linked_to : WasteProcess Obj.
            A follow up process. e.g, Recycle processing (C3) and Reuse (D).
        linked_from : WasteProcess Obj.
            A previous end-of-life process. e.g, Recycle processing (C3) and Reuse (D).
    """
    def __init__(self):
        self.parent = None
        self.process_name = None
        self.qty = 0.0
        self.unit = None
        self.life_cycle_stage = None
        self.unit_impacts = Impacts.from_parent(self)
        self.location = None
        self.transportation_link = None
        self.linked_to = None
        self.linked_from = None


    def __str__(self):
        return f"Waste Process(waste product={self.get_parent().get_name()}, name={self.get_process_name()}, LC stage={self.get_life_cycle_stage()}, qty={self.get_qty()} {self.get_unit().get_standard_notation()})"

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, parent, process_name, qty, unit, life_cycle_stage):
        """ Create new waste process.
        
            Parameters
            ----------
            parent : Waste Obj.
                Waste object for which the waste processing belong.
            process_name : str.
                Name of the process: e.g., 'Landfill', 'Recycle', 'Compost'.
            qty : float.
                Quantity of the parent object subjected to this process.
            unit : Unit Obj.
                Unit of measurement.
            life_cycle_stage : str.
                Life cycle stage of this process: e.g., 'C3', 'C4'.            
        """

        waste_process = cls()

        waste_process.set_parent(parent)
        waste_process.set_life_cycle_stage(life_cycle_stage)
        waste_process.set_process_name(process_name)
        waste_process.set_name()
        waste_process.set_qty(qty)
        waste_process.set_unit(unit)
        

        #TODO: create transportaton links/ set and get objects/ setting location as well

        return waste_process

    # ================================
    # Setters
    # ================================    
    def set_parent(self, parent):
        """ Set parent Waste object of the Waste Processing.
        
            Parameters
            ----------
            parent : Waste Obj.
                Waste object for which the waste processing belong.
        """
        self.parent = parent

        return parent
    
    def set_process_name(self, name):
        """ Set the process name.

            Parameters
            ----------
            name : str
                Name of the process: e.g., 'Landfill', 'Recycle', 'Compost'

        """
        self.process_name = name

        self.set_unit_impacts()
        
        return self
    
    def set_name(self, name=None):
        """ Set name of the process identifying the parent and process.
        
            Parameters
            ----------
            name : str
                Name identifyer.
        """

        if name is None:
            self.name = self.get_parent().get_name() + '-' + self.get_process_name()
        else:
            self.name = name

        return self
            
    def set_qty(self, qty):
        """ Set quantity of the parent subjected to this waste process.
        
            Parameters
            ----------
            qty : float.
                Quantity of the parent object subjected to this process.

        """

        self.qty = qty

        if not (self.get_linked_process() is None):
            if self.get_unit() == self.get_linked_process().get_unit():
                self.get_linked_process().set_qty(qty)
            else:
                self.get_linked_process().set_unit(self.get_unit())
                self.get_linked_process().set_qty(qty)

    def set_unit(self, unit):
        """ Set unit of measurement for the waste amount processed.
        
            Parameters
            ----------
            unit : Unit Obj.
                Unit of measurement.
        """

        if self.get_unit() is None:
            self.unit = unit
        else:
            value_in = self.get_qty()
            unit_in = self.get_unit()

            conversion_factor = unit_in.get_conversion_factor(unit)

            if conversion_factor is not None:
                self.unit = unit
                self.set_qty(value_in * conversion_factor)
                # TODO: update unit impacts
            else:
                raise ValueError(f"The new unit ({unit}) is incompatible with the existing unit ({unit_in}).")

        return self

    def set_life_cycle_stage(self, life_cycle_stage):
        """ Set life cycle stage of the product/process.

            Parameters
            ----------
            life_cycle_stage : str
                Life cycle stage of the product/process.
        """

        if self.get_life_cycle_stage() is None:
            self.life_cycle_stage = life_cycle_stage
        else:
            previous_stage = self.get_life_cycle_stage()
            self.life_cycle_stage = life_cycle_stage
            
            impact_obj = self.get_impacts()
            parent_impacts_list = self.get_parent().get_impacts()[previous_stage]
            for impact in parent_impacts_list:
                if impact == impact_obj:
                    parent_impacts_list.remove(impact_obj)
                    break

            self.get_parent().get_impacts()[life_cycle_stage].append(impact_obj)

        return self

    def set_unit_impacts(self):
        """ Set unit impacts of the waste process.
        """

        material = self.get_parent().get_impact_database_entry()
        process = self.get_process_name()
        life_cycle_stage = self.get_life_cycle_stage()
        database = self.get_parent().get_parent().get_building().get_eol_database()

        database_entry = database.get_data_entry(material, process, life_cycle_stage)
        impacts = {key: database_entry[key] for key in IMPACT_CATEGOREIS}

        # TODO: check linked processess

        # TODO: check units are consistent

        self.get_unit_impacts().update_impact_qty(impacts)

    def set_location(self, location):
        """ Set location of the waste process facility.

            Parameters
            ----------
            location : Location Obj.
                Location of the waster process facility.
        """

        self.location = location
        
        # TODO: update the transportation

    def set_linked_process(self, process):
        """ Set a linked process to the current process.

            Parameters
            ----------
            process : WasteProcess Obj.
                Secondary process following the current process.
        """

        self.linked_to = process
        process.linked_from = self

        return self

    # ================================
    # Getters
    # ================================
    def get_parent(self):
        """ Get parent Waste object of the Waste Processing.
        
            Returns
            -------
            Waste Obj.
                Waste object for which the waste processing belong.
        """
        return self.parent

    def get_process_name(self):
        """ Get the process name.

            Returns
            -------
            str
                Name of the process: e.g., 'Landfill', 'Recycle', 'Compost'
        """       
        return self.process_name
    
    def get_name(self):
        """ Get name of the process identifying the parent and process.
        
            Returns
            -------
            str
                Name identifyer.
        """

        return self.name
        
    def get_qty(self):
        """ Get quantity of the parent subjected to this waste process.
        
            Returns
            -------
            float.
                Quantity of the parent object subjected to this process.
        """
        return self.qty
    
    def get_unit(self):
        """ Get unit of measurement for the waste amount processed.
        
            Returns
            -------
            unit : Unit Obj.
                Unit of measurement.
        """        
        return self.unit
    
    def get_life_cycle_stage(self):
        """ Retrieve the life cycle stage corresponding to the waste process.

            Returns
            -------
            str
                Corresponding life cycle stage.
        """
        return self.life_cycle_stage

    def get_unit_impacts(self):
        """ Get unit impacts of the waste process.

            Returns
            -------
            Impact Obj.
                Unit impacts of the process.
        """
        return self.unit_impacts

    def get_linked_process(self, to=True):
        """ Get the linked process to the current process.

            Parameters
            ----------
            to : bool
                If True, return the process linked to, else linked from.

            Returns
            -------
            WasteProcess Obj.
                Secondary process following the current process.
        """
        if to:
            return self.linked_to
        else:
            return self.linked_from
    
if __name__ == '__main__':
    pass    