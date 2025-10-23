
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

import os
import subprocess
import shutil
from collections import defaultdict

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
from ...units import FEET
from ...units import METER
from ...units import SQUARE_FEET
from ...units import SQUARE_METER
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
            eui_data = DataImporter.csv_to_dict(config['file_paths']['building']['EUI'], 'building_type')[self.get_building_type()]
            eui = float(eui_data['eui'])
            
            total_area = 0.0
            for floor_no in range(1, self.get_no_floors() + 1):
                total_area += self.get_floor(floor_no).get_area()

                if floor_no == self.get_no_floors():
                    floor_geom_unit = self.get_floor(floor_no).get_geometry_unit()
                    if  floor_geom_unit is METER:
                        area_unit = SQUARE_METER
                    elif floor_geom_unit is FEET:
                        area_unit = SQUARE_FEET
                    else:
                        raise TypeError("Building Geometry to be in meters or feet.")
                
            eui_unit = UNITS_MAP[eui_data['unit']]
            energy_unit = eui_unit * area_unit
            conversion_factor = energy_unit.convert_to(unit)

            if summed_at == 'year':
                electricity_usage['year']['total'] = eui * total_area * conversion_factor
            elif summed_at == 'month':
                for month in range(12):  
                    electricity_usage[str(month + 1).zfill(2)]['total'] = eui * total_area * conversion_factor / 12
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
        self.make_layers_dict()
        write_idf_from_building(self)

    def run_operational_energy_model(self, eplus_path, idf_path, weather, delete=True):
        """ Run operational energy model to get operational energy use and emissions.
        """
        idf = os.path.join(idf_path, 'pod_lca_operational.idf')
        exe = os.path.join(eplus_path, 'energyplus')
        out = os.path.join(idf_path, '{}_eplus_out'.format(self.name))

        if delete:
            self.delete_result_files(out)

        print(exe, '-w', weather,'--output-directory', out, idf)
        subprocess.call([exe, '-w', weather,'--output-directory', out, idf])

        self.energy_plus_results, self.energy_plus_units = read_results_file(self, os.path.join(out, 'eplusout.eso'))

        self.get_operational_electricity_product()._inventories_uptodate = False

        return self   
       
    def make_layers_dict(self):
        """ Makes a dictionary containing all unique layers, with names, materials and
        thicknesses.
        

        Returns
        -------
        None
        
        """
        for ck in self.constructions:
            lkeys = self.constructions[ck].layers.keys()
            for lk in lkeys:
                name = self.constructions[ck].layers[lk]['name']
                thick = self.constructions[ck].layers[lk]['thickness']
                lname = '{} {}mm'.format(name, round(thick*1000, 1))
                self.layers[lname] = {'layer_name': lname,
                                                 'material_name': name,
                                                 'thickness': thick}

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

        for zk in self.floors:
            envelope = self.floors[zk].envelope
            zname = envelope.name

            self.operational_object.node_lists[zk] = NodeList.from_data(deepcopy(inl.data))
            inlname = '{}_{}'.format(self.operational_object.node_lists[zk].name, zname)
            self.operational_object.node_lists[zk].name = inlname
            self.operational_object.node_lists[zk].nodes['0'] = 'inlet_node_{}'.format(zname)

            self.operational_object.node_lists[zname] = NodeList.from_data(deepcopy(enl.data))
            enlname = '{}_{}'.format(self.operational_object.node_lists[zname].name, zname)
            self.operational_object.node_lists[zname].name = enlname
            self.operational_object.node_lists[zname].nodes['0'] = 'exhaust_node_{}'.format(zname)

            self.operational_object.ideal_air_loads[zk] = IdealAirLoad.from_data(deepcopy(ial.data))
            ialname = '{} {}'.format(zname, self.operational_object.ideal_air_loads[zk].name)
            self.operational_object.ideal_air_loads[zk].name = ialname
            self.operational_object.ideal_air_loads[zk].zone_supply_air_node_name = inlname
            self.operational_object.ideal_air_loads[zk].zone_exhaust_air_node_name = enlname

            self.operational_object.equipment_lists[zk] = EquipmentList.from_data(eql.data)
            elname =  '{}_{}'.format(self.operational_object.equipment_lists[zk].name, zname)
            self.operational_object.equipment_lists[zk].name = elname
            self.operational_object.equipment_lists[zk].zone_equipment_name1 = ialname

            self.operational_object.equipment_connections[zk] = EquipmentConnection.from_data(eqc.data)
            self.operational_object.equipment_connections[zk].name = zname
            self.operational_object.equipment_connections[zk].zone_conditioning_equipment_list = elname
            self.operational_object.equipment_connections[zk].zone_air_inlet_node = inlname
            self.operational_object.equipment_connections[zk].zone_air_exhaust_node = enlname
            self.operational_object.equipment_connections[zk].zone_air_node += '_{}'.format(zname)

            self.operational_object.daylighting_controls[zk] = DaylightingControls.from_data(deepcopy(dlc.data))
            dc_name = 'daylighting_controls_{}'.format(zname)
            dc_ref_pt_name = 'daylighting_ref_pt_{}'.format(zname)
            x, y, z = envelope.centroid
            self.operational_object.daylighting_controls[zk].name = dc_name
            self.operational_object.daylighting_controls[zk].zone_name = zname
            self.operational_object.daylighting_controls[zk].glare_reference_point = dc_ref_pt_name
            rp_key = list(self.operational_object.daylighting_controls[zk].reference_points.keys())[0]
            self.operational_object.daylighting_controls[zk].reference_points = {0: self.operational_object.daylighting_controls[zk].reference_points[rp_key]}
            self.operational_object.daylighting_controls[zk].reference_points[0]['ref_pt_name'] = dc_ref_pt_name
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

        if objs:
            return self.get_operational_electricity_product().get_emissions(category)
        else:
            emissions = Emissions.from_parent(self)
            for emission in self.get_operational_electricity_product().get_emissions(category):
                emissions += emission

            return emissions


if __name__ == '__main__':
    pass
