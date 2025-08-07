
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from math import exp

from scipy import stats

from . import DataDistribution


class Uniform(DataDistribution):
    """ A uniform data distribution.
    """

    @classmethod
    def from_params(cls, start, step, name='unspecified'):
        """ Create a uniform distribution from parameters specified.
        
        Parameters
        ----------
        start : int or float
            Starting point of uniform distribution.
        step : int or float
            Width of the distributions (distribution ends at start + step).
        name : str
            Name of the data distribution.
        """
        dist = stats.uniform(loc=start, scale=step)
        uniform = super().from_distributions(dist, is_cts=True, name=name)
        uniform.dist_name = 'uniform'

        return uniform
    

class Norm(DataDistribution):
    """ A normal data distribution.
    """

    @classmethod
    def from_params(cls, mean, std_dev, name='unspecified'):
        """ Create a normal distribution from parameters (mean and standard deviation) specified.
        
        Parameters
        ----------
        mean : int or float
            Mean of the normal distribution.
        std_dev : int or float
            Standard deviation of the normal distribution.
        name : str
            Name of the data distribution.
        """
        dist = stats.norm(loc=mean, scale=std_dev)
        norm = super().from_distributions(dist, is_cts=True, name=name)
        norm.dist_name = 'norm'

        return norm


class LogNorm(DataDistribution):
    """ A log-normal data distribution.
    """

    @classmethod
    def from_params(cls, mean, std_dev, start, name='unspecified'):
        """ Create a log-normal distribution from parameters specified. Parameters specified are the mean and standard deviation of the corresponding normal distribution, and the starting point of the log-normal distribution.
        
        Parameters
        ----------
        mean : int or float
            Mean of the corresponding normal distribution, relative to start of the log-normal distribution.
        std_dev : int or float
            Standard deviation of the corresponding normal distribution.
        start : int or float
            Starting point of the log-normal distribution.
        name : str
            Name of the data distribution.
        """
        dist = stats.lognorm(s=std_dev, loc=start, scale=exp(mean))
        lognorm = super().from_distributions(dist, is_cts=True, name=name)
        lognorm.dist_name = 'lognorm'

        return lognorm
    

class ExponentDecay(DataDistribution):
    """ A exponential decay distribution.
    """

    @classmethod
    def from_params(cls, start, decay_rate, name='unspecified'):
        """ Create a exponential distribution from parameters specified.
        
        Parameters
        ----------
        start : int or float
            Starting point of the exponential decay function.
        decay_rate : int or float
            Decay rate of the exponential function.
        name : str
            Name of the data distribution.
        """
        dist = stats.expon(loc=start, scale=decay_rate) 
        expon = super().from_distributions(dist, is_cts=True, name=name)
        expon.dist_name = 'expon'

        return expon


if __name__ == '__main__':
    pass
