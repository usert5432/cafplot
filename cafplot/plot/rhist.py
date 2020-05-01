"""
Functions to plot RHist histograms
"""

from .nphist import (
    plot_nphist1d, plot_nphist1d_error, plot_nphist2d, plot_nphist2d_contour
)

def plot_rhist1d(ax, rhist, label, histtype = None, marker = None, **kwargs):
    """Plot one dimensional RHist1D histogram.

    This is a wrapper around `plot_nphist1d` function.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes on which histogram will be plotted.
    rhist : Rhist1D
        Histogram to be plotted.
    histtype : { 'line', 'step', 'bar' } or None, optional
        Histogram style. None by default.
    marker : str or None, optional
        If not None this function will add markers on top of histogram bins.
        c.f. help(matplotlib.pyplot.scatter).
    kwargs : dict, optional
        Additional parameters to pass directly to the matplotlib plotting funcs
    """

    plot_nphist1d(
        ax, rhist.hist, rhist.bins_x, label, histtype, marker, **kwargs
    )

def plot_rhist1d_error(
    ax, rhist, err_type = 'bar', err = None, sigma = 1, **kwargs
):
    """Plot error bars for one dimensional RHist1D histogram

    Parameters
    ----------
    ax : Axes
        Matplotlib axes on which histogram will be plotted.
    rhist : Rhist1D
        Histogram to be plotted.
    err_type : { 'bar', 'margin' } or None
        Error bar style.
    err : { None, 'normal', 'poisson' }
        Type of the statistics to use for calculating error margin.
        c.f. `RHist.get_error_margin`
    sigma : float
        Confidence expressed as a number of Gaussian sigmas
        c.f. `RHist.get_error_margin`
    kwargs : dict, optional
        Additional parameters to pass directly to the matplotlib plotting funcs
        c.f. `plot_nphist1d_error`
    """

    hist_down, hist_up = rhist.get_error_margin(err, sigma)

    plot_nphist1d_error(
        ax, hist_down, hist_up, rhist.bins_x, err_type, **kwargs
    )

def plot_rhist2d(ax, rhist, **kwargs):
    """Draw a two dimensional RHist2D histogram as an image.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes on which histogram will be plotted.
    rhist : RHist2D
        Histogram to be plotted.
    kwargs : dict, optional
        Additional parameters to pass directly to the matplotlib
        NonUniformImage function

    Returns
    -------
    NonUniformImage
        Matplotlib NonUniformImage that depicts `rhist`.
    """

    return plot_nphist2d(ax, rhist.hist, rhist.bins, **kwargs)

def plot_rhist2d_contour(ax, rhist, level, **kwargs):
    """Draw level contour for a two dimensional RHist2D histogram.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes on which contours will be plotted.
    rhist : RHist2D
        Histogram to be plotted.
    level : float or list of float
        Value of level(s) at which contour(s) will be drawn.
    kwargs : dict, optional
        Additional parameters to pass to the `plot_nphist2d_contour` function.

    Returns
    -------
    pyplot.contour.QuadContourSet
        Matplotlib contour set
    """

    return plot_nphist2d_contour(ax, rhist.hist, rhist.bins, level, **kwargs)

