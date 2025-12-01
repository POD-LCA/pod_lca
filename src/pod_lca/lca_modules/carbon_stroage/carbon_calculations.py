__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ...units import CUBIC_METER
from ...units import KILOGRAM
from ...units import METER
from ...units import SQUARE_METER
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


def get_dry_mass(wet_mass, moisture_content):
    """Get the dry mass given wet mass and moisture content.

    Parameters
    ----------
    wet_mass : float
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
    wet_mass : float
        Wet mass of the product.
    wet_mass_unit : ~pod_lca.units.Unit
        Unit corresponding to the wet mass of the product.
    dry mass : float
        Dry mass of the product.
    dry dry_mass_unit : ~pod_lca.units.Unit
        Unit corresponding to the dry mass of the product.
    dry_density : float
        Dry density of the product.
    dry_desnity_unit : ~pod_lca.units.Unit
        Unit corresponding to the dry density of the product.
    carbon_percentage_dry : float
        Carbon percentage on dry basis (0.00 - 1.00).
    moisture_content : float
        Moisture content of the wet product.
    volume : float
        Volume of the product.
    volume_unit : ~pod_lca.units.Unit
        Unit corresponding to the volume of the product.
    area : float
        Area of the product.
    area_unit : ~pod_lca.units.Unit
        Unit corresponding to the area of the prouct.
    thickness : float
        Thickness of the product.
    thickness_unit : ~pod_lca.units.Unit
        Unit corresponding to the thickness of the product.

    Returns
    -------
    :class:`float`
        Biogenic carbon content of the product.
    :class:`~pod_lca.units.Unit`
        Corresponding unit of the biogenic carbon content.
    """
    carbon_percentage_dry = kwargs.get("carbon_percentage_dry", 0.0)

    dry_mass = kwargs.get("dry_mass", None)
    dry_mass_unit = kwargs.get("dry_mass_unit", KILOGRAM)
    wet_mass = kwargs.get("wet_mass", None)
    wet_mass_unit = kwargs.get("wet_mass_unit", KILOGRAM)
    moisture_content = kwargs.get("moisture_content", None)
    if (dry_mass is None) and (wet_mass is not None) and (moisture_content is not None):
        dry_mass = get_dry_mass(wet_mass, moisture_content)
        dry_mass_unit = wet_mass_unit

    if dry_mass is not None:
        return dry_mass * carbon_percentage_dry, dry_mass_unit

    volume = kwargs.get("volume", None)
    volume_unit = kwargs.get("volume_unit", CUBIC_METER)
    dry_density = kwargs.get("dry_density", None)
    dry_density_unit = kwargs.get("dry_desnity_unit", KILOGRAM / CUBIC_METER)

    if (volume is not None) and (dry_density is not None):
        return volume * dry_density * carbon_percentage_dry, volume_unit * dry_density_unit

    area = kwargs.get("area", None)
    area_unit = kwargs.get("area_unit", SQUARE_METER)
    thickness = kwargs.get("thickness", None)
    thickness_unit = kwargs.get("thickness_unit", METER)

    if (area is not None) and (thickness is not None) and (dry_density is not None):
        return area * thickness * dry_density * carbon_percentage_dry, area_unit * thickness_unit * dry_density_unit

    log("Data insuficient to determine carbon content.", "Warn")

    return 0, KILOGRAM


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
