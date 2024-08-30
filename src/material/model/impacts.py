class Impacts:

    def __init__(self, parent):
        self.parent = parent
        self.GWP = 0.0
        self.acid_pot = 0.0
        self.eutro_pot = 0.0
        self.ozone_dep = 0.0
        self.smog = 0.0
        # TODO: Have consistent reference to impact categories. Impact category names are maintained in database and not refered to in model.
        # changes are also required in get_impact and where updateImpactQty are called...
        # self.impact_qtys = {}
        # self.set_impact_categories()

    def __reduce__(self):

        return (self.__class__, (None), {"parent": self.parent,
                                         "GWP": self.GWP, "acid_pot":self.acid_pot,
                                         "eutro_pot": self.eutro_pot, "ozone_pot":self.ozone_dep,
                                         "smog": self.smog})
    
    def __setstate__(self, state):
        self.__dict__.update(state)

    # def set_impact_categories(self):

    #     impact_cats = self.get_parent().get_project().get_database().get_impact_categories()
    #     self.impact_qtys = {key: None for key in impact_cats}    

    def updateImpactQty(self, GWP=0.0, acid_pot=0.0, eutro_pot=0.0, ozone_dep=0.0, smog=0.0):

        self.GWP = GWP
        self.acid_pot = acid_pot
        self.eutro_pot = eutro_pot
        self.ozone_dep = ozone_dep
        self.smog = smog

    # def set_impact(self, impact_cat, qty):

    #     self.impact_qtys[impact_cat] = qty    

    def get_impact(self, impact_cat):

        if impact_cat == 'GWP':
            return self.GWP
        elif impact_cat == 'acid_pot':
            return self.acid_pot
        elif impact_cat == 'eutro_pot':
            return self.eutro_pot
        elif impact_cat == 'ozone_dep':
            return self.ozone_dep
        elif impact_cat == 'smog':
            return self.smog
        else:
            raise NameError
        
    def get_parent(self):

        return self.parent
