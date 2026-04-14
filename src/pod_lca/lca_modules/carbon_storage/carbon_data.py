
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log

def _get_carbon_data(data, species=None, region=None, material_form=None):
    """ Get the carbon percentage.
    
    Parameters
    ----------
    data : {'carbon percentage', 'moisture content', 'dry density', 'dry density unit'}
        Type of data to be retrieved.
    species : str
        Species identifier. Search is case insensitive.
    region : {'AU', 'CA', 'CD', 'CN', 'GLO', 'IN', 'RER','RNA', 'US','US-MT'}
        Region of origin of the product.
        -   'AU': Australia
        -   'CA': Canada
        -   'CD': Congo, the Democratic Republic of the
        -   'CN': China
        -   'GLO': Global
        -   'IN': India
        -   'RER': Europe
        -   'RNA': North America
        -   'US': United States
        -   'US-MT': United States, Montana
    material_form : str
        Final form of the product. Search is case insensitive.
    """
    biomaterial_data = DataImporter.csv_to_pandas(config['file_paths']['carbon']['BIO_MATERIAL_DATA'])

    match data:
        case "carbon percentage":
            header = "%C (dry basis)"
        case "moisture content":
            header = "Moisture % (Green)"
        case "dry density":
            header = "Dry Density (0% moisture)"
        case "dry density unit":
            header = 'Dry density unit'

    if species is None:
        species = 'Unspecified'
    if region is None:
        region = 'Unspecified'
    if material_form is None:
        material_form = 'Unspecified'

    data_entry = biomaterial_data[(biomaterial_data['Species'].str.lower()==species.lower())
                                  & (biomaterial_data['Region'].str.lower()==region.lower())
                                  & (biomaterial_data['Material Form'].str.lower()==material_form.lower())]
    
    if data_entry.empty:
        if (region == 'Unspecified') and (material_form == 'Unspecified'):
            data_entry = biomaterial_data[(biomaterial_data['Species'].str.lower()==species.lower())]
        elif (material_form == 'Unspecified'):
            data_entry = biomaterial_data[(biomaterial_data['Species'].str.lower()==species.lower())
                                          & (biomaterial_data['Region'].str.lower()==region.lower())]
            
    if data_entry.empty:
        log("No matching data found.", "Warn")
    elif len(data_entry) > 1:
        log("Multiple matching data found. Mean valuer returned", "Warn")
        return data_entry[header].mean()
    else:
        return data_entry[header].iloc[0]
    
def get_carbon_percentage(species=None, region=None, material_form=None):
    """ Get the carbon percentage.
    
    Parameters
    ----------
    species : str
        Species identifier. Search is case insensitive.
    region : {'AU', 'CA', 'CD', 'CN', 'GLO', 'IN', 'RER','RNA', 'US','US-MT'}
        Region of origin of the product.
        -   'AU': Australia
        -   'CA': Canada
        -   'CD': Congo, the Democratic Republic of the
        -   'CN': China
        -   'GLO': Global
        -   'IN': India
        -   'RER': Europe
        -   'RNA': North America
        -   'US': United States
        -   'US-MT': United States, Montana
    material_form : str
        Final form of the product. Search is case insensitive.
    """
    return _get_carbon_data('carbon percentage', species, region, material_form)

def get_moisture_content(species, region, material_form):
    """ Get moisture content at green condition.

    Parameters
    ----------
    species : str
        Species identifier.
    region : {'AU', 'CA', 'CD', 'CN', 'GLO', 'IN', 'RER','RNA', 'US','US-MT'}
        Region of origin of the product.
        -   'AU': Australia
        -   'CA': Canada
        -   'CD': Congo, the Democratic Republic of the
        -   'CN': China
        -   'GLO': Global
        -   'IN': India
        -   'RER': Europe
        -   'RNA': North America
        -   'US': United States
        -   'US-MT': United States, Montana
    material_form : str
        Final form of the product.
    """
    return _get_carbon_data('moisture content', species, region, material_form)

def get_dry_density(species, region, material_form):
    """ Get moisture content at green condition.

    Parameters
    ----------
    species : str
        Species identifier.
    region : {'AU', 'CA', 'CD', 'CN', 'GLO', 'IN', 'RER','RNA', 'US','US-MT'}
        Region of origin of the product.
        -   'AU': Australia
        -   'CA': Canada
        -   'CD': Congo, the Democratic Republic of the
        -   'CN': China
        -   'GLO': Global
        -   'IN': India
        -   'RER': Europe
        -   'RNA': North America
        -   'US': United States
        -   'US-MT': United States, Montana
    material_form : str
        Final form of the product.
    """
    return _get_carbon_data('dry density', species, region, material_form), _get_carbon_data('dry density unit', species, region, material_form)


if __name__ == '__main__':
    pass
