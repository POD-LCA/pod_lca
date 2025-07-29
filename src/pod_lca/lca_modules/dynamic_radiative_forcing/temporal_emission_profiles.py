
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from math import exp

from numpy import log
from numpy import where
from scipy import stats
from scipy import optimize

from ..uncertainty import DataDistribution
from ..uncertainty import ExponentDecay 
from ..uncertainty import LogNorm 
from ..uncertainty import Norm 
from ..uncertainty import Uniform 


class TemporalEmissionProfiles(DataDistribution):
    """ Temporal emission profiles for the purpose of calculating dynamic radiative forcing.

    Attributes
    ----------
    start : int or float
        starting point of the temporal emission profile.
    duration : int or float
        Duration of the temporal emission profile.
    """

    def __init__(self):
        super().__init__()
        self.start = None
        self.duration = None

    # ================================
    # Setters
    # ================================
    def set_start(self, start):
        """ Set the starting point of the temporal emission profile.
        
        Parameters
        ----------
        start : int or float
            starting point of the temporal emission profile.
        """
        self.start = start

        return self
    
    def set_duration(self, duration):
        """ Set the duration of the temporal emission profile.
        
        Parameters
        ----------
        duration : int or float
            Duration of the temporal emission profile.
        """        
        self.duration = duration

    # ================================
    # Getters
    # ================================
    def get_start(self):
        """ Get the starting point of the temporal emission profile.
        
        Returns
        -------
        int or float
            starting point of the temporal emission profile.
        """
        return self.start
    
    def get_duration(self):
        """ Get the duration of the temporal emission profile.
        
        Returns
        -------
        int or float
            starting point of the temporal emission profile.
        """        
        return self.duration

    # ================================
    # Methods on distributions
    # ================================
    def discrete_from_continous(self, start, range, step, integrate_point='left', cutoff=True, unitize=True):
        """ Create a discrete data set from the continous distribution.

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
        cutoff : bool
            Set distribution values before and after the range to zero.

        Returns
        -------
        numpy.ndarray
            Discrete sequence of data.
        """
        t, record = super().discrete_from_continous(start, range, step, integrate_point)

        if cutoff:
            if self.get_start() is not None:
                before_ids = where(t < self.get_start() - step/2)[0]
                record[before_ids] = 0.0
            if self.get_duration() is not None:
                after_ids = where(t > (self.get_start() + self.get_duration() + step/2))[0]
                record[after_ids] = 0.0

        if unitize:
            record /=sum(record)

        return t, record
        
        
class UniformEmissionProfile(TemporalEmissionProfiles, Uniform):
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
        uniform = super().from_params(start, step, name)

        uniform.set_start(start)
        uniform.set_duration(step)

        return uniform

    @classmethod
    def unit_pulse(cls, at, name='unspecified'):
        """ Create unit pulse at specified point.
        
        Parameters
        ----------
        at : int or float
            Point where the unit pulse occurs
        name : str
            Name of the data distribution.
        """
        pulse = cls.from_params(start=at, step=0.001, name=name)
        pulse.dist_name = 'pulse'

        pulse.set_start(at)

        return pulse
    

class NormEmissionProfile(TemporalEmissionProfiles, Norm):
    """ A normal data distribution.
    """

    @classmethod
    def from_range(cls, start, range, area_covered=0.999, name='unspecified'):
        """ Create a normal distribution from start and range specified. 
            The distribution is fitted so that area under the curve within [start, start + range] is greater than specified.
        
        Parameters
        ----------
        start : int or float
            Start value of the range.
        range : int or float
            Range of the variable to cover the distribution.
        area_covered : flat
            Percentage of area under the curve covered within the range.
        name : str
            Name of the data distribution.
        """
        mean = start + (range / 2)
        std_dev = range / (2 * stats.norm.ppf(area_covered))

        norm = cls.from_params(mean, std_dev, name)
        norm.set_start(start)
        norm.set_duration(range)

        return norm


class LogNormEmissionProfile(TemporalEmissionProfiles, LogNorm):
    """ A log-normal data distribution.
    """

    @classmethod
    def from_range(cls, start, range, area_covered=0.999, name='unspecified'):
        """ Create a log-normal distribution from start and range specified. 
            The distribution is fitted so that area under the curve within [start, start + range] is closer to specified.
        
        Parameters
        ----------
        start : int or float
            Start value of the range.
        range : int or float
            Range of the variable to cover the distribution.
        area_covered : flat
            Percentage of area under the curve covered within the range.
        name : str
            Name of the data distribution.
        """
        optim_stdev_result = optimize.minimize_scalar(lambda phi: abs(
                                                                        stats.lognorm(s=phi, loc=start, scale=(range / 2)).cdf(start + range) * 100 
                                                                        - stats.lognorm(s=phi, loc=start, scale=(range / 2)).cdf(start) * 100
                                                                        - area_covered * 100
                                                                    ),
                                                    bounds=(0.01, 2),
                                                    method='bounded'
                                                    )
        
        if optim_stdev_result.success:
            lognorm = cls.from_params(mean=log(range/2), std_dev=optim_stdev_result.x, start=start, name=name)
            lognorm.set_start(start)
            lognorm.set_duration(range)

            return lognorm
        else:
            raise RuntimeError("Parameter could not be determined")

class ExponentDecayEmissionProfile(TemporalEmissionProfiles, ExponentDecay):
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
        expon = super().from_params(start, decay_rate, name)
        expon.set_start(start)

        return expon
    
    @classmethod
    def from_range(cls, start, range, area_covered=0.85, name='unspecified'):
        """ Create a exponential decay from start and range specified. 
            The distribution is fitted so that area under the curve within [start, start + range] is closer to specified.
        
        Parameters
        ----------
        start : int or float
            Start value of the range.
        range : int or float
            Range of the variable to cover the distribution.
        area_covered : flat
            Percentage of area under the curve covered within the range.
        name : str
            Name of the data distribution.
        """ 
        optim_decay_rate_result = optimize.minimize_scalar(lambda lmbda: exp(-lmbda * start) * (1 - exp(-lmbda * range)) - area_covered,
                                                       bracket=(0.01, 2 * log(1 / (1 - area_covered)) / range),
                                                       method='brent')        
        
        if optim_decay_rate_result.success:
            expon = cls.from_params(start, optim_decay_rate_result.x, name)
            expon.set_start(start)
            expon.set_duration(range)

            return expon
        else:
            raise RuntimeError("Parameter could not be determined")


if __name__ == '__main__':
    pass
