"""
This module contains functions for working with statistical distributions.
"""

import scipy.stats as ss

def gauss_sigma_to_prob(sigma):
    """Convert significance in terms of Gaussian sigma to probability.

    Examples
    --------
    >>> gauss_sigma_to_prob(1)
    0.68...
    >>> gauss_sigma_to_prob(2)
    0.95...
    """

    return ss.norm.cdf(sigma, 0, 1) - ss.norm.cdf(-sigma, 0, 1)

def get_poisson_confidence_interval(x, prob):
    """Return Poisson confidence interval.

    This function returns confidence interval with `prob` significance for the
    mean of the Poisson distribution based on an observation `x`.
    The expression is taken from [1]_.

    References
    ----------
    [1] https://en.wikipedia.org/wiki/Poisson_distribution#Confidence_interval
    """

    if x == 0:
        low = 0
    else:
        low = ss.gamma.isf(1 - prob/2, x)

    high = ss.gamma.isf(prob/2, x + 1)

    return (low, high)

