__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu; mhtaba@uw.edu"
__version__ = "0.1.0"

def get_attribute_as_list(objects, attr_name):
    """ Get a specified attribute from objects in a list, and returns the attribute entries in a list.
        
        Parameters
        ----------
        objects : List of Obj.
            List of objects.
        attr_name : str.
            Attribute to be retrieved in a list.

        Returns
        -------
        list
            List of the attribute entries
    """
    
    return [getattr(obj, attr_name) for obj in objects]


def sort_by_attribute(objects, attr_name, descending=True):
    """ Sort a list of objects by a specified attribute value.
        
        Parameters
        ----------
        objects : List of Obj.
            List of objects.
        attr_name : str.
            Attribute to be retrieved in a list.
        descending : bool
            If true, the list is ordered in the descending order of the attribute value.

        Returns
        -------
        list
            List of the attribute entries
    """
    return sorted(objects, key=lambda obj: getattr(obj, attr_name), reverse=descending)

def set_value(objects, attr_name, value):
    """ Sort a list of objects by a specified attribute value.
        
        Parameters
        ----------
        objects : List of Obj.
            List of objects.
        attr_name : str.
            Attribute to be retrieved in a list.
        value : str/int/float/bool
            Value to be given to the attribute.
    """

    for obj in objects:
        setattr(obj, attr_name, value)
