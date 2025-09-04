
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class Records:
    """ Records object keep record of the inventory (e.g., impacts, emissions, carbon storage) created by a product or a process.

    Attributes
    ----------
    parent : ~pod_lca.materials_screening.Master
        The product or process object to which this record belong.
    <record_category> : float
        Record categories are dynamically set based on the class.
        Class variable 'record_attr_dict' keep track of the record category names and corresponding units.
    """
    record_type = "Abstract Record"
    record_attr_dict = {}

    def __init__(self):
        self.parent = None

    def __str__(self):
        if self.get_parent() is None:
            parent_name = '<None>'
        else:
            parent_name = self.get_parent().get_name()
        str = "="*50 + "\n" + f"{self.__class__.record_type} of {parent_name}\n" + "="*50 + "\n"
        for attr, unit in self.__class__.record_attr_dict.items():
            str += f"{attr:<20} {getattr(self, attr):<5} {unit:<20}\n"

        return str

    def __add__(self, other):
        """ Addition of two records.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        summed_records = {attr: getattr(self, attr, 0.0) + getattr(other, attr, 0.0)
                        for attr in self.__class__.record_attr_dict.keys()}
        
        new_record = self.__class__()
        new_record.set_parent(None)
        new_record.update_qty(summed_records)

        return new_record

    def __iadd__(self, other):
        """ In-place addition of two records.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        for attr in self.__class__.record_attr_dict.keys():
            setattr(self, attr, getattr(self, attr, 0) + getattr(other, attr, 0.0))

        return self
    
    def __sub__(self, other):
        """ Subtraction of two records.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        difference_records = {attr: getattr(self, attr, 0.0) - getattr(other, attr, 0.0)
                                for attr in self.__class__.record_attr_dict.keys()}
        
        new_record = self.__class__()
        new_record.set_parent(None)
        new_record.update_qty(difference_records)

        return new_record

    def __isub__(self, other):
        """ In-place subtraction of two records.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        for attr in self.__class__.record_attr_dict.keys():
            setattr(self, attr, getattr(self, attr, 0) - getattr(other, attr, 0.0))

        return self
    
    def __mul__(self, scalar):
        """ Multiplication of a record by a scalar.
        """
        if not isinstance(scalar, (int, float)):
            return NotImplemented

        multiplied_records = {attr: getattr(self, attr, 0.0) * scalar
                            for attr in self.__class__.record_attr_dict.keys()}
        
        new_record = self.__class__()
        new_record.set_parent(self.parent)
        new_record.update_qty(multiplied_records)

        return new_record
    
    def __imul__(self, scalar):
        """ In-place multiplication of a record.
        """
        if not isinstance(scalar, (int, float)):
            return NotImplemented

        for attr in self.__class__.record_attr_dict.keys():
            setattr(self, attr, getattr(self, attr, 0) * scalar)

        return self

    def __rmul__(self, scalar):
        """ Reflexive multiplication of a record by a scalar.
        """
        return self.__mul__(scalar)

    # ========================
    # Constructors
    # ========================
    @classmethod
    def from_parent(cls, parent):
        """ Create an record object from a parent object.
        
        Parameters
        ----------
        parent : ~pod_lca.materials_screening.Master
            The product or process object to which this record belong.
        
        Returns
        -------
        ~pod_lca.impacts.Records
            Record created.
        """
        record_obj = cls()
        record_obj.set_parent(parent)

        for attr in cls.record_attr_dict.keys():
            setattr(record_obj, attr, 0.0)

        return record_obj
    
    @classmethod
    def from_dict(cls, record_dict):
        """ Create an record object from a dictionary.
        
        Parameters
        ----------
        record_dict : dict
            Dictionary of records {**record catergory** (:class:`str`): **record quantity** (:class:`float`)}
        
        Returns
        -------
        ~pod_lca.impacts.Records
            Record created.
        """
        record_obj = cls()
        record_obj.set_parent(None)
        record_obj.update_qty(record_dict)

        return record_obj

    @classmethod
    def copy(cls, record_obj):
        """ Make a copy of the record object.

        Returns
        -------
        ~pod_lca.impacts.Records
            Copy of the object.
        """
        new_obj = cls()
        new_obj.__dict__.update(record_obj.__dict__)

        return new_obj
        
    # ========================
    # Getters and Setters
    # ========================
    def set_parent(self, parent):
        """ Set the parent object.
        
        Parameters
        ----------
        parent : ~pod_lca.materials_screening.Master.
            The product or process object to which this record belong.
        """
        self.parent = parent

        return self
    
    def get_parent(self):
        """ Retrieve the product or process object to which this record belong.
        
        Returns
        -------
        ~pod_lca.materials_screening.Master
            Product or process object to which this record belong.
        """
        return self.parent
    
    def get_categories(self, units=False):
        """ Retrieves the categories (i.e., entry names) in the record.

        Parameters
        ----------
        units : bool
            If true, returns a dictionary of categories and corresponding units.

        Returns
        -------
        :class:`list`
            list of categories.
        :class:`dict`
            Dictionary of units, keyed by category name.
        """
        if units:
            return list(self.record_attr_dict.keys()), self.record_attr_dict
        else:
            return list(self.record_attr_dict.keys())
    
    # ========================
    # Methods
    # ========================
    def clear_qty(self):
        """ Set all record quantities to zero.
        """
        for attr in self.__class__.record_attr_dict.keys():
            setattr(self, attr, 0.0)

        return self
    
    def update_qty(self, records):
        """ Update the record quantities.
        
        Parameters
        ----------
        records : dict
            Dictionary of records - { **record catergory** (:class:`str`): **record quantity** (:class:`float`)}
        """
        for key, value in records.items():
            if key not in self.__class__.record_attr_dict.keys():
                raise KeyError(f"{self.__class__.record_type} category '{key}' not found in the record categories.")
            if not isinstance(value, (int, float)):
                raise TypeError(f"{self.__class__.record_type} quantity '{value}' is not a number.")
            setattr(self, key, value)

        return self
    
    def get_record(self, attr):
        """ Get the quantity of a specific record attribute.
        
        Parameters
        ----------
        attr : str
            Name of the record attribute of concern (e.g., impact category, emission gas).

        Returns
        -------
        float
            Quantity of the record attribute.
        """
        return getattr(self, attr, None)
    
    def get_record_dict(self, units=False):
        """ Get the record as a dictionary.

        Parameters
        ----------
        units : bool
            If true, returns corresponding units as well.
        
        Returns
        -------
        dict
            Dictionary of impacts - { **impact catergory** (:class:`str`): **impact quantity** (:class:`float`)}
            or { **impact catergory** (:class:`str`): (**impact quantity** (:class:`float`), **unit** (:class:`str`))}
        """
        if units:
            record = {record: (getattr(self, record, 0.0), self.__class__.record_attr_dict[record]) for record in self.__class__.record_attr_dict.keys()}
        else:
            record = {record: getattr(self, record, 0.0) for record in self.__class__.record_attr_dict.keys()}

        return record


if __name__ == '__main__':
    pass
