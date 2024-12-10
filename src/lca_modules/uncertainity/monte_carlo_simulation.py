from utilities.objects import array_methods

import matplotlib.pyplot as plt

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class MonteCarloSimulation:
    """
    MonteCarloSimulation object carries out Monte Carlo Simulation.

    Attributes
    ----------
    project : Project Obj.
        Project on which the calculator operates.
    iterations : int
        No of iterations.
    var_param : List
        List of Distribution objects.
    impact_cat : str.
        Impact category considered for the impact calculation.

    """

    def __init__(self, project):
        self.project = project
        self.iterations = 10000
        self.var_params = []
        self.impact_cat = 'weighted'

        self.dists_short_list = ['norm', 'expon', 'uniform', 'beta', 'gamma', 'chi2', 't', 'f', 'lognorm', 'weibull_min']

        for model_name in project.get_model_names():
            self.set_var_params(model_name)

    def run(self, model_name):

        var_params = self.get_var_params(model_name)
        
        prob_data = []
        impact_data = []
        iter = 0
        while iter < self.iterations:
            prob = 1.00
            for distribution in var_params:
                var_value = distribution.pick_data_point()
                prob *= distribution.prob_of(var_value)
                
                obj = distribution.get_parent()
                setattr(obj, distribution.get_attr_name(), var_value)
                obj.update_impacts()

            total_impact = self.project.get_calculator().get_total_impact(model_name, self.impact_cat)
            prob_data.append(prob)
            impact_data.append(total_impact)
            iter +=1


        plt.scatter(impact_data, prob_data)
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.title("Quick Scatter Plot")
        plt.show(block=True)
        # TODO: plot the output_data set
        # TODO: fix curve and get distribution params

    #TODO Statistical analysis and variance reduction (https://onlinelibrary.wiley.com/doi/book/10.1002/9781118014967)
            

    def set_distributions(self, model_name):
        """Set distribution objects to all data objects in the project objects with dataset.
        """

        objects = self.project.get_model(model_name).get_products() + self.project.get_model(model_name).get_processes()

        for object in objects:
            for attr, dataset in object.get_datasets().items():
                if dataset.get_dist_fitted() is None:
                    best_fit = dataset.find_best_fit(is_cts=True, fit_method='MLE', validate=True, short_list=self.dists_short_list, printout=False)
                    if best_fit is None:
                        best_fit = dataset.find_best_fit(is_cts=True, fit_method='MLE', validate=True, printout=False)
                    distribution = dataset.set_distribution(best_fit)
                    object.set_distribution(distribution, attr)                 
                else:
                    # TODO: if it is not already in the distribution list, add it
                    pass

        # TODO: check the dataset and distribution are of same length
        
        pass

    def set_var_params(self, model_name):
        """Get variable parameters within the model.
        """

        self.set_distributions(model_name)

        objects = self.project.get_model(model_name).get_products() + self.project.get_model(model_name).get_processes()
        for object in objects:
            self.var_params.extend(list(object.get_distributions().values()))

        return self.var_params
        

    def set_impact_cat(self, impact_cat):

        self.impact_cat = impact_cat

    def get_var_params(self, model_name):
        """Get variable parameters within the model.
        """

        return self.var_params

    def set_scenarios(self, *args, **kwargs):
        """ Set scenarios for Scenario Aware Monte Carlo Simulations.
            This will update the variable parameters.
        """

        pass # TODO: implement

if __name__ == '__main__':
    pass