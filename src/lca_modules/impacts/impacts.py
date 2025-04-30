from lca_modules.impacts.impact_categories import IMPACT_CATEGOREIS, IMPACT_WEIGHTING_FACTOR_EPA, IMPACT_WEIGHTING_FACTOR_NIST

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class Impacts:
    """
    Impacts object keep record of the impacts created by a product or a process.

    Attributes
    ----------
    parent : Master Obj.
        The product or process object to which this impact belong.
    <impact_category> : float
        Impact categories are dynamically set based on the database attached to the project.
        Database keep track of the impact category names.
    """

    def __init__(self):
        self.parent = None

    def __str__(self):
        if self.get_parent() is None:
            parent_name = '<None>'
        else:
            parent_name = self.get_parent().get_name()
        str = "="*50 + "\n" + f"Impacts of {parent_name}\n" + "="*50 + "\n"
        for impact, unit in IMPACT_CATEGOREIS.items():
            str += f"{impact:<20} {getattr(self, impact):<5} {unit:<20}\n"

        return str

    def __add__(self, other):
        """ Addition of two impacts."""
        if not isinstance(other, Impacts):
            return NotImplemented

        summed_impacts = {attr: getattr(self, attr, 0.0) + getattr(other, attr, 0.0)
                        for attr in IMPACT_CATEGOREIS.keys()}
        
        new_impact = Impacts()
        new_impact.set_parent(None)
        new_impact.update_impact_qty(summed_impacts)

        return new_impact

    def __iadd__(self, other):
        """ In-place addition of two impacts."""
        if not isinstance(other, Impacts):
            return NotImplemented

        for attr in IMPACT_CATEGOREIS.keys():
            setattr(self, attr, getattr(self, attr, 0) + getattr(other, attr, 0.0))

        return self
    
    def __mul__(self, scalar):
        """ Multiplication of an impact by a scalar."""
        if not isinstance(scalar, (int, float)):
            return NotImplemented

        multiplied_impacts = {attr: getattr(self, attr, 0.0) * scalar
                            for attr in IMPACT_CATEGOREIS.keys()}
        
        new_impact = Impacts()
        new_impact.set_parent(self.parent)
        new_impact.update_impact_qty(multiplied_impacts)

        return new_impact
    
    def __imul__(self, scalar):
        """ In-place multiplication of an impact."""

        if not isinstance(scalar, (int, float)):
            return NotImplemented

        for attr in IMPACT_CATEGOREIS.keys():
            setattr(self, attr, getattr(self, attr, 0) * scalar)

        return self

    def __rmul__(self, scalar):
        """ Reflexive multiplication of an impact by a scalar."""
        return self.__mul__(scalar)
    
    # ========================
    # Constructors
    # ========================
    @classmethod
    def from_parent(cls, parent):
        """ Create an impact object from a parent object.
        
        Parameters
        ----------
        parent : Master Obj.
            The product or process object to which this impact belong.
        
        Returns
        -------
        Impacts Obj.
            Impact object created.
        """

        impact_obj = cls()
        impact_obj.set_parent(parent)

        for impact in IMPACT_CATEGOREIS:
            setattr(impact_obj, impact, 0.0)

        return impact_obj
    
    @classmethod
    def from_dict(cls, impact_dict):
        """ Create an impact object from a dictionary.
        
        Parameters
        ----------
        impact_dict : dict
            Dictionary of impacts {impact catergory (str): impact quantity (float)}
        
        Returns
        -------
        Impacts Obj.
            Impact object created.
        """

        impact_obj = cls()
        impact_obj.set_parent(None)
        impact_obj.update_impact_qty(impact_dict)

        return impact_obj

    @classmethod
    def copy(cls, impact_obj):
        """ Make a copy of the impact object.

            Returns
            -------
            Impacts Obj.
                Copy of the object.
        """

        new_obj = cls()
        new_obj.__dict__.update(impact_obj.__dict__)

        return new_obj
        
    # ========================
    # Getters and Setters
    # ========================
    def set_parent(self, parent):
        """ Set the parent object.
        
        Parameters
        ----------
        parent : Master Obj.
            The product or process object to which this impact belong.
        """

        self.parent = parent

        return self
    
    def get_parent(self):
        """ Retrieve the product or process object to which this impact belong.
        
        Returns
        -------
        Master Obj.
            Product or process object to which this impact belong.
        """

        return self.parent

    # ========================
    # Methods
    # ========================
    def clear_impact_qty(self):
        """ Set all impact quantities to zero."""

        for impact in IMPACT_CATEGOREIS:
            setattr(self, impact, 0.0)

        return self
    
    def update_impact_qty(self, impacts):
        """ Update the impact quantities.
        
        Parameters
        ----------
        impacts : dict
            Dictionary of impacts {impact catergory (str): impact quantity (float)}
        """

        for key, value in impacts.items():
            setattr(self, key, value)

        return self

    def get_impact(self, impact_cat):
        """ Get the quantity of a specific impact category.
        
        Parameters
        ----------
        impact_cat : str
            Name of the impact category of concern.

        Returns
        -------
        float
            Quantity of the impact.
        """

        return getattr(self, impact_cat, None)
        
    def get_weighted_impact(self, method='TRACI_EPA'):
        """ Get a weighted value for impacts.
            Ref: [1] The Carbon Leadership Forum. (2018) Life Cycle ASssesment of Buildings: A Practice Guide. 
                     DOI: http://hdl.handle.net/1773/41885
        
        Parameters
        ----------
        method : str
            Which weightages to be used:
                'TRACI_EPA' - from Ref [1]
                'TRACI_NIST' - from Ref [1]
            
        Returns
        -------
        float
            The weighted impact.
        """

        if method == 'TRACI_EPA':
            weights = IMPACT_WEIGHTING_FACTOR_EPA
        elif method == 'TRACI_NIST':
            weights = IMPACT_WEIGHTING_FACTOR_NIST
        else:
            raise NotImplementedError
        
        # TODO: normalise the impacts begore applying weights
        weighted_impact = 0.0
        for (impact_cat, weight) in weights.items():
            impact = getattr(self, impact_cat, None)
            if impact is not None:
                weighted_impact += impact * weight
            else:
                return None
        
        return weighted_impact

if __name__ == '__main__':
    pass
