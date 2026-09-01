__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class ArrayMethods:

    @staticmethod
    def get_attribute_as_list(objects, attr_name):
        """Get a specified attribute from objects in a list, and returns the attribute entries in a list.

        Parameters
        ----------
        objects : list of object
            List of objects.
        attr_name : str
            Attribute to be retrieved in a list.

        Returns
        -------
        list
            List of the attribute entries
        """
        return [getattr(obj, attr_name) for obj in objects]

    @staticmethod
    def sort_by_attribute(objects, attr_name, descending=True):
        """Sort a list of objects by a specified attribute value.

        Parameters
        ----------
        objects : list of object
            List of objects.
        attr_name : str
            Attribute to be retrieved in a list.
        descending : bool
            If true, the list is ordered in the descending order of the attribute value.

        Returns
        -------
        list
            List of the attribute entries
        """
        return sorted(objects, key=lambda obj: getattr(obj, attr_name), reverse=descending)

    @staticmethod
    def set_value(objects, attr_name, value):
        """Sort a list of objects by a specified attribute value.

        Parameters
        ----------
        objects : list of object
            List of objects.
        attr_name : str
            Attribute to be retrieved in a list.
        value : str or int or float or bool
            Value to be given to the attribute.
        """
        for obj in objects:
            setattr(obj, attr_name, value)

    @staticmethod
    def find(objects, attr_name, value, return_first=False):
        """Find objects whose attribute matches the given value.

        Parameters
        ----------
        objects : list of object
            List of objects.
        attr_name : str
            Attribute (or method) to search.
        value : any
            Value to match.
        return_first : bool
            If True, return the first matching object; otherwise, return a list of all matching objects.

        Returns
        -------
        object or None
            Matching object, or None if not found.
        """
        matches = []
        for obj in objects:
            member = getattr(obj, attr_name)

            # check if it is a method
            if callable(member):
                member_value = member()
            else:
                member_value = member

            if member_value == value:
                if return_first:
                    return obj
                else:
                    matches.append(obj)

        if matches:
            return matches
        else:
            return None
    

if __name__ == "__main__":
    pass
