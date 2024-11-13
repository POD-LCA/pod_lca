
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np


__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class UncertainityUtils:

    def get_all_cts_distributions():
        """ Get all constinous probability distributions in the scipy.stats module."""

        return [d for d in dir(stats) if isinstance(getattr(stats, d), stats.rv_continuous)]
    
    def get_all_disc_distributions():
        """ Get all discrtete probability distributions in the scipy.stats module."""

        return [d for d in dir(stats) if isinstance(getattr(stats, d), stats.rv_discrete)]

    def find_best_fit(data, is_cts=True, fit_method='MLE', validate=True, printout=True):
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

        min_data_points = 4 # fitting done only if the data set has atleast this many data points

        if is_cts:
            dists_lst = UncertainityUtils.get_all_cts_distributions()
        else:
            dists_lst = UncertainityUtils.get_all_disc_distributions()

        best_k_param = 10000
        best_fit = None
        if len(data) >= min_data_points:
            for dist_name in dists_lst:
                try:
                    k_test = stats.kstest(data, dist_name, method=fit_method)
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
            critical_ks_param = UncertainityUtils.get_critical_ks_param(alpha, len(data))
            if best_k_param < critical_ks_param:
                print(f"KS statistic fall below KS test critical values at a significance level: alpha = {alpha} => KS_crit. = {critical_ks_param}.")
                return best_fit
            else:
                print(f"KS statistic is not statistically significant.")
                return None
        else:
            return best_fit

    def get_critical_ks_param(alpha, n):
        """ Get the KS test critical value at a significance level alpha.
         
            Parameters
            ----------
            alpha : float
                Significance level at critical value.
            n : int
                Sample size.

            Returns
            -------
            float
                KS test critical value, at the significance level specified.        

        """

        return stats.ksone.ppf(1 - alpha / 2, n)

    def plot_QQ(data, dist_name):
        """ Plot the Q-Q plot comparing the data with the proposed fit.
        
            Parameters
            ----------
            data : list
                Data to be fitted.
            dist : str
                Name of the selected distribution.           
        
        """

        stats.probplot(data, dist=dist_name, plot=plt)
        plt.title(f"Q-Q Plot (distribution: {dist_name})")
        plt.show()

    def plot_fit(data, dist_name):
        """ Plot the data histogram with the  proposed distribution fit overlayed.
        
            Parameters
            ----------
            data : list
                Data to be fitted.
            dist : str
                Name of the selected distribution.           
        
        """

        plt.hist(data, bins=30, density=True, alpha=0.6, color='g', label='Data')

        dist = getattr(stats, dist_name)
        params  = dist.fit(data)
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = dist.pdf(x, *params)

        plt.plot(x, p, 'k', linewidth=2, label=f'Fitted {dist_name}')

        plt.legend()
        plt.show()


if __name__ == '__main__':
    
    data = np.random.normal(0, 1, 100)  # Set your data set here

    dist_name = UncertainityUtils.find_best_fit(data, is_cts=True, fit_method='MLE', validate=True, printout=True)

    UncertainityUtils.plot_QQ(data, dist_name)
    UncertainityUtils.plot_fit(data, dist_name)
