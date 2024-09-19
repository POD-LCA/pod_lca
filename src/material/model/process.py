from material.model.master import Master

class Process(Master):

    def __init__(self, id, name, model, stage):
        super().__init__(id, name, model, stage)
    
class transportationProcess(Process):

    def __init__(self, id, name, model, stage):
        super().__init__(id, name, model, stage)
        self.transported_distance = 0.0
        self.transported_weight = 0.0
        self.transported_distance_unit = None
        self.transported_weight_unit = None
        self.transported_products = []

    def __reduce__(self):
        
        return (self.__class__, (self.id, self.name, None, self.life_cycle_stage,), {"model": self.model, "year":self.year, 
                                                                                     "impacts": self.impacts, 
                                                                                     "database_item": self.database_item, 
                                                                                     "qty": self.qty, "unit":self.unit,
                                                                                     "transported_distance": self.transported_distance,
                                                                                     "transported_weight": self.transported_weight,
                                                                                     "transported_products": self.transported_products,
                                                                                     "transported_distance_unit": self.transported_distance_unit,
                                                                                     "transported_weight_unit": self.transported_weight_unit})
    
    def get_transported_distance(self):

        return self.transported_distance
    
    def get_transported_weight(self):

        return self.transported_weight
    
    def get_transported_distance_unit(self):
        
        return self.transported_distance_unit
    
    def get_transported_weight_unit(self):

        return self.transported_weight_unit
    
    def get_transported_products(self):

        return self.transported_products

    def set_transported_distance(self, qty):

        if isinstance(qty, str):
            try:
                qty = float(qty)
            except:
                raise TypeError

        self.transported_distance = qty

        self.update_qty(self.transported_distance * self.get_transported_weight())

    def set_travel_weight(self):

        weight = 0.0
        products = self.get_transported_products()
        for product in products:
            weight_added = product.get_weight()
            weight_conversion = self.get_calculator().conversion_factor(product.get_weight_unit(), self.get_transported_weight_unit())
            weight += (weight_added * weight_conversion)
        
        self.transported_weight = weight

        self.update_qty(self.transported_distance * self.transported_weight)

    def set_transported_distance_unit(self, unit):
        
        self.transported_distance_unit = unit
    
    def set_transported_weight_unit(self, unit):

        self.transported_weight_unit = unit

    def set_unit(self):

        self.unit = self.get_transported_weight_unit() + self.get_transported_distance_unit()
    
    def set_transported_products(self, products):

        if len(self.get_transported_products()) == 0:
            weight_unit = products[0].get_weight_unit() if isinstance(products, list) else products.get_weight_unit()
            self.set_transported_weight_unit(weight_unit)
            self.set_unit()
    
        if isinstance(products, list):
            self.get_transported_products().extend(products)
        else:
            self.get_transported_products().append(products)
        
        self.set_travel_weight()

    def remove_transported_product(self, item):

        products = self.get_transported_products()
        try:
            products.remove(item)
        except:
            pass # item not in list

        self.set_travel_weight()
