
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class SensitivityAnalysis:

    def compute_sensitivity_of_param(obj, param, impact_cat='weighted', sensitivity_type='relative', printout=True, **kwargs):
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
        sensitivity_type : str
            Type of sensitivity analysis.
            'relative' - relative percentage change of impact.  (default)
            'symmetric' - symmetric percentage change of impact.
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

        base_impact = model.get_total_impact(impact_cat)
        base_val = getattr(obj, param)

        method_name = 'set_'+ param
        method = getattr(obj, method_name)

        result_range = [0, 0]
        impacts_range = [None, None]
        if 'range' in kwargs:
            range_lst = sorted((kwargs['range']))

            if (base_val > range_lst[1]) or (base_val < range_lst[0]):
                raise ValueError(f"The range of {param} ({range_lst}) does not include the base value ({base_val})")
            
            for i in [0,1]:
                method(range_lst[i])
                impact_new = model.get_total_impact(impact_cat)
                relative_percentage_change = 100 * (impact_new - base_impact) / base_impact # TODO: make a choice (also Lines 70 and 178)
                symmetric_percentage_change = 100 * (impact_new - base_impact) / (base_impact + impact_new)

                if sensitivity_type == 'relative':
                    result_range[i] = relative_percentage_change
                elif sensitivity_type == 'symmetric':
                    result_range[i] = symmetric_percentage_change
                else:
                    raise ValueError(f"Invalid sensitivity type: {sensitivity_type}")   

                impacts_range[i] = impact_new

                method(base_val)
                
        elif 'options' in kwargs:
            results, impacts = [], []
            for option in kwargs['options']:
                method(option)
                impact_new = model.get_total_impact(impact_cat)
                relative_percentage_change = 100 * (impact_new - base_impact) / base_impact
                symmetric_percentage_change = 100 * (impact_new - base_impact) / (base_impact + impact_new)

                if sensitivity_type == 'relative':
                    results.append(relative_percentage_change)
                elif sensitivity_type == 'symmetric':
                    results.append(symmetric_percentage_change)
                else:
                    raise ValueError(f"Invalid sensitivity type: {sensitivity_type}")

                impacts.append(impact_new)

                method(base_val)

            result_range[0] = min(results)
            result_range[1] = max(results)

            impacts_range[0] = min(impacts)
            impacts_range[1] = max(impacts)        

            corr_options = [kwargs['options'][results.index(min(results))], 
                            kwargs['options'][results.index(max(results))]]

        else:
            raise KeyError(f"Either the range or option data not provided or key used is invalid.")

        if printout:
                print("*"*50 + "\nSENSITIVITY ANALYSIS\n" + "*"*50)
                print(f"Product: {obj.get_name()}")
                print(f"Param: {param}")
                print(f"Base value: {base_val}")
                print(f"Base impact: {base_impact}")
                if 'range' in kwargs:
                    print(f"Range: {range_lst}")
                elif 'options' in kwargs:
                    print(f"Options: {kwargs['options']}")
                formatted_result = ", ".join(f"{num:.1f}" for num in result_range)
                print(f"Sensitivity (%): ({formatted_result})")
                print(f"Impacts Range: {impacts_range}")
                if 'options' in kwargs:
                    print(f"       : {corr_options}")
                if sensitivity_type == 'relative':
                    print("(Sensitivity as relative percentage change)")
                elif sensitivity_type == 'symmetric':
                    print("(Sensitivity as symmetric percentage change)")
                else:
                    raise ValueError(f"Invalid sensitivity type: {sensitivity_type}")

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

        base_impact = model.get_total_impact(impact_cat)

        for group in groups:
            obj = group['obj']
            param = group['param']
            base_val = getattr(obj, param)

            method_name = 'set_'+ param
            method = getattr(obj, method_name)

            group['base_val'] = base_val
            group['method'] = method

        results = {}
        for objective in ['min', 'max']:
            for group in groups:
                obj = group['obj']
                param = group['param']
                base_val = group['base_val']
                method = group['method']
                
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
                        impact_tmp = model.get_total_impact(impact_cat)
                        if (objective == 'min' and impact_tmp <= ref_impact) or (objective == 'max' and impact_tmp >= ref_impact):
                            selected_option = option
                            ref_impact = impact_tmp

                    method(selected_option)
                    obj.update_inventory_records()

                    if objective == 'min':
                        group['min_option'] = selected_option
                    else:
                        group['max_option'] = selected_option

                else:
                    raise KeyError(f"Either the range or option data not provided or key used is invalid.")
                
            impact_new = model.get_total_impact(impact_cat)
            relative_percentage_change = 100 * (impact_new - base_impact) / base_impact
            symmetric_percentage_change = 100 * (impact_new - base_impact) / (base_impact + impact_new)

            results[objective] = relative_percentage_change

            for group in groups:
                base_val = group['base_val']
                method = group['method']

                method(base_val)

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
                print("(Sensitivity as symmetric percentage change)")

        return [results['min'], results['max']]


if __name__ == '__main__':
    pass
