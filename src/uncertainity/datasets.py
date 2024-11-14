from uncertainity.utils import UncertainityUtils

import scipy.stats as stats
import matplotlib.pyplot as plt


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class DataSet:
    """
    Data-set object with the corresponding distribution fitted from Scipy.stats package.

    Attributes
    ----------
    name : str.
        Name of the data set.
    data : list of floats
        The data set.
    dist_fitted : Distribution Obj.
        Distribution fitted to the data set.
    """
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.dist_fitted = None

    def find_best_fit(self, is_cts=True, fit_method='MLE', validate=True, printout=True):
        """ Find the best fit probability distribution for the data, considering the Kolmogorov–Smirnov (KS) test.

            Parameters
            ----------
            data : list
                Data to be fitted.
            is_cts : bool
                True, if the data comes from a continous variable.
            fit_methods : str
                'MLE', 'MSE'
            validate : bool
                If True, the selected fit will be checked against the critical KS parameter value.
            printout : bool
                If True, print out outcomes.

            Returns
            -------
            str
                Name of the selected distribution.
        
        """

        if is_cts:
            dists_lst = UncertainityUtils.get_all_cts_distributions()
        else:
            dists_lst = UncertainityUtils.get_all_disc_distributions()

        best_k_param = 10000
        best_fit = None
        for dist_name in dists_lst:
            try:
                dist = getattr(stats, dist_name)
                params = dist.fit(self.data, method=fit_method)
                k_test = stats.kstest(self.data, dist_name, args=params)
                print(f"{dist_name} distribution fits with a KS statistic of {k_test.statistic}. Best fit {best_fit} with KS statistic of {best_k_param}.")
            except:
                print(f"KS test failed for {dist_name} distribution.")
                continue

            if k_test.statistic < best_k_param:
                best_fit = dist_name
                best_k_param = k_test.statistic
            elif k_test.statistic < best_k_param:
                raise NotImplementedError(f"Equally best fit distributions found!! {best_fit} and {dist_name}")
                # TODO: what if multiple best fits

        if printout:
            print(f"Choosen fit {best_fit} with KS statistic of {best_k_param}")

        if validate:
            alpha = 0.05
            critical_ks_param = UncertainityUtils.get_critical_ks_param(alpha, len(self.data))
            if best_k_param < critical_ks_param:
                print(f"KS statistic fall below KS test critical values at a significance level: alpha = {alpha} => KS_crit. = {critical_ks_param}.")
                return best_fit
            else:
                print(f"KS statistic is not statistically significant.")
                return None
        else:
            return best_fit
        
    def fit_distribution(self, best_fit, fit_method='MLE'):
        """ Fit a distribution to the data set.

            Parameters
            ----------
            best_fit : str
                Name of the distribution fitted to the data set, following Scipy.stats module.
            fit_methods : str
                'MLE', 'MSE'
            
            Returns
            -------
            Distribution Obj.
                The fitted distribtuion to the data set.
        
        """

        dist = getattr(stats, best_fit)
        params  = dist.fit(self.data, method=fit_method)

        self.dist_fitted = Distribution(best_fit, params, dist)

        return self.dist_fitted

    def plot_data(self):
        """ Plot the data histogram with the  proposed distribution fit overlayed.
        """

        plt.hist(data, bins=30, density=True, alpha=0.6, color='g', label='Data') #TODO: update parameters

        plt.legend()
        plt.show()

    def plot_fit(self):
        """ Plot the data histogram with the fitted distribution overlayed. 
        """

        plt.hist(self.data, bins=30, density=True, alpha=0.6, color='g', label='Data')

        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = self.dist_fitted.dist.pdf(x, *self.dist_fitted.params)

        plt.plot(x, p, 'k', linewidth=2, label=f'Fitted {self.dist_fitted.dist_name}')

        plt.legend()
        plt.show()


class Distribution:
    """
    Distribution object.
    A wrapper for scipy.stats._continuous_distns Obj.

    Attributes
    ----------
    dist_name : str.
        Name of the distribution fitted to the data set, following Scipy.stats module.
    params : tuple
        Parameters defining the distribution fitted.
    dist : scipy.stats._continuous_distns Obj.
        Fitted distribution object from Scipy.
    """
    def __init__(self, dist_name, params, dist):
        self.dist_name = dist_name
        self.params = params
        self.dist = dist

    def pick_data_point(self):
        """ Pick a random variate from the distibution.

            Returns
            -------
            float
                A random variate from the distribution.
        """

        return self.dist.rvs(*self.params, size = 1)[0]

    def prob_of(self, x):
        """ Get the probability density at the given random variate.

            Parameters
            ----------
            x : float
                Random variate picked.

            Returns
            -------
            float
                Probability density.
        """

        return self.dist.pdf(x, *self.params)
    

if __name__ == '__main__':
    import numpy as np

    data = np.random.normal(12, 24, 100)  # Set your data set here

    dataset = DataSet('test', data)
    dataset.plot_data()
    # best_fit = dist.find_best_fit(is_cts=True, fit_method='MLE', validate=True, printout=True)
    best_fit = 'norm'
    distribution = dataset.fit_distribution(best_fit)
    dataset.plot_fit()

    x = distribution.pick_data_point()
    p = distribution.prob_of(x)
