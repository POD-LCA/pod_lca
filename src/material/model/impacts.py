class Impacts:

    def __init__(self, parent):
        self.parent = parent
        if parent is not None:
            for key, value in parent.get_project().get_database().get_impact_categories().items():
                setattr(self, key, value)

    def __reduce__(self):

        return (self.__class__, (None,), self.__dict__)
    
    def __setstate__(self, state):
        self.__dict__.update(state)   

    def updateImpactQty(self, impacts):

        for key, value in impacts.items():
            setattr(self, key, value)

    def get_impact(self, impact_cat):

        return getattr(self, impact_cat)
        
    def get_parent(self):

        return self.parent
