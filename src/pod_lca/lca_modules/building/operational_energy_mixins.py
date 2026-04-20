
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

import os
import subprocess
import shutil
from collections import defaultdict
from pathlib import Path

from . import OperationalElectricityProduct
from ..impacts import Emissions
from ..impacts import Impacts
from ..operational.equipment import  EquipmentConnection
from ..operational.equipment import  EquipmentList
from ..operational.ideal_air_load import  IdealAirLoad
from ..operational.light import  DaylightingControls
from ..operational.light import  DaylightingReferencePoint
from ..operational.node_list import  NodeList
from ..operational.read_write import read_results_file
from ..operational.read_write import write_idf_from_building
from ...units import Quantity as Q
from ...units import UNITS_MAP
from ...units import WATT_HOUR
from ...utilities import config
from ...utilities import DataImporter

    
class OperationalMixins:
    """ Methods for calculation of B6-B7 impacts
    """

    def set_operational_electricity_product(self, unit=None):
        """ Set the operational electricity product of the building
        """
        self.operational_energy_product = OperationalElectricityProduct.create(self, unit)

    def get_operational_electricity_product(self):
        """ Set the operational electricity product of the building
        """
        return self.operational_energy_product

    def get_operational_electricity_usasge(self, method='EUI', summed_at='year', group_by_category=True, group_by_zone=False, unit=WATT_HOUR):
        """ Get the operational electricity demands of the building.

        Parameters
        ----------
        method : {'eplus', 'EUIs'} 
            How operation electricity to be computed.
        summed_at : {'year', 'month'}
            Freequency at whcih the energy plus results are summed.
        group_by_category : bool
            If true, grouped by category, 'heating', 'lighting', and 'cooling'.
        group_by_zone : bool
            If true, grouped by zone.
        unit : ~pod_lca.units.Unit
            Unit of measurement of the electricity usage.

        Returns
        -------
        ~pod_lca.impacts.Impacts
            B6 impacts of the building.
        """
        electricity_usage = defaultdict(lambda: defaultdict(float))

        if method == 'EUIs': 
            electricity_usage_quantity = 0
            for envelope in self.building_envelope.get_envelopes():
                building_type = envelope.floor_plan_obj.get_usage()
                eui_data = DataImporter.csv_to_dict(config['file_paths']['building']['EUI'], 'building_type')[building_type]
   
                floor_area = envelope.floor_plan_obj.get_area()
                eui = Q(float(eui_data['eui']), UNITS_MAP[eui_data['unit']])
                
                electricity_usage_quantity = floor_area * eui

            if summed_at == 'year':
                electricity_usage['year']['total'] = electricity_usage_quantity.value
            elif summed_at == 'month':
                for month in range(12):  
                    electricity_usage[str(month + 1).zfill(2)]['total'] = electricity_usage_quantity.value / 12
            else:
                raise ValueError('Summed at time not recognized.')

        elif method == 'eplus':

            for tk, item in self.energy_plus_results.items():
                
                if summed_at == 'year':
                    time = 'year' 
                elif summed_at == 'month':
                    time = tk[-2:]
                else:
                    raise ValueError('Summed at time not recognized.')
                
                for zone, values in item.items():
                    for category in ['heating', 'lighting', 'cooling']:
                        conversion_factor = UNITS_MAP[self.energy_plus_units[zone][category]].convert_to(unit)

                        if group_by_category and group_by_zone:
                            name = zone + '-' + category
                        elif group_by_category:
                            name = category
                        elif group_by_zone:
                            name = zone
                        else:
                            name = None

                        if name is None:  
                            electricity_usage[time]['total'] += values[category] * conversion_factor
                        else:
                            electricity_usage[time][name] += values[category] * conversion_factor

        return electricity_usage

    def write_idf(self):
        """ Write idf file.
        """

        self.building_envelope.make_envelope_connectivity_network()
        self.building_envelope.set_outside_boundary_conditions()

        self.make_constructions_dict()
        self.make_layers_dict()
        self.building_envelope.set_cycle_directions()
        self.set_zone_systems()
        write_idf_from_building(self)

    def set_weather_file_path(self, file_path):
        self.weather_file_path = file_path

    def get_weather_file_path(self):
        if self.weather_file_path is None:
            climate_zone = self.get_location().get_climate_zone()
            return config["file_paths"]["weather_files"][climate_zone]
        else:
            return self.weather_file_path

    def run_operational_energy_model(self, delete=True):
        """ Run operational energy model to get operational energy use and emissions.
        """
        idf = config['file_paths']['operational']['TEMP']
        exe = config['file_paths']['operational']['EPLUS']
        out = config['file_paths']['operational']['OUTPUT']

        weather = self.get_weather_file_path()

        Path(out).mkdir(exist_ok=True)

        if delete:
            self.delete_result_files(out)

        print(exe, '-w', weather,'--output-directory', out, idf)
        subprocess.call([exe, '-w', weather,'--output-directory', out, idf])

        self.energy_plus_results, self.energy_plus_units = read_results_file(self, os.path.join(out, 'eplusout.eso'))

        self.get_operational_electricity_product()._inventories_uptodate = False

        return self
    
    def make_constructions_dict(self):
        self.constructions = {}
        for ek in self.building_envelope.envelopes:
            env = self.building_envelope.envelopes[ek]

            for sk in env.surfaces:
                con = env.surfaces[sk].construction
                self.constructions[con.name] = con

        windows = self.building_envelope.envelopes[ek].windows
        for wk in windows:
            con = windows[wk]
            self.constructions[con.name] = con

    def make_layers_dict(self):
        """ Makes a dictionary containing all unique layers, with names, materials and
        thicknesses.
        

        Returns
        -------
        None
        
        """
        self.layers = {}
        for ck in self.constructions:
            lkeys = self.constructions[ck].layers.keys()
            for lk in lkeys:
                layer = self.constructions[ck].layers[lk]
                name = self.constructions[ck].layers[lk].name
                thick = self.constructions[ck].layers[lk].thickness
                lname = '{} {}mm'.format(name, round(thick*1000, 1))
                self.layers[lname] = {'layer': layer}
                layer.name = lname

    def set_zone_systems(self):

        from copy import deepcopy

        eqc_key = list(self.operational_object.equipment_connections.keys())[0]
        eql_key = list(self.operational_object.equipment_lists.keys())[0]
        inl_key = list(self.operational_object.node_lists.keys())[0]
        enl_key = list(self.operational_object.node_lists.keys())[1]
        ial_key = list(self.operational_object.ideal_air_loads.keys())[0]
        dlc_key = list(self.operational_object.daylighting_controls.keys())[0]
        dlr_key = list(self.operational_object.daylighting_reference_points.keys())[0]

        eqc = self.operational_object.equipment_connections[eqc_key]
        eql = self.operational_object.equipment_lists[eql_key]
        inl = self.operational_object.node_lists[inl_key]
        enl = self.operational_object.node_lists[enl_key]
        ial = self.operational_object.ideal_air_loads[ial_key]
        dlc = self.operational_object.daylighting_controls[dlc_key]
        # dlr = self.daylighting_reference_points[dlr_key]

        for ek in self.building_envelope.envelopes:
            envelope = self.building_envelope.envelopes[ek]
            zname = envelope.name

            self.operational_object.node_lists[ek] = NodeList.from_data(deepcopy(inl.data))
            inlname = '{}_{}'.format(self.operational_object.node_lists[ek].name, zname)
            self.operational_object.node_lists[ek].name = inlname
            self.operational_object.node_lists[ek].nodes['0'] = 'inlet_node_{}'.format(zname)

            self.operational_object.node_lists[zname] = NodeList.from_data(deepcopy(enl.data))
            enlname = '{}_{}'.format(self.operational_object.node_lists[zname].name, zname)
            self.operational_object.node_lists[zname].name = enlname
            self.operational_object.node_lists[zname].nodes['0'] = 'exhaust_node_{}'.format(zname)

            self.operational_object.ideal_air_loads[ek] = IdealAirLoad.from_data(deepcopy(ial.data))
            ialname = '{} {}'.format(zname, self.operational_object.ideal_air_loads[ek].name)
            self.operational_object.ideal_air_loads[ek].name = ialname
            self.operational_object.ideal_air_loads[ek].zone_supply_air_node_name = inlname
            self.operational_object.ideal_air_loads[ek].zone_exhaust_air_node_name = enlname

            self.operational_object.equipment_lists[ek] = EquipmentList.from_data(eql.data)
            elname =  '{}_{}'.format(self.operational_object.equipment_lists[ek].name, zname)
            self.operational_object.equipment_lists[ek].name = elname
            self.operational_object.equipment_lists[ek].zone_equipment_name1 = ialname

            self.operational_object.equipment_connections[ek] = EquipmentConnection.from_data(eqc.data)
            self.operational_object.equipment_connections[ek].name = zname
            self.operational_object.equipment_connections[ek].zone_conditioning_equipment_list = elname
            self.operational_object.equipment_connections[ek].zone_air_inlet_node = inlname
            self.operational_object.equipment_connections[ek].zone_air_exhaust_node = enlname
            self.operational_object.equipment_connections[ek].zone_air_node += '_{}'.format(zname)

            self.operational_object.daylighting_controls[ek] = DaylightingControls.from_data(deepcopy(dlc.data))
            dc_name = 'daylighting_controls_{}'.format(zname)
            dc_ref_pt_name = 'daylighting_ref_pt_{}'.format(zname)
            x, y, z = envelope.centroid
            self.operational_object.daylighting_controls[ek].name = dc_name
            self.operational_object.daylighting_controls[ek].zone_name = zname
            self.operational_object.daylighting_controls[ek].glare_reference_point = dc_ref_pt_name
            rp_key = list(self.operational_object.daylighting_controls[ek].reference_points.keys())[0]
            self.operational_object.daylighting_controls[ek].reference_points = {0: self.operational_object.daylighting_controls[ek].reference_points[rp_key]}
            self.operational_object.daylighting_controls[ek].reference_points[0]['ref_pt_name'] = dc_ref_pt_name
            dl_rpt = DaylightingReferencePoint.from_data({'name': dc_ref_pt_name,
                                                                 'zone_name': zname,
                                                                 'x': x,
                                                                 'y': y,
                                                                 'z': z + self.operational_object.daylighting_controls_height,
                                                                 })
            self.operational_object.daylighting_reference_points[dc_ref_pt_name] = dl_rpt


        del self.operational_object.equipment_connections[eqc_key]
        del self.operational_object.equipment_lists[eql_key]
        del self.operational_object.node_lists[inl_key]
        del self.operational_object.node_lists[enl_key]
        del self.operational_object.ideal_air_loads[ial_key]
        del self.operational_object.daylighting_controls[dlc_key]
        del self.operational_object.daylighting_reference_points[dlr_key]

    def delete_result_files(self, out_path):
        """ Deletes energy+ result files.

        Parameters:
            out_path (str): Path to the energy+ output folder.

        Returns:
            None
        """
        shutil.rmtree(out_path)

    # ================================
    # Inventory Records Methods
    # ================================ 
    def get_operational_impacts(self, category='total', objs=False):
        """ Get B6 impacts of the building.

        Parameters
        ----------
        category : {'heating', 'lighting', 'cooling', 'total'}
            Category of operational energy.
        objs : bool, optional
            If True, return a list of emissions objects for each material. 
            If False, return a single emissions object for the entire building. Default is False.

        Returns
        -------
        ~pod_lca.impacts.Impacts
            B6 impacts of the building.
        """
        if not self.get_operational_electricity_product()._inventories_uptodate:
            self.get_operational_electricity_product().update_inventory_records()

        if (self.operational_energy_method == 'eplus' and self.get_operational_energy_object().is_dirty):
            self.get_operational_electricity_product().update_inventory_records()

        if objs:
            return self.get_operational_electricity_product().get_impacts(category)
        else:
            impacts = Impacts.from_parent(self)
            for impact in self.get_operational_electricity_product().get_impacts(category):
                impacts += impact

            return impacts

    def get_operational_emissions(self, category='total', objs=False):
        """ Get B6 emissions of the building.

        Parameters
        ----------
        category : {'heating', 'lighting', 'cooling', 'total'}
            Category of operational energy.
        objs : bool, optional
            If True, return a list of emissions objects for each material. 
            If False, return a single emissions object for the entire building. Default is False.

        Returns
        -------
        ~pod_lca.impacts.Emissions
            B6 emissions of the building.
        """
        if not self.get_operational_electricity_product()._inventories_uptodate:
            self.get_operational_electricity_product().update_inventory_records()

        if (self.operational_energy_method == 'eplus' and self.get_operational_energy_object().is_dirty):
            self.get_operational_electricity_product().update_inventory_records()

        if objs:
            return self.get_operational_electricity_product().get_emissions(category)
        else:
            emissions = Emissions.from_parent(self)
            for emission in self.get_operational_electricity_product().get_emissions(category):
                emissions += emission

            return emissions


if __name__ == '__main__':
    pass
