"""
This module contains class definition for the 2D ROOT-like histogram.
"""

import numpy as np
from .rhist import RHist

class RHist2D(RHist):
    """A 2D ROOT-like histogram"""

    @staticmethod
    def from_data(
        data_x, data_y, bins_x, bins_y, weights = None,
        range_x = None, range_y = None
    ):
        """Constructs a `RHist2D` from the data.

        Parameters
        ----------
        data_x : ndarray, shape (N,)
            First coordinates of the data points to be binned.
        data_y : ndarray, shape (N,)
            Second coordinates of the data points to be binned.
        bins_x : list of float or int
            List of bin edges for the first dimension.
            If `bins` is an int, then the bin edges are calculated by splitting
            `range` into `bins` equal segments.
        bins_y : list of float or int
            List of bins edges for the second dimension (c.f. `bins_x`)
        weights : ndarray, shape (N,), optional
            Weights associated to each data point. By default all data points
            are weighted with equal weight of 1.
        range_x : tuple of 2 floats, optional
            Range (low, high) for the bins in the first dimension.
        range_y : tuple of 2 floats, optional
            Range (low, high) for the bins in the second dimension.

        Returns
        -------
        RHist2D
            A ROOT-like 2D histogram built from the `data_x`, `data_y`.
        """
        # pylint: disable=redefined-builtin
        hist, bins_x, bins_y = np.histogram2d(
            data_x, data_y, bins = [bins_x, bins_y], weights = weights,
            range = [range_x, range_y]
        )
        bins = [bins_x, bins_y]

        if weights is None:
            w_sq = None
        else:
            w_sq = weights**2

        err_sq, _ = np.histogram(data_x, data_y, bins, weights = w_sq)

        return RHist2D(bins, hist, err_sq)

    @property
    def bins_x(self):
        """ Bin edges for the first dimension """
        return self._bins[0]

    @property
    def bins_y(self):
        """ Bin edges for the second dimension """
        return self._bins[1]

