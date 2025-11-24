__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


from pod_lca.lca_modules.operational.light import Light
from pod_lca.lca_modules.operational.light import DaylightingControls
from pod_lca.lca_modules.operational.light import DaylightingReferencePoint
from pod_lca.lca_modules.operational.people import People
from pod_lca.lca_modules.operational.electric_eq import ElectricEquipment
from pod_lca.lca_modules.operational.zone_control_thermostat import ZoneControlThermostat
from pod_lca.lca_modules.operational.setpoint import DualSetpoint
from pod_lca.lca_modules.operational.ideal_air_load import IdealAirLoad
from pod_lca.lca_modules.operational.infiltration import Infiltration
from pod_lca.lca_modules.operational.equipment import EquipmentList
from pod_lca.lca_modules.operational.equipment import EquipmentConnection
from pod_lca.lca_modules.operational.zone_list import ZoneList
from pod_lca.lca_modules.operational.node_list import NodeList
from pod_lca.lca_modules.operational.outdoor_air import OutdoorAir
from pod_lca.lca_modules.operational.schedule import Schedule

from pod_lca.lca_modules.operational.read_write.read_idf import find_schedule_compact
from pod_lca.lca_modules.operational.read_write.read_idf import find_daylight_controls
from pod_lca.lca_modules.operational.read_write.read_idf import find_daylight_reference_points
from pod_lca.lca_modules.operational.read_write.read_idf import find_lights
from pod_lca.lca_modules.operational.read_write.read_idf import find_people
from pod_lca.lca_modules.operational.read_write.read_idf import find_electric_equipment
from pod_lca.lca_modules.operational.read_write.read_idf import find_zone_control_thermostat
from pod_lca.lca_modules.operational.read_write.read_idf import find_thermostat_setpoint
from pod_lca.lca_modules.operational.read_write.read_idf import find_ideal_air_loads
from pod_lca.lca_modules.operational.read_write.read_idf import find_infiltration
from pod_lca.lca_modules.operational.read_write.read_idf import find_equipment_list
from pod_lca.lca_modules.operational.read_write.read_idf import find_equipment_connections
from pod_lca.lca_modules.operational.read_write.read_idf import find_zone_lists
from pod_lca.lca_modules.operational.read_write.read_idf import find_node_lists
from pod_lca.lca_modules.operational.read_write.read_idf import find_outdoor_air
from pod_lca.lca_modules.operational.read_write.read_idf import find_schedule_type_limits
from pod_lca.lca_modules.operational.read_write.read_idf import find_schedule_day_interval
from pod_lca.lca_modules.operational.read_write.read_idf import find_schedule_week_daily
from pod_lca.lca_modules.operational.read_write.read_idf import find_schedule_year


class OperationalObject(object):
    def __init__(self):
        self.name = None
        self.daylighting_controls = None
        self.daylighting_reference_points = None
        self.lights = None
        self.peoples = None
        self.electric_equipment = None
        self.zone_control_thermostats = None
        self.setpoints = None
        self.ideal_air_loads = None
        self.infiltrations = None
        self.equipment_lists = None
        self.equipment_connections = None
        self.zone_lists = None
        self.node_lists = None
        self.outdoor_airs = None
        self.schedules = None
        self.daylighting_controls_height = 0.8

    @classmethod
    def from_idf(cls, path):
        data = {}
        find_daylight_controls(path, data)
        find_daylight_reference_points(path, data)
        find_lights(path, data)
        find_people(path, data)
        find_electric_equipment(path, data)
        find_zone_control_thermostat(path, data)
        find_thermostat_setpoint(path, data)
        find_ideal_air_loads(path, data)
        find_infiltration(path, data)
        find_equipment_list(path, data)
        find_equipment_connections(path, data)
        find_zone_lists(path, data)
        find_node_lists(path, data)
        find_outdoor_air(path, data)

        find_schedule_compact(path, data)
        find_schedule_type_limits(path, data)
        find_schedule_day_interval(path, data)
        find_schedule_week_daily(path, data)
        find_schedule_year(path, data)

        # find_spaces(path, data)
        # find_space_lists(path, data)

        operational_object = cls.from_data(data)
        return operational_object

    @classmethod
    def from_data(cls, data):
        oo = cls()

        oo.daylighting_controls = {
            lk: DaylightingControls.from_data(data["daylighting_controls"][lk]) for lk in data["daylighting_controls"]
        }
        oo.daylighting_reference_points = {
            lk: DaylightingReferencePoint.from_data(data["daylighting:referencepoint"][lk])
            for lk in data["daylighting:referencepoint"]
        }
        oo.lights = {lk: Light.from_data(data["lights"][lk]) for lk in data["lights"]}
        oo.peoples = {pk: People.from_data(data["people"][pk]) for pk in data["people"]}
        oo.electric_equipment = {
            ek: ElectricEquipment.from_data(data["electric_equipment"][ek]) for ek in data["electric_equipment"]
        }
        oo.zone_control_thermostats = {
            zk: ZoneControlThermostat.from_data(data["zone_control_thermostat"][zk])
            for zk in data["zone_control_thermostat"]
        }
        oo.setpoints = {sk: DualSetpoint.from_data(data["setpoint"][sk]) for sk in data["setpoint"]}
        oo.ideal_air_loads = {ik: IdealAirLoad.from_data(data["ideal_air_load"][ik]) for ik in data["ideal_air_load"]}
        oo.infiltrations = {ik: Infiltration.from_data(data["infiltration"][ik]) for ik in data["infiltration"]}
        oo.equipment_lists = {ek: EquipmentList.from_data(data["equipment_list"][ek]) for ek in data["equipment_list"]}
        oo.equipment_connections = {
            ek: EquipmentConnection.from_data(data["equipment_connection"][ek]) for ek in data["equipment_connection"]
        }
        oo.zone_lists = {zk: ZoneList.from_data(data["zone_lists"][zk]) for zk in data["zone_lists"]}
        oo.node_lists = {nk: NodeList.from_data(data["node_lists"][nk]) for nk in data["node_lists"]}
        oo.outdoor_airs = {ok: OutdoorAir.from_data(data["outdoor_air"][ok]) for ok in data["outdoor_air"]}
        oo.schedules = {sk: Schedule.from_data(data["schedules"][sk]) for sk in data["schedules"]}
        return oo
