
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


def compute_sensitivity_of_param(obj, param, impact_cat='weighted', printout=True, **kwargs):
    """ Compute the sensitivity of a parameter of an object.

        Parameters
        ----------
        obj : Master Obj
            Entry on which the sensitivity is tested.
        param : str
            Parameter varied.
            This must be an attribute of the object.
        impact_cat : str
            Impact category considered.
            Weighted impact, if 'weighted'
        printout : bool
            Printout results if true.
            Default - True
        **kwargs
            range : tuple
                Minimum and maximum value for the parameter.
                e.g., qty of a product or process.
            options : list of str.
                A range of options given as strings for the parameter.
                e.g., database_item name (i.e., to change the impact value)


        Returns
        -------
        tuple
            Minimum and maximum percentage change of impact.
    """

    model = obj.get_model()
    project =  model.get_project()
    claculator = project.get_calculator()

    base_val = getattr(obj, param)
    base_impact = claculator.get_total_impact(model.get_name(), impact_cat)

    method_name = 'set_'+ param
    method = getattr(obj, method_name)

    result_range = [0, 0]
    if 'range' in kwargs:
        range_lst = sorted((kwargs['range']))

        if (base_val > range_lst[1]) or (base_val < range_lst[0]):
            raise ValueError(f"The range of {param} ({range_lst}) does not include the base value ({base_val})")
        
        for i in [0,1]:
            method(range_lst[i])
            impact_new = claculator.get_total_impact(model.get_name(), impact_cat)
            percentage_change = 100 * (impact_new - base_impact) / base_impact

            result_range[i] = percentage_change
            
    elif 'options' in kwargs:
        results = []
        for option in kwargs['options']:
            method(option)
            impact_new = claculator.get_total_impact(model.get_name(), impact_cat)
            percentage_change = 100 * (impact_new - base_impact) / base_impact

            results.append(percentage_change)

        result_range[0] = min(results)
        result_range[1] = max(results)

        corr_options = [kwargs['options'][results.index(min(results))], 
                        kwargs['options'][results.index(max(results))]]

    else:
        raise KeyError(f"Either the range or option data not provided or key used is invalid.")

    if printout:
            print("*"*50 + "\nSENSITIVITY ANALYSIS\n" + "*"*50)
            print(f"Product: {obj.get_name()}")
            print(f"Param: {param}")
            print(f"Base value: {base_val}")
            if 'range' in kwargs:
                print(f"Range: {range_lst}")
            elif 'options' in kwargs:
                print(f"Options: {kwargs['options']}")
            formatted_result = ", ".join(f"{num:.1f}" for num in result_range)
            print(f"Sensitivity (%): ({formatted_result})")
            if 'options' in kwargs:
                print(f"       : {corr_options}")

    return result_range

def compute_sensitivity_of_params(model, groups, impact_cat='weighted', printout=True,):
    """ Compute the sensitivity of a parameters of multiple objects.
        Sensitivity is computed with all effects in combination.

        Parameters
        ----------
        model : Model Obj.
            Model in which the sensitivity is considered.
        groups : List of dict
            [{'obj': Master Obj, 'param': str, 'range': tuple}, 
             {'obj': Master Obj, 'param': str, 'options': list of str},
             ...
            ]
            where;
                obj : Master Obj
                    Entry on which the sensitivity is tested.
                param : str
                    Parameter varied.
                    This must be an attribute of the object.
                range : tuple
                    Minimum and maximum value for the parameter, in that order.
                    e.g., qty of a product or process.
                options : list of str.
                    A range of options given as strings for the parameter.
                    e.g., database_item name (i.e., to change the impact value)

        Returns
        -------
        tuple
            Minimum and maximum percentage change of impact.
    """

    project =  model.get_project()
    claculator = project.get_calculator()

    base_impact = claculator.get_total_impact(model.get_name(), impact_cat)

    results = {}
    for objective in ['min', 'max']:
        for group in groups:
            obj = group['obj']
            param = group['param']
            base_val = getattr(obj, param)

            method_name = 'set_'+ param
            method = getattr(obj, method_name)
            
            if 'range' in group:
                range_lst = sorted((group['range']))
                if (base_val > range_lst[1]) or (base_val < range_lst[0]):
                    raise ValueError(f"The range of {param} ({range_lst}) does not include the base value ({base_val})")
                
                i = 0 if objective == 'min' else 1
                method(range_lst[i])
                    
            elif 'options' in group:
                selected_option = None
                ref_impact = base_impact
                for option in group['options']:
                    method(option)
                    impact_tmp = claculator.get_total_impact(model.get_name(), impact_cat)
                    if (objective == 'min' and impact_tmp <= ref_impact) or (objective == 'max' and impact_tmp >= ref_impact):
                        selected_option = option
                        ref_impact = impact_tmp

                method(selected_option)
                obj.update_impacts()

                if objective == 'min':
                    group['min_option'] = selected_option
                else:
                    group['max_option'] = selected_option

            else:
                raise KeyError(f"Either the range or option data not provided or key used is invalid.")
            
        impact_new = claculator.get_total_impact(model.get_name(), impact_cat)
        percentage_change = 100 * (impact_new - base_impact) / base_impact

        results[objective] = percentage_change

    if printout:
            print("*"*50 + "\nSENSITIVITY ANALYSIS\n" + "*"*50)
            for group in groups:
                print(f"Product: {obj.get_name()}")
                print(f"Param: {param}")
                print(f"Base value: {base_val}")
                if 'range' in group:
                    print(f"Range: {group['range']}")
                elif 'options' in group:
                    print(f"Options: {group['options']}")
            print('-'*50)        
            formatted_result = f"{results['min']:.1f}, {results['max']:.1f}"
            print(f"Sensitivity (%): ({formatted_result})")
            for group in groups:
                if 'options' in group:
                    print(f"       : ({group['min_option']}, {group['max_option']})")

    return [results['min'], results['max']]

#TODO: look to simplify or identify reusable parts