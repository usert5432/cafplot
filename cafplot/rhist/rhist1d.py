"""
This module contains class definition for the 1D ROOT-like histogram.
"""

import numpy as np
from .rhist import RHist

class RHist1D(RHist):
    """A 1D ROOT-like histogram"""

    @staticmethod
    def from_data(data, bins, weights = None, range = None):
        """Constructs a `RHist1D` from the data.

        Parameters
        ----------
        data : ndarray, shape (N,)
            Dataset to be binned
        bins : list of float or int
            List of bin edges. if `bins` is an int, then the bin edges are
            calculated by splitting `range` into `bins` equal segments.
        weights : ndarray, shape (N,), optional
            Weights associated to each data point. By default all data points
            are weighted with equal weight of 1.
        range : tuple of 2 floats, optional
            Range (low, high) for the bins.

        Returns
        -------
        RHist1D
            A ROOT-like histogram built from the `data`.
        """
        # pylint: disable=redefined-builtin

        hist, bins = np.histogram(
            data, bins = bins, weights = weights, range = range
        )

        if weights is None:
            w_sq = None
        else:
            w_sq = weights**2

        err_sq, _ = np.histogram(
            data, bins = bins, weights = w_sq, range = range
        )

        return RHist1D([bins,], hist, err_sq)

    @property
    def bins_x(self):
        """ Bin edges """
        return self.bins[0]

