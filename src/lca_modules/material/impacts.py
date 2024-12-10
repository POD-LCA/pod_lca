
__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
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

    def __init__(self, parent):
        self.parent = parent
        if parent is not None:
            for impact in parent.get_project().get_database().get_impact_categories():
                setattr(self, impact, 0.0)

    def __reduce__(self):

        return (self.__class__, (None,), self.__dict__)
    
    def __setstate__(self, state):
        self.__dict__.update(state)   

    def updateImpactQty(self, impacts):
        """ Update the impact quantities.
        
        Parameters
        ----------
        impacts : dict
            Dictionary of impacts {impact catergory (str): impact quantity (float)}
        """

        for key, value in impacts.items():
            setattr(self, key, value)

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
        
    def get_parent(self):
        """ Retrieve the product or process object to which this impact belong.
        
        Returns
        -------
        aster Obj.
            Product or process object to which this impact belong.
        """

        return self.parent
        
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
        # FIXME: The method needs to be updated

        if method == 'TRACI_EPA':
            weights = {'GWP':16, 'AP':5, 'EP':5, 'ODP':5, 'SFP':6}
        elif method == 'TRACI_NIST':
            weights = {'GWP':16, 'AP':5, 'EP':5, 'ODP':5, 'SFP':6}
        else:
            raise NotImplementedError
        
        weighted_impact = 0.0
        for (impact_cat, weight) in weights.items():
            impact = getattr(self, impact_cat, None)
            if impact is not None:
                weighted_impact += impact * weight
            else:
                return None
        
        return weighted_impact


    def copy(self):
        """ Make a copy of the impact object.

            Returns
            -------
            Impacts Obj.
                Copy of the object.
        """

        new_obj = Impacts(None)
        new_obj.__dict__.update(self.__dict__)

        return new_obj

if __name__ == '__main__':
    pass
