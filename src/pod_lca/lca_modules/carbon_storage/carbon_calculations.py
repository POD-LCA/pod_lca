__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ...units import KILOGRAM
from ...units import Quantity as Q
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


def get_dry_mass(wet_mass, moisture_content):
    """Get the dry mass given wet mass and moisture content.

    Parameters
    ----------
    wet_mass : ~pod_lca.units.Quantity
        Wet mass.
    moisture_content : float
        Moisture content at wet condition.

    Returns
    -------
    float
        Mass at 0.00 moisture content.
    """
    return wet_mass / (1 + moisture_content)


def get_biogenic_carbon_content(**kwargs):
    """Determine biogenic carbon content.

    Other Parameters
    ----------------
    carbon_composition : float
        Carbon content as a percentage of dry mass.
    wet_mass : ~pod_lca.units.Quantity
        Wet mass of the product.
    dry mass : ~pod_lca.units.Quantity
        Dry mass of the product.
    dry_density : ~pod_lca.units.Quantity
        Dry density of the product.
    moisture_content : float
        Moisture content of the wet product.
    volume : ~pod_lca.units.Quantity
        Volume of the product.
    area : ~pod_lca.units.Quantity
        Area of the product.
    thickness : ~pod_lca.units.Quantity
        Thickness of the product.

    Returns
    -------
    ~pod_lca.units.Quantity
        Biogenic carbon content of the product.
    """
    carbon_percentage_dry = kwargs.get("carbon_composition", 0.0)

    dry_mass = kwargs.get("dry_mass", None)
    wet_mass = kwargs.get("wet_mass", None)
    moisture_content = kwargs.get("moisture_content", None)
    if (dry_mass is None) and (wet_mass is not None) and (moisture_content is not None):
        dry_mass = get_dry_mass(wet_mass, moisture_content)

    if dry_mass is not None:
        return dry_mass * carbon_percentage_dry

    volume = kwargs.get("volume", None)
    dry_density = kwargs.get("dry_density", None)

    if (volume is not None) and (dry_density is not None):
        return volume * dry_density * carbon_percentage_dry

    area = kwargs.get("area", None)
    thickness = kwargs.get("thickness", None)

    if (area is not None) and (thickness is not None) and (dry_density is not None):
        return area * thickness * dry_density * carbon_percentage_dry

    log("Data insuficient to determine carbon content.", "Warn")

    return Q(0, KILOGRAM)

def get_biogenic_carbon_dioxide_content(biogenic_carbon_content):
    """Get the biigenic carbon dioxide content from the biogenic carbon content.

    Parameters
    ----------
    biogenic_carbon_content : float
        Biogenic carbon content.

    Returns
    -------
    float
        Biogenic CO2 content.
    """
    molecular_weight_dict = DataImporter.json_to_dict(config["file_paths"]["drf"]["MOLECULER_WEIGHT"])

    return biogenic_carbon_content * molecular_weight_dict["CO2"] / molecular_weight_dict["C"]


if __name__ == "__main__":
    pass
