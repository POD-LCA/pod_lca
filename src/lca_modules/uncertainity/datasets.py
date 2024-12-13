from lca_modules.uncertainity.utils import UncertainityUtils

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class DataSet:
    """
    Dataset object with the corresponding distribution fitted from Scipy.stats package.
    A Dataset is a collection (list) of data points.

    Attributes
    ----------
    name : str.
        Name of the data set.
    data : list of floats
        The data set.
    dist_fitted : Distribution Obj.
        Distribution fitted to the data set.
    parent : Object.
        Object to which the dataset is attached.
    attr : str
        Attribute to which dataset is attached.
    """
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.dist_fitted = None
        self.parent = None
        self.attr = None

    def set_parent(self, obj):
        """ Set parent of the dataset.

            Parameters
            ----------
            obj : Master Obj.
                Object to which the dataset correspond.
        """ 

        self.parent = obj   

    def set_attr(self, attr):
        """ Set parent of the dataset.

            Parameters
            ----------
            attr : str.
                Attribute to which the dataset correspond.
        """ 

        self.attr = attr

    def get_data(self):

        return self.data

    def get_dist_fitted(self):
        """ Get the distribution fitted to the dataset.
        """

        return self.dist_fitted      

    def find_best_fit(self, is_cts=True, fit_method='MLE', validate=True, short_list=None, printout=True):
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
            short_list : list of str.
                A short list of distributions to considered for best-fit.
            printout : bool
                If True, print out outcomes.

            Returns
            -------
            str
                Name of the selected distribution.
        
        """

        if short_list is None:
            if is_cts:
                dists_lst = UncertainityUtils.get_all_cts_distributions() 
            else:
                dists_lst = UncertainityUtils.get_all_disc_distributions()
        else:
            dists_lst = short_list

        best_k_param = 10000
        best_fit = None
        for dist_name in dists_lst:
            try:
                _, params = self.fit_distribution(dist_name, fit_method)
                k_test = stats.kstest(self.data, dist_name, args=params)
            except:
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
                if printout:
                    print(f"KS statistic fall below KS test critical values at a significance level: alpha = {alpha} => KS_crit. = {critical_ks_param}.")
                return best_fit
            else:
                if printout:
                    print(f"KS statistic is not statistically significant.")
                return None
        else:
            return best_fit
        
    def fit_distribution(self, dist_fit, fit_method='MLE'):
        """ Fit a distribution to the data.

            Parameters
            ----------
            dist_fit : str
                Name of the distribution fitted to the data set, following Scipy.stats module.
            fit_methods : str
                'MLE', 'MSE'
            
            Returns
            -------
            scipy.stats._continuous_distns Obj.
                The fitted distribtuion to the data set.
            tuple
                Parameters of the fitted distribution.
        
        """

        dist_tmp = getattr(stats, dist_fit)
        params  = dist_tmp.fit(self.data, method=fit_method)
        dist = dist_tmp(*params)

        return dist, params
            
    def set_distribution(self, best_fit, fit_method='MLE'):
        """ Set a Distribution Obj to the DataSet Obj.

            Parameters
            ----------
            best_fit : str
                Name of the distribution set to the data set, following Scipy.stats module.
            fit_methods : str
                'MLE', 'MSE'
            
            Returns
            -------
            Distribution Obj.
                The fitted distribtuion to the data set.
        
        """

        dist, params = self.fit_distribution(best_fit, fit_method)
        self.dist_fitted = Distribution(best_fit, params, dist)

        return self.dist_fitted

    def plot_data(self):
        """ Plot the data histogram with the  proposed distribution fit overlayed.
        """

        plt.hist(self.data, bins=30, density=True, alpha=0.6, color='g', label='Data') #TODO: update parameters

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
    dist : scipy.stats._distn_infrastructure.rv_continuous_frozen Obj.
        Fitted distribution object from Scipy.
    parent : Object.
        Object to which the dataset is attached.
    attr : str
        Attribute to which dataset is attached.
    """
    def __init__(self, dist_name, params, dist):
        self.dist_name = dist_name
        self.params = params
        self.dist = dist
        self.parent = None
        self.attr = None

    def set_parent(self, obj):
        """ Set parent of the distribution.

            Parameters
            ----------
            obj : Master Obj.
                Object to which the distribution correspond.
        """ 

        self.parent = obj   

    def set_attr_name(self, attr):
        """ Set parent of the distribution.

            Parameters
            ----------
            attr : str.
                Attribute to which the distribution correspond.
        """ 

        self.attr = attr   

    def get_parent(self):
        """ Return the parent object.

            Returns
            -------
            Master Obj.
                Parent object of the distribution.
        """ 

        return self.parent

    def get_attr_name(self):
        """ Get the name of the corresponding attribute.

            Returns
            -------
            str.
                Namw of the attribute.
        """ 

        return self.attr  
    
    def get_dist_name(self):

        return self.dist_name

    def pick_data_point(self):
        """ Pick a random variate from the distibution.

            Returns
            -------
            float
                A random variate from the distribution.
        """

        return self.dist.rvs(size=1)[0]

    def pick_data_points(self, n):
        """ Pick a random variate from the distibution.

            Parameters
            ----------
            n : int
                Number of points to pick

            Returns
            -------
            float
                A random variate from the distribution.
        """

        return self.dist.rvs(size=n)
    
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

        return self.dist.pdf(x)
        # return self.dist.cdf(x+0.5) - self.dist.cdf(x-0.5) # FIXME: Probability density to probability
    
    # TODO create discrete distributions
    

if __name__ == '__main__':
    pass
