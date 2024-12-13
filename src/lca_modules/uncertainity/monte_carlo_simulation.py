
from lca_modules.uncertainity.datasets import DataSet

import matplotlib.pyplot as plt
from numpy import mean, std, histogram, exp, log, linspace
from scipy.integrate import quad

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class MonteCarloSimulator:
    """
    MonteCarloSimulation object carries out Monte Carlo Simulation.

    Attributes
    ----------
    model : Model Obj.
        Model on which the hotspot analysis is performed.
    iterations : int
        No of iterations.
    impact_cat : str.
        Impact category considered for the impact calculation.
    var_param : List
        List of Distribution objects.
    result_dataset : DataSet Obj.
        Data from the Monte Carlo Simulation
    result_distribution: Distribution Obj
        Distribution fitted to the Monte Carlo simulation data


    """
    def __init__(self):
        self.model = None
        self.iterations = None
        self.impact_cat = None
        self.var_params = []

        self.scenario = []
        self.scenario_defs = {'low': 0.2, 'med': 0.5, 'high':0.8}

        self.result_dataset = None
        self.result_distribution = None
        
        self.dists_short_list = ['norm', 'expon', 'uniform', 'beta', 'gamma', 'chi2', 't', 'f', 'lognorm', 'weibull_min']


    @classmethod
    def from_model(cls, model):

        monte_carlo_simulator = cls()
        monte_carlo_simulator.set_model(model)
        monte_carlo_simulator.set_iterations(10000)
        monte_carlo_simulator.set_impact_cat("GWP")

        monte_carlo_simulator.set_var_params()
        
        return monte_carlo_simulator
    
    def set_model(self, model):

        self.model = model

    def set_iterations(self, no_iters):

        self.iterations = no_iters

    def set_impact_cat(self, impact_cat):

        self.impact_cat = impact_cat

    def set_var_params(self):
        """Get variable parameters within the model.
        """

        self.set_distributions()

        objects = self.model.get_all_items()
        for object in objects:
            self.var_params.extend(list(object.get_distributions().values()))

        return self.var_params
    
    def set_scenario(self, dict):

        self.scenario = dict
        
    def get_model(self):

        return self.model
    
    def get_iterations(self):

        return self.iterations
    
    def get_impact_cat(self):

        return self.impact_cat

    def get_var_params(self):
        """Get variable parameters within the model.
        """

        return self.var_params
    
    def get_scenario(self):

        return self.scenario

    def run(self):

        project = self.get_model().get_project()
        var_params_tmp = self.get_var_params()
        scenarios = self.get_scenario()

        var_params = []
        methods_list = {}
        for distribution in var_params_tmp:
            obj = distribution.get_parent()
            if obj in scenarios:
                method_name = 'set_'+ distribution.get_attr()
                method_obj = getattr(obj, method_name)
                value = distribution.dist.ppf(self.scenario_defs[scenarios[obj]])
                method_obj(value)
            else:
                var_params.append(distribution)
                method_name = 'set_'+ distribution.get_attr()
                methods_list[distribution] = getattr(obj, method_name)

        impact_data = []
        for iter_in_group in MonteCarloSimulator.get_groups(self.iterations, 1000):
            var_values = {}
            for distribution in var_params:
                var_values[distribution] = distribution.pick_data_points(iter_in_group)

            iter = 0        
            while iter < iter_in_group:
                for distribution in var_params:        
                    methods_list[distribution](var_values[distribution][iter])

                total_impact = project.get_calculator().get_total_impact(self.model.get_name(), self.impact_cat)
                impact_data.append(total_impact)
                iter +=1

        self.set_data(impact_data)
        self.print_results()

        return impact_data
    
    def set_data(self, impact_data):

        dataset = DataSet.from_data(impact_data, name='MonteCarloSimualation')
        if max(impact_data) - min(impact_data) == 0.0:
            self.result_dataset = dataset
            self.result_distribution = None
        else:
            best_fit = dataset.find_best_fit(is_cts=True, fit_method='MLE', validate=True, short_list=self.dists_short_list, printout=False)
            if best_fit is None:
                best_fit = dataset.find_best_fit(is_cts=True, fit_method='MLE', validate=True, printout=False)
            self.result_distribution = dataset.set_distribution(best_fit)
            self.result_dataset = dataset

    def print_results(self):
  
        print("*"*50 + "\nMONTE CARLO SIMULATION\n" + "*"*50)
        print(f"number of iterations: {self.get_iterations()}")

        data = self.result_dataset.get_data()
        if max(data) - min(data) == 0.0:
            print(f"Single point of data at {max(data)}")
        else:
            distribution = self.result_distribution.dist
            print(f"Data fitted to a {self.result_distribution.get_dist_name()} distribution")
            print(f"mean : {distribution.mean()}")
            print(f"std : {distribution.std()}")
    
    def plot_hist(self, bin_size):
        
        _, ax = plt.subplots()

        res = 100
        data = self.result_dataset.get_data()
        if not (max(data) - min(data) == 0.0):
            x = linspace(min(data), max(data), res)
            p = self.result_distribution.dist.pdf(x)
            ax.plot(x, p, 'k', linewidth=2, label='Fitted')
        
        ax.hist(data, bins=int(self.iterations/bin_size), density=True, alpha=0.5, label='Histogram', color='blue')
        
        ax.set_xlabel('Impact')
        ax.set_ylabel('Count')
        ax.legend()
        plt.show()

    # def run(self):


    #     project = self.get_model().get_project()
    #     var_params = self.get_var_params()
        
    #     prob_data = []
    #     impact_data = []
    #     iter = 0
    #     while iter < self.iterations:
    #         prob = 1.00
    #         for distribution in var_params:

    #             var_value = distribution.pick_data_point()
    #             prob *= distribution.prob_of(var_value) # TODO: deciding the rounding value
                
    #             obj = distribution.get_parent()

    #             method_name = 'set_'+ distribution.get_attr_name()
    #             method = getattr(obj, method_name)
    #             method(var_value)

    #         total_impact = project.get_calculator().get_total_impact(self.model.get_name(), self.impact_cat)
    #         prob_data.append(prob)
    #         impact_data.append(total_impact)
    #         iter +=1

    #     _, ax = plt.subplots()
    #     target_bin_width = 10
    #     _, bins = histogram(impact_data, bins=int(self.iterations/target_bin_width))
    #     bin_width = bins[1] - bins[0]
    #     ax.hist(impact_data, bins=int(self.iterations/target_bin_width), alpha=0.5, label='Histogram', color='blue')
    #     ax.scatter(impact_data, [prob * self.iterations * bin_width for prob in prob_data], label='Scatter Plot', alpha=0.1, color='black', edgecolor='black')
    #     ax.set_xlabel('Impact')
    #     ax.set_ylabel('Count')
    #     ax.legend()
    #     plt.show()
    #     # TODO: plot the output_data set
    #     # TODO: fix curve and get distribution params

    # #TODO Statistical analysis and variance reduction (https://onlinelibrary.wiley.com/doi/book/10.1002/9781118014967)

    def set_distributions(self):
        """Set distribution objects to all data objects in the project objects with dataset.
        """

        objects = self.model.get_all_items()

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
    
    def set_scenarios(self, dict):
        """ Set scenarios for Scenario Aware Monte Carlo Simulations.
            This will update the variable parameters.
        """

        pass # TODO: implement

    @staticmethod
    def get_groups(total, part_size):

        full_parts = total // part_size
        remainder = total % part_size
        
        parts = [part_size] * full_parts
        if remainder > 0:
            parts.append(remainder)
        
        return parts

if __name__ == '__main__':
    pass