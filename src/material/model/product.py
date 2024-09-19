from material.model.master import Master

class Product(Master):

    def __init__(self, id, name, model, stage):
        super().__init__(id, name, model, stage)
        self.weight = 0.0
        self.weight_unit = 'kg'
        self.density = 1.0 # the weight of 1 unit of prodcut
        self.transporter = None
        self.is_material = False
        self.is_energy = False

    def __reduce__(self):
        return (self.__class__, (self.id, self.name, None, self.life_cycle_stage), {"model": self.model, "year":self.year, "impacts": self.impacts,
                                                                                    "database_item": self.database_item, 
                                                                                    "qty": self.qty, "weight": self.weight, "transporter": self.transporter,
                                                                                    "density": self.density, "unit":self.unit, 
                                                                                    "is_material":self.is_material, "is_energy":self.is_energy})

    def update_qty(self, qty):
        """ Update the qty of the product.
            This will also re-set the corresponding impact quantities.
            
        Parameters:
        ----------
        qty : float
            Product quantity.
        
        """
        
        if isinstance(qty, str):
            try:
                qty = float(qty)
            except:
                raise TypeError
            
        self.qty = qty
        self.weight = self.qty * self.density

        self.set_impacts_qtys()

    def set_density(self, density):

        if isinstance(density, str):
            try:
                density = float(density)
            except:
                raise TypeError
    
        self.density = density
    
    def set_unit(self, unit):

        self.unit = unit
        # TODO: update density

    def set_weight_unit(self, unit):

        self.weight_unit = unit
    
    def set_transporter(self, transporter):
        
        self.transporter = transporter
        transporter.set_travel_weight()
    
    def get_weight(self):

        return self.weight
    
    def get_transporter(self):

        return self.transporter
    
    def get_weight_unit(self):

        return self.weight_unit

class Fuel(Product):

    def __init__(self, id, name, model, stage):
        super().__init__(id, name, model, stage)
        self.is_material = True
        self.is_energy = True

class Emission(Product):

    def __init__(self, id, name, model, stage):
        super().__init__(id, name, model, stage)
        self.is_emssion = True

class Waste(Product):

    def __init__(self, id, name, model, stage):
        super().__init__(id, name, model, stage)
        self.is_waste = True
