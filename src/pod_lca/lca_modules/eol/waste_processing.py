__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..carbon_storage import CarbonStorage
from ..impacts import Impacts
from ..impacts import Emissions
from ...units import INCH
from ...units import UNITS_MAP
from ...utilities import config
from ...utilities import DataImporter


class WasteProcess:
    """Waste process a waste object is subjected to.

    Attributes
    ----------
    parent : ~pod_lca.eol.Waste
        Waste object for which the waste processing belong.
    process_name : {'Landfill', 'Recycle', 'Compost', 'Incinerate'}
            End-of-life pathway:

            - `'Landfill'`: transporting waste to a landfill.
            - `'Recycle'`: transporting waste to a recycler.
            - `'Compost'`: transporting to a composting facility.
            - `'Incinerate'`: transporting to an incinerator.
            Default to 'Incinerate'.
    qty : float
        Quantity of the parent object subjected to this process.
    unit : ~pod_lca.units.Unit
        Unit of measurement.
    life_cycle_stage : {'C3', 'C4', 'D'}
        Life cycle stage of this process.
    unit_impacts :  ~pod_lca.impacts.Impacts
        Unit impacts of the process.
    unit_emissions :  ~pod_lca.impacts.Emissions
        Unit emissions of the process.
    location : ~pod_lca.location.Location
        Location where the process occurs.
    transporation_leg : ~pod_lca.transportation.TransportationLeg
        Transportation of the waste object from parent's location to process location.
    linked_to : ~pod_lca.eol.WasteProcess
        A follow up process. e.g, Recycle processing (C3) and Reuse (D).
    linked_from : ~pod_lca.eol.WasteProcess
        A previous end-of-life process. e.g, Recycle processing (C3) and Reuse (D).
    """

    def __init__(self):
        self.parent = None
        self.process_name = None
        self.qty = 0.0
        self.unit = None
        self.life_cycle_stage = None
        self.unit_impacts = Impacts.from_parent(self)
        self.unit_emissions = Emissions.from_parent(self)
        self.unit_stored_carbon_release = Emissions.from_parent(self)
        self.location = None
        self.transporation_leg = None
        self.linked_to = None
        self.linked_from = None

        self.gas_capture_system = None

    def __str__(self):
        return f"Waste Process(waste product={self.get_parent().get_name()}, name={self.get_process_name()}, LC stage={self.get_life_cycle_stage()}, qty={self.get_qty()} {self.get_unit().get_standard_notation()})"

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, parent, process_name, qty, unit, life_cycle_stage, linked_process=None, **kwargs):
        """Create new waste process.

        Parameters
        ----------
        parent : ~pod_lca.eol.Waste
            Waste object for which the waste processing belong.
        process_name : {'Landfill', 'Recycle', 'Compost', 'Incinerate'}
                End-of-life pathway:

                - `'Landfill'`: transporting waste to a landfill.
                - `'Recycle'`: transporting waste to a recycler.
                - `'Compost'`: transporting to a composting facility.
                - `'Incinerate'`: transporting to an incinerator.
                Default to 'Incinerate'.
        qty : float
            Quantity of the parent object subjected to this process.
        unit : ~pod_lca.units.Unit
            Unit of measurement.
        life_cycle_stage : {'C3', 'C4', 'D'}
            Life cycle stage of this process.
        linked_process : {None, 'C4', 'D'}
            Linked waste process.

        Other Parameters
        ----------------
        gas_capture_system : {'Energy Recovery', 'Flaring'}
            Applicable for landfill process only. Type of landfill gas capture system.

        Returns
        -------
        ~pod_lca.eol.WasteProcess
            Waste process object.
        """
        waste_process = cls()

        waste_process.set_parent(parent)
        waste_process.set_life_cycle_stage(life_cycle_stage)
        waste_process.set_process_name(process_name)
        if (process_name == "Landfill"): 
            waste_process.set_gas_capture_system(kwargs.get('gas_capture_system', "Flaring"))

        parent.get_waste_processes().append(waste_process)

        if linked_process is not None:
            for process in linked_process:
                linked_waste_process = WasteProcess.new(parent, process_name, qty, unit, process)

                waste_process.set_linked_process(linked_waste_process)
                parent.waste_processes.append(linked_waste_process)

        return waste_process

    # ================================
    # Setters
    # ================================
    def set_parent(self, parent):
        """Set parent Waste object of the Waste Processing.

        Parameters
        ----------
        parent : ~pod_lca.eol.Waste
            Waste object for which the waste processing belong.
        """
        self.parent = parent

        return self

    def set_process_name(self, name):
        """Set the process name.

        Parameters
        ----------
        name : {'Landfill', 'Recycle', 'Compost', 'Incinerate'}
                End-of-life pathway:

                - `'Landfill'`: transporting waste to a landfill.
                - `'Recycle'`: transporting waste to a recycler.
                - `'Compost'`: transporting to a composting facility.
                - `'Incinerate'`: transporting to an incinerator.
        """
        self.process_name = name

        return self

    def set_life_cycle_stage(self, life_cycle_stage):
        """Set life cycle stage of the product/process.

        Parameters
        ----------
        life_cycle_stage : {'C3', 'C4', 'D'}
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

    def set_location(self, location):
        """Set location of the waste process facility.

        Parameters
        ----------
        location : ~pod_lca.location.Location
            Location of the waster process facility.
        """
        self.location = location
        self.get_transportation_leg().set_shipping_destination(location)

        return self

    def set_linked_process(self, process):
        """Set a linked process to the current process.

        Parameters
        ----------
        process : ~pod_lca.eol.WasteProcess
            Secondary process following the current process.
        """
        self.linked_to = process
        process.linked_from = self

        return self
    
    def set_gas_capture_system(self, gas_capture_system):
        """Set the gas capture system for landfill process.

        Parameters
        ----------
        gas_capture_system : {'Energy Recovery', 'Flaring'}
            Type of landfill gas capture system.
        """
        self.gas_capture_system = gas_capture_system

        return self

    # ================================
    # Getters
    # ================================
    def get_parent(self):
        """Get parent Waste object of the Waste Processing.

        Returns
        -------
        ~pod_lca.eol.Waste
            Waste object for which the waste processing belong.
        """
        return self.parent

    def get_process_name(self):
        """Get the process name.

        Returns
        -------
        str
            Name of the process: e.g., 'Landfill', 'Recycle', 'Compost'
        """
        return self.process_name

    def get_name(self):
        """Get name of the process identifying the parent and process.

        Returns
        -------
        str
            Name identifyer.
        """
        return self.get_parent().get_name() + "_" + self.get_process_name()

    def get_qty(self):
        """Get quantity of the parent subjected to this waste process.

        Returns
        -------
        float
            Quantity of the parent object subjected to this process.
        """
        total_waste_quantity = self.get_parent().get_qty()
        percentage_in_process = self.get_parent().get_process_mix()[self.get_process_name()]

        return total_waste_quantity * percentage_in_process

    def get_unit(self):
        """Get unit of measurement for the waste amount processed.

        Returns
        -------
        ~pod_lca.units.Unit
            Unit of measurement.
        """
        return self.get_parent().get_unit()

    def get_weight(self):
        """Get weight of the parent subjected to this waste process.

        Returns
        -------
        float
            Quantity of the parent object subjected to this process.
        """
        total_waste_quantity = self.get_parent().get_weight()
        percentage_in_process = self.get_parent().get_process_mix()[self.get_process_name()]

        return total_waste_quantity * percentage_in_process

    def get_weight_unit(self):
        """Get unit of measurement for the weight of waste processed.

        Returns
        -------
        ~pod_lca.units.Unit
            Unit of measurement.
        """
        return self.get_parent().get_weight_unit()

    def get_life_cycle_stage(self):
        """Retrieve the life cycle stage corresponding to the waste process.

        Returns
        -------
        str
            Corresponding life cycle stage.
        """
        return self.life_cycle_stage

    def get_unit_impacts(self):
        """Get unit impacts of the waste process.

        Returns
        -------
        ~pod_lca.impacts.Impacts
            Unit impacts of the process.
        """
        self.update_unit_inventories()
        return self.unit_impacts

    def get_unit_emissions(self):
        """Get unit emissions of the waste process.

        Returns
        -------
        ~pod_lca.impacts.Emissions
            Unit emissions of the process.
        """
        self.update_unit_inventories()
        return self.unit_emissions

    def get_unit_stored_carbon_release(self):
        """Get unit emissions of the waste process due to the release of stored carbon.

        Returns
        -------
        ~pod_lca.impacts.Emissions
            Unit emissions of the process.
        """
        self.update_unit_inventories()
        return self.unit_stored_carbon_release
    
    def get_linked_process(self, to=True):
        """Get the linked process to the current process.

        Parameters
        ----------
        to : bool
            If True, return the process linked to, else linked from.

        Returns
        -------
        ~pod_lca.eol.WasteProcess
            Secondary process following the current process.
        """
        if to:
            return self.linked_to
        else:
            return self.linked_from
        
    def get_gas_capture_system(self):
        """Get the gas capture system for landfill process.

        Returns
        -------
        str
            Type of landfill gas capture system.
        """
        return self.gas_capture_system

    def get_transportation_leg(self):
        """Get the transportation leg corresponding to the end-of-life pathway.

        Returns
        -------
        ~pod_lca.transportation.TransportationLeg
            Secondary process following the current process.
        """
        return self.transporation_leg

    # ================================
    # Methods
    # ================================
    def update_unit_inventories(self):
        """Set unit impacts of the waste process."""
        material = self.get_parent().get_impact_database_entry()
        process = self.get_process_name()
        life_cycle_stage = self.get_life_cycle_stage()

        if process == "Landfill" and material == "Wood":
            impacts, emissions = self.get_landfill_wood_impacts_emissions()
        else:
            unit = self.get_unit()
            database = self.get_parent().get_eol_process_impact_database()

            database_entry = database.get_data_entry(material, process, life_cycle_stage)
            declared_unit = database_entry[database.get_unit_key()]
            conversion_factor = declared_unit.convert_to(unit)

            impacts = {key: database_entry[key] * conversion_factor for key in self.unit_impacts.record_attr_dict}
            emissions = {key: database_entry[key] * conversion_factor for key in self.unit_emissions.record_attr_dict}

        # biogenic carbon effects
        self.set_effects_release_of_stored_carbon()
        
        self.unit_impacts.update_qty(impacts)
        self.unit_emissions.update_qty(emissions)

    def get_landfill_wood_impacts_emissions(self):
        """Get unit impacts and emissions for wood materials in landfill.

        Returns
        -------
        dict
            Impacts dictionary.
        dict
            Emissions dictionary.
        """
        gas_capture_system = self.get_gas_capture_system()
        annual_precipitation = self.get_parent().get_parent().get_model().get_location().get_annual_precipitation(unit=INCH)

        match annual_precipitation:
            case val  if val < 20:
                annual_precipitation_range = "<20"
            case val if 20 <= val <= 40:
                annual_precipitation_range = "20-40"
            case val if val > 40:
                annual_precipitation_range = ">40"
            case _:
                raise ValueError("Annual precipitation not recognized.")
            
        wood_landfill_methane_data = DataImporter.csv_to_pandas(config["file_paths"]["eol"]["EOL_WOOD_LANDFILL_METHANE"])
        data = wood_landfill_methane_data[(wood_landfill_methane_data["Annual Precipitation (inches)"] == annual_precipitation_range) & 
                                          (wood_landfill_methane_data["Landfill Gas Capture System"] == gas_capture_system)]
        
        if len(data) == 1:
            declared_unit = UNITS_MAP[data["Unit"].values[0]]
            declared_qty = data["Qty"].values[0]
        
            unit = self.get_unit()
            conversion_factor = declared_unit.convert_to(unit) / declared_qty
    
            impacts = {key: data[key].values[0] * conversion_factor for key in self.unit_impacts.record_attr_dict if key in data}
            emissions = {key: data[key].values[0] * conversion_factor for key in self.unit_emissions.record_attr_dict if key in data}

            return impacts, emissions
    
    def set_effects_release_of_stored_carbon(self):
        """ Set the effects of releasing stored carbon during waste processing."""
        from ..dynamic_radiative_forcing import DynamicRadiativeForcing

        # emissions
        self.unit_stored_carbon_release = self.get_emissions_of_stored_biogenic_carbon()

        # GWP effects
        drf_calcualator = DynamicRadiativeForcing()
        self.unit_impacts.update_qty({"GWP": self.unit_impacts.get_record("GWP") + 
                                      self.unit_stored_carbon_release.get_record("CO2") * drf_calcualator.get_GWP("CO2", time_horizon=100) +
                                      self.unit_stored_carbon_release.get_record("CH4") * drf_calcualator.get_GWP("CH4", time_horizon=100)})
        
        return self

    def get_emissions_of_stored_biogenic_carbon(self):
        """Calculate biogenic carbon emissions from the waste process.

        Returns
        -------
        ~pod_lca.impacts.Emissions
            Emission from releasing stored carbon.
        """
        material = self.get_parent().get_impact_database_entry()
        process = self.get_process_name()
        life_cycle_stage = self.get_life_cycle_stage()
        unit = self.get_unit()
        database = self.get_parent().get_eol_process_impact_database()

        database_entry = database.get_data_entry(material, process, life_cycle_stage)
        declared_unit = database_entry[database.get_unit_key()]
        conversion_factor = declared_unit.convert_to(unit)

        emission_of_stored_carbon = Emissions.from_parent(self)

        bio_tag = CarbonStorage.get_bio_tag()
        bio_carbon_emissions = DataImporter.csv_to_pandas(config['file_paths']['eol']['EOL_STORED_CARBON_EMISSIONS'])
        data = bio_carbon_emissions[
            (bio_carbon_emissions['Material'] == material) &
            (bio_carbon_emissions['Process'] == process)
        ]
        if not data.empty:
            if self.get_parent().get_parent().get_unit().get_qty_measured() == "mass":
                waste_conversion_factor = self.get_parent().get_parent().get_unit().convert_to(unit)
            else:
                waste_conversion_factor = (1 / self.get_parent().get_parent().get_density()) * self.get_parent().get_parent().get_weight_unit().convert_to(unit)
                    
            bio_carbon_storage = self.get_parent().get_parent().unit_carbon_storage.get_record(bio_tag) * waste_conversion_factor
            
            molecular_weights = DataImporter.json_to_dict(config["file_paths"]["drf"]["MOLECULER_WEIGHT"])

            unit_CH4_emissions = bio_carbon_storage * (data['emitted as CH4 (%)'].values[0] / 100) * molecular_weights['CO2'] / molecular_weights['C']
            unit_C02_emissions = bio_carbon_storage * (data['emitted as CO2 (%)'].values[0] / 100) * molecular_weights['CH4'] / molecular_weights['C']

            emission_of_stored_carbon.update_qty({"CO2": unit_C02_emissions * conversion_factor,
                                                "CH4": unit_CH4_emissions * conversion_factor})
            
            # TODO: set temporal emission profile for biogenic emissions.

        return emission_of_stored_carbon



if __name__ == "__main__":
    pass
