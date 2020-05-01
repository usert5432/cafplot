"""
A collection of function to calculate statistical properties of histograms
"""

import numpy as np

def get_mean(data, weights):
    """Calculate mean of a weighted data."""
    return np.sum(data * weights)

def get_rms(data, weights):
    """Calculate RMS of a weighted data."""
    return np.sum(data**2 * weights)

def get_stdev(data, weights):
    """Calculate standard deviation of a weighted data."""
    mean = get_mean(data, weights)
    return np.sum((data - mean)**2 * weights)

def get_histogram_statistics(hist, bins, stat):
    """Calculate histogram statistical property `stat`

    Parameters
    ----------
    hist : ndarray, shape (N,)
        Histogram itself
    bins : ndarray, shape (N+1,)
        Bin edges
    stat : { 'mean', 'rms', 'stdev' }
        Type of statistic to calculate

    Returns
    -------
    float
        Value of a statistical property `stat` for the histogram `hist`
    """
    bin_centers = (bins[:-1] + bins[1:]) / 2
    density     = hist / np.sum(hist)

    if stat == 'mean':
        return get_mean(bin_centers, density)
    elif stat == 'rms':
        return get_rms(bin_centers, density)
    elif stat == 'stdev':
        return get_stdev(bin_centers, density)
    else:
        raise ValueError("Unknown statistics: %s" % (stat))

