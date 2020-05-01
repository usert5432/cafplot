"""
Functions for plotting numpy histograms
"""

import numpy as np
from   matplotlib.image import NonUniformImage

def plot_nphist1d_base(ax, hist, bins, histtype = 'line', **kwargs):
    """Basic function to plot numpy histogram.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes on which histogram will be plotted.
    hist : ndarray, shape (N,)
        Histogram to be plotted.
    bins : ndarray, shape (N+1,)
        Bind edges for the histogram `hist`.
    histtype : { 'line', 'step', 'bar' }, optional
        Histogram style
    kwargs : dict, optional
        Additional parameters to pass directly to the matplotlib plotting funcs
    """

    if histtype == 'line':
        ax.hlines(hist, xmin = bins[:-1], xmax = bins[1:], **kwargs)

    elif histtype == 'step':
        ax.step(bins, np.hstack([0, hist]), where = "pre", **kwargs)

    elif histtype == 'bar':
        ax.bar(
            bins[:-1], height = hist, width = bins[1:] - bins[:-1],
            align = 'edge', **kwargs
        )
    else:
        raise ValueError("Unknown hist type: %s" % (histtype))

def plot_nphist1d_maker(ax, hist, bins, marker, **kwargs):
    """Plot markers to indicate numpy histogram bins.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes on which histogram will be plotted.
    hist : ndarray, shape (N,)
        Histogram to be plotted.
    bins : ndarray, shape (N+1,)
        Bind edges for the histogram `hist`.
    marker : str
        Marker style to plot. c.f. help(matplotlib.pyplot.scatter).
    kwargs : dict, optional
        Additional parameters to pass directly to the matplotlib plotting funcs
    """

    centers = (bins[:-1] + bins[1:]) / 2
    ax.scatter(centers, hist, marker = marker, **kwargs)

def plot_nphist1d(
    ax, hist, bins, label, histtype = None, marker = None, **kwargs
):
    """Plot numpy histogram.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes on which histogram will be plotted.
    hist : ndarray, shape (N,)
        Histogram to be plotted.
    bins : ndarray, shape (N+1,)
        Bind edges for the histogram `hist`.
    histtype : { 'line', 'step', 'bar' } or None, optional
        Histogram style. None by default.
    marker : str or None, optional
        If not None this function will add markers on top of histogram bins.
        c.f. help(matplotlib.pyplot.scatter).
    kwargs : dict, optional
        Additional parameters to pass directly to the matplotlib plotting funcs
    """

    if histtype is not None:
        plot_nphist1d_base(ax, hist, bins, histtype, label = label, **kwargs)
        # Do not label markers if histogram was plotted
        label = None

    if marker is not None:
        plot_nphist1d_maker(ax, hist, bins, marker, label = label, **kwargs)

def plot_nphist1d_error(ax, hist_down, hist_up, bins, err_type, **kwargs):
    """Plot vertical errors defined by numpy histograms

    Parameters
    ----------
    ax : Axes
        Matplotlib axes on which histogram will be plotted.
    hist_down : ndarray, shape (N,)
        Histogram describing the lower edge of error bars.
    hist_up : ndarray, shape (N,)
        Histogram describing the upper edge of error bars.
    bins : ndarray, shape (N+1,)
        Bind edges for the histograms.
    err_type : { 'bar', 'margin' } or None
        Error bar style.
    kwargs : dict, optional
        Additional parameters to pass directly to the matplotlib plotting funcs
    """

    if err_type is None:
        return

    centers = (bins[:-1] + bins[1:]) / 2

    if err_type == 'bar':
        ax.vlines(centers, hist_down, hist_up, **kwargs)
    elif err_type == 'margin':
        ax.fill_between(centers, hist_down, hist_up, **kwargs)
    else:
        raise ValueError("Unknown err type plot: '%s'" % (err_type,))

def plot_nphist2d(ax, hist, bins, **kwargs):
    """Draw 2D numpy histogram as a 2D image

    Parameters
    ----------
    ax : Axes
        Matplotlib axes on which histogram will be plotted.
    hist : ndarray, shape (N,M)
        Histogram to be plotted.
    bins : (ndarray, ndarray)
        Bind edges for the histograms.
    kwargs : dict, optional
        Additional parameters to pass directly to the matplotlib
        NonUniformImage function

    Returns
    -------
    NonUniformImage
        Matplotlib NonUniformImage that depicts `hist`.
    """

    bins_x = bins[0]
    bins_y = bins[1]

    range_x = (bins_x[0], bins_x[-1])
    range_y = (bins_y[0], bins_y[-1])

    im = NonUniformImage(
        ax, origin = 'lower', extent = range_x + range_y, **kwargs
    )

    centers_x = (bins_x[1:] + bins_x[:-1]) / 2
    centers_y = (bins_y[1:] + bins_y[:-1]) / 2

    im.set_data(centers_x, centers_y, hist.T)
    ax.images.append(im)

    ax.set_xlim(range_x)
    ax.set_ylim(range_y)

    return im

def plot_nphist2d_contour(
    ax, hist, bins, level, color = None, label = None, **kwargs
):
    """Draw level contour for the 2D numpy histogram.

    Parameters
    ----------
    ax : Axes
        Matplotlib axes on which contours will be plotted.
    hist : ndarray, shape (N,M)
        Histogram to be plotted.
    bins : (ndarray, ndarray)
        Bind edges for the histograms.
    level : float or list of float
        Value of level(s) at which contour(s) will be drawn.
    color : str or list of str or None, optional
        Colors for each contour to be drawn. If `color` is a str then
        all contours will have the same color.
    label : str or list of str or None, optional
        Labels for contours. If `label` is str, then only the first contour
        will be labeled.
    kwargs : dict, optional
        Additional parameters to pass directly to the pyplot.contour function

    Returns
    -------
    pyplot.contour.QuadContourSet
        Matplotlib contour set
    """

    bins_x = bins[0]
    bins_y = bins[1]

    range_x = (bins_x[0], bins_x[-1])
    range_y = (bins_y[0], bins_y[-1])

    centers_x = (bins_x[1:] + bins_x[:-1]) / 2
    centers_y = (bins_y[1:] + bins_y[:-1]) / 2

    if isinstance(level, (tuple, list)):
        levels = level
    else:
        levels = [ level, ]

    contour_set = ax.contour(
        centers_x, centers_y, hist.T, levels = levels,
        origin = 'lower', extent = range_x + range_y,
        colors = color, **kwargs
    )

    if label is not None:
        if isinstance(label, (tuple, list)):
            for l,c in zip(label, contour_set.collections):
                c.set_label(l)
        else:
            contour_set.collections[0].set_label(label)

    return contour_set

