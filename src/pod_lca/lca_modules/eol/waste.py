__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from math import isnan

from . import WasteProcess
from ..impacts import Impacts
from ..impacts import Emissions
from ..impacts import UniformEmissionProfile
from ..materials_screening import Product
from ..transportation import WasteTransportLeg
from ...utilities import config
from ...utilities import log


class Waste(Product):
    """Waste product handling the end-of-life or product.

    Attributes
    ----------
    parent : ~pod_lca.buildings.Assembly or ~pod_lca.materials_screening.Product
        The thing being was converted to waste.
    waste_processes : list of ~pod_lca.eol.WasteProcess
        List of processes the waste will be subjected to. These processes are in parallel.
    process_mix : dict
        The mix of processes the waste product will be subject to: {**process name** (:class:`str`): **percentage** (:class:`str` or :class:`float`)}.
        Percentage can be in the form of string with a % sign or decimal value.
    impacts : dict
        Impact objects categorized by life cycle stage {**life cycle stage** (:class:`str`): list of :class:`~pod_lca.impacts.Impacts`}
    emissions : dict
        Emission objects categorized by life cycle stage {**life cycle stage** (:class:`str`): list of :class:`~pod_lca.impacts.Emissions`}
    bio_based : bool
        True if the material is bio-based.
    """

    def __init__(self):
        super().__init__()
        self.parent = None
        self.waste_processes = None
        self.process_mix = None
        self.impacts = {"C1": Impacts.from_parent(self), "C2": [], "C3": [], "C4": [], "D": []}
        self.emissions = {"C1": Emissions.from_parent(self), "C2": [], "C3": [], "C4": [], "D": []}
        self.bio_based = True

        # cache
        self._inventory_records_uptodata = False

    def __str__(self):
        str = "=" * 50 + "\n" + f"Waste Product ({self.get_name()})\n" + "=" * 50 + "\n"
        str += f"Total qty: {self.get_qty()} {self.get_unit().get_standard_notation()}\n"
        str += "Process mix:\n"
        for process in self.get_waste_processes():
            if not process.get_linked_process(to=False):
                mix_percent = self.get_process_mix()[process.get_process_name()]
                if isinstance(mix_percent, (float, int)):
                    mix_percent = f"{mix_percent * 100:.2%f}%"
                str += f"\t {process.get_process_name()} : {process.get_qty()} {process.get_unit().get_standard_notation()} ({mix_percent})\n"

        return str

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, parent, database_item, qty, unit, process_mix, bio_based=None):
        """Create new waste product.

        Parameters
        ----------
        parent : ~pod_lca.buildings.Assembly or ~pod_lca.materials_screening.Product
            The thing that which was converted to waste.
        database_item : str
            Material name corresponding to the database entry which gives the unit impact of the product.
        qty : float
            Quantity of the product/process.
        unit : ~pod_lca.units.Unit
            Unit of measurement corresponding to the quantity of the product/process.
        process_mix : dict
            The mix of processes the waste product will be subject to: {**process name** (:class:`str`): **percentage** (:class:`str` or :class:`float`)}.
            Percentage can be in the form of string with a % sign or decimal value.
        bio_based : bool
            True if the material is bio-based.

        Returns
        -------
        ~pod_lca.eol.Waste
            Waste product.
        """
        waste_item = cls()

        waste_item.set_parent(parent)
        waste_item.set_name("Waste " + database_item)
        waste_item.set_bio_based(bio_based)
        waste_item.set_impact_database_entry(database_item)
        waste_item.set_qty(qty)
        waste_item.set_unit(unit)

        waste_item.set_process_mix(process_mix)
        waste_item.set_waste_processess()

        return waste_item

    # ================================
    # Setters
    # ================================
    def set_parent(self, parent):
        """Set parent of the waste product.

        Parameters
        ----------
        parent : ~pod_lca.buildings.Assembly or ~pod_lca.materials_screening.Product
            The thing that which was converted to waste.
        """
        self.parent = parent

        return self

    def set_impact_database_entry(self, database_item: str):
        """Sets the impacts database entry corresponding to the item.
        This method will also update the corresponding impact quanitities.

        Parameters
        ----------
        database_item : str
            The name of the database item which gives the item impacts.
        """
        database = self.get_eol_process_impact_database()
        if not database.check_database_entry(database_item):
            if self.get_bio_based():
                database_item = config["setup"]["eol"]["EOL_DEFAULT_KEY"] + "_BIOBASED"
            else:
                database_item = config["setup"]["eol"]["EOL_DEFAULT_KEY"] + "_OTHER"

        self.impact_database_entry = database_item
        self._inventory_records_uptodata = False

        return self

    def set_waste_processess(self):
        """Set waste processe for the waste product. Also sets the process mix.

        Notes
        -----
        The waste mix allocated to any process which is beyond its cutoff distance is reallocated to Landfill.

        Parameters
        ----------
        process_mix : dict
            The mix of processes the waste product will be subject to: {**process name** (:class:`str`): **percentage** (:class:`str` or :class:`float`)}.
            Percentage can be in the form of string with a % sign or decimal value.
        """
        waste_process_dict = config["setup"]["eol"]["WASTE_PROCESS_STAGES"]
        self.waste_processes = []

        transfer_to_landfill_quantity = 0.0
        for waste_process_name in waste_process_dict.keys() - ["Landfill"]:
            mix_percent = self.get_process_mix(waste_process_name)
            if mix_percent:
                process_qty = self.get_qty() * mix_percent
                result = self.set_waste_process(waste_process_name, process_qty)
                if isinstance(result, (float, int)):
                    transfer_to_landfill_quantity += result

        # set landfill process
        mix_percent = self.get_process_mix("Landfill")
        process_qty = self.get_qty() * mix_percent
        process_qty += transfer_to_landfill_quantity

        self.set_waste_process("Landfill", process_qty)

        return self

    def set_waste_process(self, process_name, process_qty):
        """Set waste process. If cutoff due to distance, returns the unprocessed waste quantity.

        Parameters
        ----------
        process_name : {'Landfill', 'Recycle', 'Compost', 'Incinerate'}
            End-of-life pathway: \n
            - `'Landfill'`: transporting waste to a landfill.
            - `'Recycle'`: transporting waste to a recycler.
            - `'Compost'`: transporting to a composting facility.
            - `'Incinerate'`: transporting to an incinerator.
        process_qty : float
            Quantity of waste subjected to this process

        Returns
        -------
        :class:`~pod_lca.eol.WasteProcess`
            If the process is not cutoff
        :class:`float`
            If the process is cutoff, the balance waste quantity to be processed
        """
        waste_process_dict = config["setup"]["eol"]["WASTE_PROCESS_STAGES"]

        lc_stage = waste_process_dict[process_name]
        linked_process = None
        if isinstance(lc_stage, list):
            lc_stage = waste_process_dict[process_name][0]
            linked_process = waste_process_dict[process_name][1:]

        waste_process_obj = WasteProcess.new(self, process_name, process_qty, self.get_unit(), lc_stage, linked_process)

        waste_process_obj.transporation_leg = WasteTransportLeg.from_object(
            material=waste_process_obj, manager=self.get_parent().get_eol_manager(), eol_pathway=process_name
        )

        return waste_process_obj

    def set_bio_based(self, is_bio_based):
        """Set the bio-based nature of the material.

        Parameters
        ----------
        is_bio_based : bool
            True, if the material is bio-based.
        """
        if is_bio_based is None:
            self.bio_based = False
        else:
            self.bio_based = is_bio_based

        return self

    def set_process_mix(self, process_mix):
        """Get the mix of process the waste product is subjected to.

        Parameters
        ----------
        dict
            The mix of processes the waste product will be subject to: {**process name** (:class:`str`): **percentage** (:class:`str` or :class:`float`)}.
            Percentage can be in the form of string with a % sign or decimal value.

        Raises
        ------
        TypeError
            Mix percentates are unrecognized.
        ValueError
            Mix percentages does not sum to 100%.
        """
        waste_process_dict = config["setup"]["eol"]["WASTE_PROCESS_STAGES"]
        process_mix_cleaned = {}
        if Waste.check_mix_sum(process_mix):
            for process_name in waste_process_dict.keys():
                if process_name in process_mix.keys():
                    mix_percent_input = process_mix[process_name]
                    if isinstance(mix_percent_input, (float, int)):
                        if isnan(mix_percent_input):
                            mix_percent = 0.0
                        else:
                            mix_percent = mix_percent_input
                    elif isinstance(mix_percent_input, str):
                        if mix_percent_input in ["NA", "N/A"]:
                            mix_percent = 0.0
                        if mix_percent_input[-1] == "%":
                            mix_percent = float(mix_percent_input[:-1]) / 100.0
                        else:
                            mix_percent = float(mix_percent_input)
                    else:
                        raise TypeError("mix percentages are of unrecognized type. Must be float, int, or string.")
                else:
                    mix_percent = 0.0

                process_mix_cleaned[process_name] = mix_percent

            self.process_mix = process_mix_cleaned
            self._inventory_records_uptodata = False

            return self

        else:
            raise ValueError("Waste mix does not sum to 100%.")

    def set_production_year(self, year):
        """Set the production year of the waste product.

        Parameters
        ----------
        year : int
            Year in which the waste is generated.
        """
        self.production_year = year

        for emission_lst in self.get_emissions().values():
            if isinstance(emission_lst, Emissions):
                emission_lst = [emission_lst]
            for emission in emission_lst:
                pulse = UniformEmissionProfile.unit_pulse(at=year)
                emission.set_temporal_emission_profile(pulse)

        return self

    # ================================
    # Getters
    # ================================
    def get_parent(self):
        """Get parent of the waste product.

        Returns
        -------
        ~pod_lca.buildings.Assembly or ~pod_lca.materials_screening.Product
            The thing that which was converted to waste.
        """
        return self.parent

    def get_waste_processes(self):
        """Get waste processe for the waste product.

        Returns
        -------
        list of ~pod_lca.eol.WasteProcess
            List of processes the waste will be subjected to. These processes are in parallel.
        """
        return self.waste_processes

    def get_process_mix(self, process_name=None, mode="assigned"):
        """Get the mix of process the waste product is subjected to.

        Parameters
        ----------
        process_name : {'Landfill', 'Recycle', 'Compost', 'Incinerate'}
            End-of-life pathway: \n
            - `'Landfill'`: transporting waste to a landfill.
            - `'Recycle'`: transporting waste to a recycler.
            - `'Compost'`: transporting to a composting facility.
            - `'Incinerate'`: transporting to an incinerator.
        mode : {'assigned', 'actual'}
            Mode of calculation used for process mix; \n
            - `'assigned'`: the prescribed process mix.
            - `'actual'`: realized process mix. The differences due to cut-off distances are considered.
            Default is 'assigned'

        Returns
        -------
        dict
            The mix of processes the waste product will be subject to: {**process name** (:class:`str`): **percentage** (:class:`str` or :class:`float`)}.
            Percentage can be in the form of string with a % sign or decimal value.

        Raises
        ------
        ValueError
            Calculation mode not recognized.
        """
        if mode == "assigned":
            if process_name is None:
                return self.process_mix
            else:
                return self.process_mix[process_name]
        elif mode == "actual":
            self.update_waste_process_mix()
            process_mix = {}
            for process in self.get_waste_processes():
                if process.get_linked_process(to=False) is None:
                    process_mix[process.get_life_cycle_stage()] = process.get_qty() / self.get_qty()

            self._last_process_mix = process_mix

            return process_mix
        else:
            raise ValueError("Calucation mode of process mix is not recognized.")

    def get_bio_based(self):
        """Get the bio-based nature of the material.

        Returns
        -------
        bool
            True, if the material is bio-based.
        """
        return self.bio_based

    def get_production_year(self):
        """Get the production year of the waste product.

        Returns
        -------
        int
            Year in which the waste is generated.
        """
        return self.production_year

    def get_eol_process_impact_database(self):
        """Get the end-of-life product database corresponding to the project.

        Returns
        -------
        ~pod_lca.impacts.EOLImpactsDatabase
            True, if the material is bio-based.
        """
        return self.get_parent().get_eol_process_impact_database()

    def get_demolition_impact_database(self):

        return self.get_parent().get_eol_demolition_database()

    def get_impacts(self, lc_stage=None):
        """Get the impacts of the waste product.

        Parameters
        ----------
        lc_stage : {'C1', 'C2', 'C3', 'C4', 'D'}
            Life cycle stage: \n
            - `'C1'`: Demolition.
            - `'C2'`: Transportation.
            - `'C3'`: Processing.
            - `'C4'`: Disposal.
            - `'D'`: Benefits from reuse, recovery, recycling.

        Returns
        -------
        dict or ~pod_lca.impacts.Impacts
            If lc_stage is None, returns a dictionary of impacts categorized by life cycle stage {**life cycle stage** (:class:`str`): list of :class:`~pod_lca.impacts.Impacts`}.
            If lc_stage is specified, returns the impacts corresponding to the life cycle stage as a :class:`~pod_lca.impacts.Impacts` object.
        """
        self.update_inventory_records()
        
        if lc_stage is None:
            return self.impacts.values()
        else:
            return self.impacts[lc_stage]
        
    # ================================
    # Methods
    # ================================
    def update_inventory_records(self):
        """Update the demolition (C1), transportation (C2), and processing (C3-C4) impacts of waste."""
        self.update_waste_process_mix()
        if self.get_waste_processes():
            if not self._inventory_records_uptodata:
                self._inventory_records_uptodata = True

                # C1 impacts
                demolition_impact_database = self.get_demolition_impact_database()
                database_entry = demolition_impact_database.get_data_entry(self.get_impact_database_entry())
                declared_unit = database_entry[demolition_impact_database.get_unit_key()]
                declared_qty = database_entry[demolition_impact_database.get_qty_key()]
                conversion_factor = declared_unit.convert_to(self.get_unit())

                impacts_data = {
                    key: database_entry[key] * conversion_factor * self.get_qty() / declared_qty
                    for key in self.impacts["C1"].record_attr_dict
                }
                emissions_data = {
                    key: database_entry[key] * conversion_factor * self.get_qty() / declared_qty
                    for key in self.emissions["C1"].record_attr_dict
                }

                self.impacts["C1"].update_qty(impacts_data)
                self.emissions["C1"].update_qty(emissions_data)

                impacts = self.impacts
                for key in impacts.keys():
                    if key != "C1":
                        impacts[key] = []

                emissions = self.emissions
                for key in emissions.keys():
                    if key != "C1":
                        emissions[key] = []

                for process in self.get_waste_processes():
                    # C3-C4 impacts
                    process_impact = process.get_unit_impacts() * process.get_qty()
                    process_emission = process.get_unit_emissions() * process.get_qty()
                    impacts[process.get_life_cycle_stage()].append(process_impact)
                    emissions[process.get_life_cycle_stage()].append(process_emission)

                    if process.get_transportation_leg() is not None:
                        # C2 impacts
                        impacts["C2"].append(process.get_transportation_leg().get_impacts())
                        emissions["C2"].append(process.get_transportation_leg().get_emissions())

                self.set_production_year(self.get_production_year())

        return self

    def update_waste_process_mix(self):
        """Update the waste process mix based on cutoof distances.

        Notes
        -----
        The waste mix allocated to any process which is beyond its cutoff distance is reallocated to Landfill.
        """
        process_mix = self.get_process_mix()

        transfer_to_landfill_percentage = 0.0
        landfill_process = None
        existing_processes = []
        # update existing processes
        for process in self.get_waste_processes():
            process_name = process.get_process_name()
            if (
                (process_name in process_mix.keys())
                and not (process_name == "Landfill")
                and (process.get_linked_process(to=False) is None)
            ):
                if process.get_transportation_leg().get_travel_dist() > process.transporation_leg.get_cutoff_distance():
                    transfer_to_landfill_percentage += process_mix[process_name]
                    process_mix[process_name] = 0.0
                    log(
                        f"Waste process {process.get_process_name()} quantity for {process.get_name()} is set to zero as the closes facility at a distance greater than the cutoff distance.",
                        "Info",
                    )
            elif process_name == "Landfill":
                landfill_process = process
            else:
                pass

            existing_processes.append(process_name)

        # add new processes
        for process_name in process_mix.keys() - existing_processes:
            process_qty = self.get_qty() * process_mix[process_name]
            if process_qty:
                result = self.set_waste_process(process_name, process_qty)
                if isinstance(result, (float, int)):
                    transfer_to_landfill_percentage += result

        # set landfill process
        if landfill_process is not None:
            process_mix["Landfill"] += transfer_to_landfill_percentage

        return self

    @staticmethod
    def check_mix_sum(process_mix, tol=0.00001):
        """check if the process mix adds up to 100%.

        Parameters
        ----------
        process_mix : dict
            The mix of processes the waste product will be subject to: {**process name** (:class:`str`): **percentage** (:class:`str` or :class:`float`)}.
            Percentage can be in the form of string with a % sign or decimal value.
        tol : float
            Tolerence checked against

        Returns
        -------
        bool
            True if the sum of the mix percentages adds upto a 100%, within tolerence.

        """
        sum = 0.0
        for key, value in process_mix.items():
            if isinstance(value, str):
                if value[-1] == "%":
                    value = float(value[:-1]) / 100
            elif isnan(value):
                value = 0.0
            sum += value

        if abs(sum - 1) < tol:
            return True
        else:
            return False


if __name__ == "__main__":
    pass
