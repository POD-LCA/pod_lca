
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


if __name__ == '__main__':
    pass