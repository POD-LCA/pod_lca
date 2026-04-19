__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from ..building_envelope import Envelope
from ..building_envelope import Wall
from ..building_envelope import Floor
from ..building_envelope import Ceiling
from ..building_envelope import Window
from ..geometry import window_surfaces_from_wwr
from ..operational import find_constructions
from ..operational import find_materials
from ..operational import find_materials_air_gap
from ..operational import find_no_mass_materials
from ..operational import find_gas_materials
from ..operational import find_glazing_materials
from ..operational import OperationalEnergyObject
from ...utilities import config


class EnvelopeMixins():
    def read_constructions_data(self, path=None):
        if path is None:
            path = config['file_paths']['operational']['CONSTRUCTIONS']
        
        find_constructions(path, self.idf_constructions_data)

    def read_material_properties_data(self, path=None):
        if path is None:
            path = config['file_paths']['operational']['SYSTEMS']
        find_materials(path, self.idf_material_properties)
        find_materials_air_gap(path, self.idf_material_properties)
        find_no_mass_materials(path, self.idf_material_properties)
        find_gas_materials(path, self.idf_material_properties)
        find_glazing_materials(path, self.idf_material_properties)

    def create_envelopes_from_template(self, operational_sys_path=None):


        wall_service_life = 30
        structure_service_life = 60
        window_service_life = 40

        for fk in self.floors:
            floor = self.floors[fk]
            e = Envelope.from_floor(floor)
            floor.set_envelope(e)

            # add walls - - - - - - - - - - - - - - - - - - - - - - - - - - -

            walls = 'Rainscreen-Thinbrick'
            surfaces = [e.surfaces[sk] for sk in e.wall_surface_keys]
            walls = Wall.from_idf(walls, self, surfaces, wall_service_life)
            e.add_construction(walls)

            # add floor slabs - - - - - - - - - - - - - - - - - - - - - - - - - - -

            if floor.is_on_ground:
                gslab = 'Generic Ground Slab'
                surfaces = [e.surfaces['floor']]
                gslab = Floor.from_idf(gslab, self, surfaces, structure_service_life)
                e.add_construction(gslab)
            else:
                slab = 'Insulated 8in Slab Floor'
                surfaces = [e.surfaces['floor']]
                slab = Floor.from_idf(slab, self, surfaces, structure_service_life)
                e.add_construction(slab)


            # add ceiling slabs - - - - - - - - - - - - - - - - - - - - - - - - - - -

            if floor.is_last:
                roof = 'Generic Roof'
                surfaces = [e.surfaces['ceiling']]
                roof = Ceiling.from_idf(roof, self, surfaces, structure_service_life)
                e.add_construction(roof)
            else:
                ciel = 'Generic Interior Ceiling'
                surfaces = [e.surfaces['ceiling']]
                ciel = Ceiling.from_idf(ciel, self, surfaces, structure_service_life)
                e.add_construction(ciel)

        self.update_envelope_surfaces()

        # add windows - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        for fk in self.floors:
            if not self.floors[fk].is_below_grade:
                env = self.floors[fk].envelope
                for wall_key in env.wall_surface_keys:
                    wwr = .4
                    window = 'Generic Double Pane'
                    surfaces = window_surfaces_from_wwr(env, wall_key, wwr)
                    window = Window.from_idf(window, self, surfaces, window_service_life)
                    env.add_window(window, wall_key)


        self.operational_object = OperationalEnergyObject.from_idf(operational_sys_path)
        self.set_zone_systems()