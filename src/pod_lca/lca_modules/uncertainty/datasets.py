__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from collections import Counter

import numpy as np
import scipy.stats as stats

from .utils import UncertainityUtils
from ...utilities import log


class DataDistribution:
    """Dataset object with the corresponding distribution fitted from Scipy.stats package.
        A Dataset is a collection (list) of data points.

    Attributes
    ----------
    name : str
        Name of the data set.
    data : list of float (or str)
        The data set.
    dist_name : str
        Distribution name as used in :class:`scipy.stats`.
    dist : scipy.stats.rv_continuous or scipy.stats.rv_discrete
        Fitted distribution object from Scipy.
    parent : object
        Object to which the dataset is attached.
    attr : str
        Attribute to which dataset is attached.
    scenarios : dict
        Definition of quartile points for scenarios.
        For continous variables values are numbers between 0-1.
    is_cts : bool
        If true, the data are from a contrinous variable, otherwise a discrete variable.
    """

    CONTNS_DIST_SHORTLIST = ["norm", "expon", "uniform", "beta", "gamma", "chi2", "t", "f", "lognorm", "weibull_min"]

    def __init__(self):
        self.name = None
        self.data = None
        self.dist_name = None
        self.distribution = None
        self.attribute = None
        self.parent = None
        self.scenarios = {"low": 0.2, "med": 0.5, "high": 0.8}
        self.is_cts = None

    def __str__(self):
        string = f"Dataset has {len(self.get_data())} entries in the range {min(self.get_data()):.2f} to {max(self.get_data()):.2f}"
        if self.get_distribution() is not None:
            string += f"\nData fitted to a {self.get_dist_name()} distribution with \nmean : {self.get_distribution().mean():.2f} \nstd : {self.get_distribution().std():.2f}"

        return string

    # ================================
    # Constructors
    # ================================
    @classmethod
    def from_data(cls, data, is_cts, name="unspecified", del_data=False, set_dist=True):
        """Create a Dataset object from data input.

        Parameters
        ----------
        data : list of float
            The data set.
        name : str
            Name of the data set.
        is_cts : bool
            If true, the data are from a contrinous variable, otherwise a discrete variable.

        Returns
        -------
        ~pod_lca.uncertainty.DataDistribution
            Data distribution created.
        """
        dataset = cls()
        dataset.set_data(data)
        dataset.set_name(name)
        dataset.is_cts = is_cts

        if set_dist:
            dataset.set_distribution()

        if del_data:
            dataset.delete_data()

        return dataset

    @classmethod
    def from_distributions(cls, dist, is_cts, name="unspecified"):
        """Create a Dataset object from data input.

        Parameters
        ----------
        dist : scipy.stats.rv_continuous
            Fitted distribution object from Scipy.
        name : str
            Name of the data set.
        is_cts : bool
            If true, the data are from a contrinous variable, otherwise a discrete variable.

        Returns
        -------
        ~pod_lca.uncertainty.DataDistribution
            Data distribution created.
        """
        dataset = cls()
        dataset.set_name(name)
        dataset.set_distribution(dist)

        dataset.is_cts = is_cts

        return dataset

    # ================================
    # Setters
    # ================================
    def set_data(self, data):
        """Set data to the Data distribution.

        Parameters
        ----------
        data : list of float
            The data set.
        """
        self.data = data

        return self

    def set_name(self, name):
        """Set name to the data distribution.

        Parameters
        ----------
        name : str
            Name of the data set.
        """
        self.name = name

        return self

    def set_distribution(self, dist=None):
        """Set a distribution function to the data distribution.

        Parameters
        ----------
        dist : scipy.stats.rv_continuous or scipy.stats.rv_discrete
            Fitted distribution.

        Raises
        ------
        ValueError
            A valid distribution could not be fitted.
        """
        if dist is None:
            if self.is_cts:
                try:
                    best_fit = self.find_best_fit(is_cts=True)
                    if best_fit is not None:
                        dist, _ = self.fit_cts_distribution(best_fit, fit_method="MLE")
                        self.distribution = dist
                        self.dist_name = best_fit
                    else:
                        raise ValueError("A best-fit found could not be found.")
                except:
                    log("A valid distribution could not be fitted.", "Warn")
            else:
                self.distribution = self.generate_discrete_distribution()
                self.dist_name = self.distribution.name
        else:
            self.distribution = dist
            self.dist_name = (
                dist.dist.name
                if isinstance(self.distribution, stats._distn_infrastructure.rv_continuous_frozen)
                else dist.name
            )

        return self

    def set_parent(self, obj):
        """Set parent of the dataset.

        Parameters
        ----------
        obj : object
            Object to which the dataset correspond.
        """
        self.parent = obj

        return self

    def set_attr_name(self, attr):
        """Set attribute to which the dataset belong.

        Parameters
        ----------
        attr : str
            Attribute to which the dataset correspond.
        """
        self.attribute = attr

        return self

    def set_scenario(self, scenario_name, value):
        """Set the statistic for a given scenario.

        Parameters
        ----------
        scenario_name : {'high', 'med', 'low'}
            Scenario.
        value: float
            Scenario value given as a value between 0 and 1.
        """
        self.scenarios[scenario_name] = value

    # ================================
    # Getters
    # ================================
    def get_data(self):
        """Get data list.

        Returns
        ----------
        list of float
            The data set.
        """
        return self.data

    def get_name(self):
        """Get the name of the data distribution.

        Returns
        ----------
        str
            Name of the data distribution.
        """
        return self.name

    def get_distribution(self):
        """Get the distribution fitted to the dataset.

        Returns
        ----------
        scipy.stats.rv_continuous or scipy.stats.rv_discrete
            Fitted distribution.
        """
        return self.distribution

    def get_dist_name(self):
        """Get the name of the distribution fitted.

        Returns
        ----------
        str
            Distribution name as used in :class:`scipy.stats`.
        """
        return self.dist_name

    def get_attr(self):
        """Get the attribute to which the dataset belong.

        Returns
        -------
        str
            Attribute to which the dataset correspond.
        """
        return self.attribute

    def get_parent(self):
        """Get parent of the dataset.

        Returns
        -------
        object
            Object to which the dataset correspond.
        """
        return self.parent

    def get_scenario(self, scenario_name):
        """Get the statistic for a given scenario.

        Parameters
        ----------
        scenario_name : str
            Scenario name given as 'high', 'med', or 'low'.
        """
        return self.scenarios[scenario_name]

    # ================================
    # Delete
    # ================================
    def delete_data(self):
        """Delete data from the dataset."""
        self.data = None

        return self

    # ================================
    # Methods for fitting distributions
    # ================================
    def find_best_fit(self, is_cts=True, fit_method="MLE"):
        """Find the best fit probability distribution for the data, considering the Kolmogorov–Smirnov (KS) test.

        Parameters
        ----------
        data : list
            Data to be fitted.
        is_cts : bool
            True, if the data comes from a continous variable.
        fit_methods : {'MLE', 'MSE'}
            Best fitting method: \n
            - 'MLE' - Maximum Likelihood Estimate
            - 'MSE' - Mean Squared Error

        Returns
        -------
        str
            Name of the selected distribution.

        Raises
        ------
        NotImplementedError
            Could not discrimenate between eaqually good best-fits.
        """
        if is_cts:
            full_dists_lst = UncertainityUtils.get_all_cts_distributions()
            short_lst = DataDistribution.CONTNS_DIST_SHORTLIST
        else:
            full_dists_lst = UncertainityUtils.get_all_disc_distributions()
            short_lst = []

        best_k_param = 10000
        best_fit = None
        for dist_lst in [short_lst, full_dists_lst]:
            for dist_name in dist_lst:
                try:
                    _, params = self.fit_cts_distribution(dist_name, fit_method)
                    k_test = stats.kstest(self.data, dist_name, args=params)
                except:
                    continue

                if k_test.statistic < best_k_param:
                    if self.validate_dist_fit(dist_name, params):
                        best_fit = dist_name
                        best_k_param = k_test.statistic
                elif k_test.statistic == best_k_param:
                    raise NotImplementedError(f"Equally best fit distributions found!! {best_fit} and {dist_name}")
                    # TODO: what if multiple best fits

            if best_fit is not None:  # a best-fit is found from the short list
                return best_fit

        return best_fit

    def validate_dist_fit(self, dist_name, params):
        """Validate a distribution fitted to a dataset.

        Parameters
        ----------
        dist_name : str
            Distribution name as used in :class:`scipy.stats`.
        params : tuple
            Parameters corresponding to the fit.

        Returns
        -------
        bool
            True if validated, otherwise False.
        """
        alpha = 0.05
        critical_ks_param = UncertainityUtils.get_critical_ks_param(alpha, len(self.data))

        k_test = stats.kstest(self.data, dist_name, args=params)
        k_param = k_test.statistic
        if k_param < critical_ks_param:
            return True
        else:
            return False

    def fit_cts_distribution(self, dist_fit, fit_method="MLE"):
        """Fit a distribution to the data.

        Parameters
        ----------
        dist_fit : str
            Name of the distribution fitted to the data set, following Scipy.stats module.
        fit_methods : {'MLE', 'MSE'}
            Best fitting method: \n
            - 'MLE' - Maximum Likelihood Estimate
            - 'MSE' - Mean Squared Error

        Returns
        -------
        :class:`scipy.stats.rv_continuous`
            The fitted distribtuion to the data set.
        :class:`tuple`
            Parameters of the fitted distribution.
        """
        dist_tmp = getattr(stats, dist_fit)
        params = dist_tmp.fit(self.data, method=fit_method)
        dist = dist_tmp(*params)

        return dist, params

    def generate_discrete_distribution(self):
        """Generate a discrete distribution from the data.

        Returns
        -------
        scipy.stats.rv_discrete
            Scipy discrete distribution.
        """
        freq = Counter(self.data)

        xk = np.array(list(freq.keys()))
        pk = np.array(list(freq.values())) / len(self.data)

        return stats.rv_discrete(name="from_data", values=(xk, pk))

    # ================================
    # Methods on distributions
    # ================================
    def pick_data_point_from_distribution(self):
        """Pick a random variate from the distibution.

        Returns
        -------
        float or str
            A random variate from the distribution.
        """
        return self.distribution.rvs(size=1)[0]

    def pick_data_points_from_distribution(self, n):
        """Pick a random variate from the distibution.

        Parameters
        ----------
        n : int
            Number of points to pick.

        Returns
        -------
        list
            A list of random variates from the distribution.
        """
        if self.is_cts:
            return self.distribution.rvs(size=n)
        else:
            if self.distribution.xk.dtype == np.int32:
                return self.distribution.rvs(size=n)
            else:
                xk, pk = self.distribution.xk, self.distribution.pk
                dist_tmp = stats.rv_discrete(name="custm", values=(np.arange(len(xk)), pk))
                inidces = dist_tmp.rvs(size=n)

                return [xk[idx] for idx in inidces]

    def prob_of(self, x):
        """Get the probability density at the given random variate.

        Parameters
        ----------
        x : float
            Random variate picked.

        Returns
        -------
        float
            Probability density.
        """
        if self.is_cts:
            return self.distribution.pdf(x)
            # return self.dist.cdf(x+0.5) - self.dist.cdf(x-0.5) # FIXME: Probability density to probability
        else:
            return self.distribution.pmf(x)

    def percentile(self, p):
        """Get the percentile of the distribution.

        Parameters
        ----------
        p : float
            Percentile to be calculated.

        Returns
        -------
        float
            Percentile of the distribution.
        """
        if self.is_cts:
            return self.distribution.ppf(p)
        else:
            return self.distribution.ppf(p)

    def discrete_from_continous(self, start, range, step, integrate_point="left"):
        """Create a discrete data set from the continous distribution.

        Parameters
        ----------
        start : float
            Starting value of the discrete data set.
        range : float
            Range of the data set.
        step : float
            Step of the discrete data series.
        integrate_point : {'left', 'middle', 'right'}
            Point to which the data is grouped.

        Returns
        -------
        numpy.ndarray
            Discrete sequence of data.

        Raises
        ------
        ValueError
            Integrate point not recognized.
        """
        t = np.arange(start, start + range + step, step)
        if t[-1] > start + range:
            t = np.delete(t, -1)
        if integrate_point == "left":
            interval_starts = t
            interval_ends = t + step
        elif integrate_point == "middle":
            interval_starts = t - step / 2
            interval_ends = t + step / 2
        elif integrate_point == "right":
            interval_starts = t - step
            interval_ends = t
        else:
            raise ValueError("Integrate point not recognized.")

        if self.is_cts:
            return t, np.asarray(self.distribution.cdf(interval_ends) - self.distribution.cdf(interval_starts))


if __name__ == "__main__":
    pass
