"""
Base class for ROOT-like histograms
"""

import numpy as np
from cafplot.stats import (
    gauss_sigma_to_prob, get_poisson_confidence_interval,
    get_histogram_statistics
)

class RHist:
    """A base class for ROOT-like histograms

    Each `RHist` contains the histogram itself, bin edges and squared errors
    associated to each bin. `RHist` support basic arithmetic operations,
    and histogram scaling.

    Parameters
    ----------
    bins : list of ndarray
        List of bin edges for each dimension.
    hist : ndarray
        Numpy Histogram.
    err_sq : ndarray, optional
        Numpy histogram of squared errors associate to each bin.
        If not specified errors are assumed to be 0.
    """

    def __init__(self, bins, hist, err_sq = None):
        self._bins = bins
        self._hist = hist

        if err_sq is None:
            err_sq = np.zeros(hist.shape)

        self._err_sq = err_sq

        self._self_sanity_check()

    @property
    def bins(self):
        """ List of bin edges for each dimension """
        return self._bins

    @property
    def hist(self):
        """ Histogram data """
        return self._hist

    @property
    def err_sq(self):
        """ Squared error for each bin """
        return self._err_sq

    @property
    def ndim(self):
        """ Number of histogram dimensions """
        return len(self._bins)

    def get_error_margin(self, err = None, sigma = 1):
        """Return lower and upper error margins for the histogram.

        This function calculates lower and upper error margins for a histogram
        with confidence `sigma`.

        Parameters
        ----------
        err : { None, 'normal', 'poisson' }
            Type of the statistics to use for calculating error margin.
            Supported statistics: 'normal' and 'poisson'. By default it
            will use the 'normal' distribution.
        sigma : float
            Confidence expressed as a number of Gaussian sigmas.

        Returns
        -------
        (lower, upper) : tuple of 2 ndarray
            lower and upper error margins for the histogram
        """
        if (err is None) or (err == 'normal'):
            err = sigma * np.sqrt(self._err_sq)
            return (self._hist - err, self._hist + err)

        if err == 'poisson':
            prob = gauss_sigma_to_prob(sigma)
            return get_poisson_confidence_interval(self._hist, prob)

        raise ValueError("Unknown error type: '%s'" % (err))

    def get_stat(self, stat, axis = 0):
        """Calculate statistical property of a histogram along axis

        Parameters
        ----------
        stat : { 'mean', 'rms', 'stdev' }
            Type of statistic to calculate.
        axis : int
            Axis along which statistic will be calculated

        Returns
        -------
        float
            Value of a `stat' along axis `axis`

        See Also
        --------
        get_histogram_statistics : performs the actual calculation
        """

        if (axis >= self.ndim) or (axis < 0):
            raise RuntimeError(
                "Dimension %d exceedes histogram ndim %d" % (axis, self.ndim)
            )

        if self.ndim == 1:
            projected_hist = self._hist
        else:
            projected_hist = np.sum(
                self._hist,
                axis = (i for i in range(len(self.ndim)) if i != axis)
            )

        return get_histogram_statistics(projected_hist, self._bins[axis], stat)

    def scale(self, factor):
        """Scale histogram inplace by a `factor`."""
        self._hist   = factor * self.hist
        self._err_sq = factor**2 * self.err_sq

    def _self_sanity_check(self):
        hist_shape = self.hist.shape
        err_shape  = self.err_sq.shape

        if hist_shape != err_shape:
            raise RuntimeError(
                "Hist data shape '%s' is not equal to error shape '%s'" \
                % (hist_shape, err_shape)
            )

        for dim,bins_dim in enumerate(self.bins):
            if len(bins_dim.shape) != 1:
                raise RuntimeError(
                    "Hist bins for dimension %d have invalid shape '%s'" \
                    % (dim, bins_dim.shape)
                )

            if (hist_shape[dim] + 1) != bins_dim.shape[0]:
                raise RuntimeError(
                    "Hist bins for dimension %d incompatible with data" % (dim)
                )

    def _are_bins_compatible(self, other):
        if len(self.bins) != len(other.bins):
            return False

        for dim in range(len(self.bins)):
            if (
                   (self.bins[dim].shape != other.bins[dim].shape)
                or (any(self.bins[dim]   != other.bins[dim]))
            ):
                return False

        return True

    def _coerce_other(self, other):
        """Coerce 'other' into an `RHist` if possible.

        In case if `other is `RHist` this function verifies that two histograms
        have similar bin edges.

        If `other` is a number then it converts it into a dummy `RHist` with
        the came bin edges as `self`.
        """

        if isinstance(other, RHist):
            if not self._are_bins_compatible(other):
                raise ValueError("Histograms have incompatible binnings")
            return other

        elif isinstance(other, (int, float)):
            return RHist(self.bins, other, 0)

        else:
            RuntimeError(
                "Do not know how to handle binop of a RHist and %s." % (
                    type(other)
                )
            )

        return None

    def __add__(self, other):
        other = self._coerce_other(other)

        hist   = self.hist   + other.hist
        err_sq = self.err_sq + other.err_sq

        return type(self)(self._bins, hist, err_sq)

    def __sub__(self, other):
        other = self._coerce_other(other)

        hist   = self.hist   - other.hist
        err_sq = self.err_sq + other.err_sq

        return type(self)(self._bins, hist, err_sq)

    def __mul__(self, other):
        other = self._coerce_other(other)

        hist   = self.hist * other.hist
        err_sq = (other.hist**2 * self.err_sq + self.hist**2 * other.err_sq)

        return type(self)(self._bins, hist, err_sq)

    def __div__(self, other):
        other = self._coerce_other(other)

        hist   = self._hist / other._hist
        err_sq = (
            (1 / other.hist)**2 * self.err_sq
          + (self.hist / other.hist**2)**2  * other.err_sq
        )

        return (type(self))(self._bins, hist, err_sq)

    def __truediv__(self, other):
        return self.__div__(other)

