"""
This module defines FSurface corresponding to the CAFAna FrequentistSurface
"""

import scipy.stats as ss

from cafplot.stats import gauss_sigma_to_prob
from .surface import Surface

class FSurface(Surface):
    """A Surface subclass corresponding to the FrequentistSurface in CAFAna

    Each point of the surface is assumed to represent a Log-Likelihood
    for x,y coordinates to assume given values.
    """

    def level(self, sigma = 1, best_value = None):
        """Calculate surface level corresponding to `sigma` significance.

        This function finds a surface level such that the probability of point
        drawn from the $\\chi^2$ distribution with 2 degrees of freedom to lie
        below that level is given by Gaussian `sigma`.

        Parameters
        ----------
        sigma : float, optional
            Probability expressed as a number of Gaussian sigmas. Default: 1.
        best_value : float or None, optional
            If `best_value` is not None, then shift resulting surface level
            `best_value` - `self.best_value`. Default: None.

        Returns
        -------
        float
            Surface level.
        """
        prob = gauss_sigma_to_prob(sigma)

        result = ss.chi2.isf(1 - prob, 2)

        if best_value is not None:
            result += best_value - self.best_value

        return result

