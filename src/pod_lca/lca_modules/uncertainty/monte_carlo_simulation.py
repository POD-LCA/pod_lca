
from lca_modules.material.calculator import Calculator
from lca_modules.uncertainty.datasets import DataDistribution
from lca_modules.uncertainty.utils import UncertainityUtils

import time


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
        Model on which the Monte Carlo Simulation is performed.
    iterations : int
        No of iterations.
    impact_cat : str.
        Impact category considered for the impact calculation.
    var_param : List
        List of Distribution objects.
    scenario : dict.
        Dictionary of objects and the scenario set to them---{object (Master Obj): scenario (str)}
        Scenario values are 'low', 'med', and 'high'.
    result : result Obj.
        Data from the Monte Carlo Simulation

    """
    def __init__(self):
        self.model = None
        self.iterations = None
        self.impact_cat = None
        self.var_params = []
        self.scenario = {}

        self.run_time = None
        self.result = None

    def __str__(self):
        """ Print results of the Monte Carlo Simulation."""

        str = "*"*50 + "\nMONTE CARLO SIMULATION\n" + "*"*50 + "\n"
        str += f"number of iterations: {self.get_iterations()}\n"
        str += f"impact category considered: {self.get_impact_cat()}\n"
        str += f"CPU time (s): {self.run_time:.2f}\n"

        data = self.result.get_data()
        if max(data) - min(data) == 0.0:
            str += f"Single point of data at {max(data)}"
        else:
            str += f"{self.get_result()}\n"

        return str

    # ================================
    # Constructors
    # ================================  
    @classmethod
    def from_model(cls, model, no_iter=10000, impact_cat='GWP'):
        """ Create a Monte Carlo Simulator for a model.
        
            Attributes
            ----------
            model : Model Obj.
                Model on which the Monte Carlo Simulation is performed.
            
        """
        monte_carlo_simulator = cls()
        monte_carlo_simulator.set_model(model)
        monte_carlo_simulator.set_iterations(no_iter)
        monte_carlo_simulator.set_impact_cat(impact_cat)

        monte_carlo_simulator.set_var_params()
        
        return monte_carlo_simulator

    # ================================
    # Setters
    # ================================    
    def set_model(self, model):
        """ Set a model to the Simulator.
        
            Attributes
            ----------
            model : Model Obj.
                Model on which the Monte Carlo Simulation is performed.        
        
        """

        self.model = model

    def set_iterations(self, no_iters):
        """ Set the number of iterations of the simulation.
        
            Attributes
            ----------
            no_iters : int.
                Number of iterations of the simulations.        
        
        """

        self.iterations = no_iters

    def set_impact_cat(self, impact_cat):
        """ Set the impact category considered for the simulation.
        
            Attributes
            ----------
            impact_cat : str.
                Impact category considered for the impact calculation.    
        
        """

        self.impact_cat = impact_cat

    def set_var_params(self, params=None, set_all=True):
        """Find and set the variable parameters within the model.

            Parameters
            ----------
            params : list
                List of distributions to be considered in the MCS.
            set_all : bool
                If true, set all the parameters in the model with a distribution.
        """
        if params is not None:
            self.var_params = params
        elif set_all and params is None:
            objects = self.model.get_all_items()
            for object in objects:
                self.var_params.extend(list(object.get_data_distributions().values()))    
        else:
            raise NotImplementedError

        return self.var_params
    
    def set_scenario(self, dict):
        """ Set scenarios for a simulation.
        
            Parameters
            ----------
            scenario : dict.
                Dictionary of objects and the scenario set to them---{object (Master Obj): scenario (str)}
                Scenario values are 'low', 'med', and 'high'.
        
        """

        self.scenario = dict

    def set_result(self, results, is_cts):
        """ Sets the results of the Monte Carlo Simulation.
        
            Parameters
            ----------
            results : list of float
                A list of impact data from each iteration of the simulation.
            is_cts : bool
                True, if the results are in a continous scale.
        
        """

        self.result = MonteCarlo_results.from_data(results, name='MonteCarloSimualation', is_cts=is_cts, set_dist=False)

    # ================================
    # Getters
    # ================================
    def get_model(self):
        """ Get the model for which the simulation will be run.
        
            Returns
            ----------
            Model Obj.
                Model on which the Monte Carlo Simulation is performed.        
        
        """
        return self.model
    
    def get_iterations(self):
        """ Get the number of iterations of the simulation.
        
            Returns
            ----------
            int.
                Number of iterations of the simulations.        
        
        """
        return self.iterations
    
    def get_impact_cat(self):
        """ Get the impact category considered for the simulation.
        
            Returns
            ----------
            str.
                Impact category considered for the impact calculation.    
        
        """
        return self.impact_cat

    def get_var_params(self):
        """Get variable parameters within the model.
        """

        return self.var_params
    
    def get_scenario(self):
        """ Get scenarios set for the simulation.
        
            Returns
            ----------
            dict.
                Dictionary of objects and the scenario set to them---{object (Master Obj): scenario (str)}
                Scenario values are 'low', 'med', and 'high'.
        
        """
        return self.scenario

    def get_result(self):
        """ Sets the results of the Monte Carlo Simulation.
        
            Returns
            ----------
            MonteCarlo_reults Obj.
                Data from the Monte Carlo Simulation.
        
        """
        return self.result

    # ================================
    # Methods
    # ================================    
    def run(self):
        """ Run a Monte Carlo Simulation.
        """
        

        var_params_tmp = self.get_var_params()
        scenarios = self.get_scenario()

        is_cts = False
        var_params = []
        methods_list = {}
        for distribution in var_params_tmp:
            obj = distribution.get_parent()
            if obj in scenarios:
                method_name = 'set_'+ distribution.get_attr()
                method_obj = getattr(obj, method_name)
                value = distribution.get_distribution().ppf(distribution.get_scenario(scenarios[obj]))
                method_obj(value)
            else:
                var_params.append(distribution)
                method_name = 'set_'+ distribution.get_attr()
                methods_list[distribution] = getattr(obj, method_name)

            if distribution.is_cts:
                is_cts =True

        start = time.time()
        result = []
        for iter_in_group in UncertainityUtils.get_groups(self.iterations, 1000):
            var_values = {}
            for distribution in var_params:
                var_values[distribution] = distribution.pick_data_points_from_distribution(iter_in_group)

            iter = 0        
            while iter < iter_in_group:
                for distribution in var_params:        
                    methods_list[distribution](var_values[distribution][iter])

                total_impact = Calculator.get_total_impact(self.model, self.impact_cat)
                result.append(total_impact)
                iter +=1

        elapsed = time.time() - start
        self.run_time = elapsed

        self.set_result(result, is_cts)

        return result
    
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

    def update_all_distributions(self):
        """Set distribution objects to all data objects in the project objects with dataset.
        """
        objects = self.model.get_all_items()

        for object in objects:
            for dataset in object.get_data_distributions().values():
                if dataset.get_distribution() is None:
                    dataset.set_distribution()               

class MonteCarlo_results(DataDistribution):

    def __init__(self):
        super().__init__()

    def __str__(self):
        str = f"Generated {len(self.get_data())} models giving impact values in the range {min(self.get_data()):.2f} to {max(self.get_data()):.2f}"
        if  self.get_distribution() is not None:             
            str += f"\nData fitted to a {self.get_dist_name()} distribution with \nmean : {self.get_distribution().mean():.2f} \nstd : {self.get_distribution().std():.2f}" 

        return str


if __name__ == '__main__':
    pass