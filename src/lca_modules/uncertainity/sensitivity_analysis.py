
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


def compute_sensitivity(obj, param, **kwargs):
    """ Compute the sensitivity of a parameter of an object.

        Parameters
        ----------
        obj : Master Obj  #TODO: this list will extend as Building/Transportation modules are added
            Entry on which the sensitivity is tested.
        param : str
            Parameter varied.
            This must be an attribute of the object.
        impact_cat : str
            Impact category considered.
            Weighted impact, if 'weighted'
        **kwargs
            range : tuple
                Minimum and maximum value for the parameter.
                e.g., qty of a product or process.
            options : list of str.
                A range of options given as strings for the parameter.
                e.g., database_item name (i.e., to change the impact value)
            impact_cat : str
                Impact category name.
                Default - 'weighted'
            printout : bool
                Printout results if true.
                Default - True

        Returns
        -------
        tuple
            Minimum and maximum percentage change of impact.
    """

    impact_cat = kwargs['impact_cat'] if 'impact_cat' in kwargs else 'weighted'
    printout = kwargs['printout'] if 'printout' in kwargs else True

    model = obj.get_model()
    project =  model.get_project()
    claculator = project.get_calculator()

    base_val = getattr(obj, param)
    base_impact = claculator.get_total_impact(model.get_name(), impact_cat)

    result_range = [0, 0]
    if 'range' in kwargs:
        if (base_val > kwargs['range'][1]) or (base_val < kwargs['range'][0]):
            raise ValueError(f"The range of {param} ({kwargs['range']}) does not include the base value ({base_val})")
        
        for i in [0,1]:
            setattr(obj, param, kwargs['range'][i])
            obj.update_impacts()
            impact_new = claculator.get_total_impact(model.get_name(), impact_cat)
            percentage_change = 100 * (impact_new - base_impact) / base_impact

            result_range[i] = percentage_change
            #TODO: calculate and print point sensitivity
    elif 'options' in kwargs:
        results = []
        for option in kwargs['options']:
            setattr(obj, param, option)
            obj.update_impacts()
            impact_new = claculator.get_total_impact(model.get_name(), impact_cat)
            percentage_change = 100 * (impact_new - base_impact) / base_impact

            results.append(percentage_change)

        result_range[0] = min(results)
        result_range[1] = max(results)
    else:
        raise KeyError(f"Either the range or option data not provided or key used is invalid.")
        #TODO: is there a defaulting option

    if printout:
            print("*"*50 + "\nSENSITIVITY ANALYSIS\n" + "*"*50)
            print(f"Product: {obj.get_name()}")
            print(f"Param: {param}")
            print(f"Base value: {base_val}")
            if 'range' in kwargs:
                print(f"Range: {kwargs['range']}")
            elif 'options' in kwargs:
                print(f"Options: {kwargs['options']}")
            formatted_result = ", ".join(f"{num:.1f}" for num in result_range)
            print(f"Sensitivity: ({formatted_result})")

    return result_range

    # TODO: sensetivity for combinrd changes