"""
Functions for plotting cafplot.surface.Surface
"""

from .rhist import plot_rhist2d, plot_rhist2d_contour

def plot_surface(ax, surface, **kwargs):
    """Plot `surface` as a 2D image.

    A wrapper around `plot_rhist2d` to draw surface as a 2d image.

    Parameters
    ----------
    ax : Axes
        matplotlib axes on which contours will be plotted.
    surface : Surface
        cafplot.surface.Surface object to be plotted
    kwargs : dict, optional
        Values to pass to the plot_rhist2d

    Returns
    -------
    NonUniformImage
        matplotlib NonUniformImage that depicts `surface`.
    """
    return plot_rhist2d(ax, surface.rhist, **kwargs)

def plot_surface_best_fit(ax, surface, **kwargs):
    """Show `surface` best fit point on a 2D image.

    Parameters
    ----------
    ax : Axes
        matplotlib axes on which contours will be plotted.
    surface : Surface
        cafplot.surface.Surface object which best fit point is to be shown
    kwargs : dict, optional
        Values to pass to the pyplot.scatter function
    """

    ax.scatter(*surface.best_fit, **kwargs)

def plot_surface_gauss_contour(ax, surface, sigma = 1, **kwargs):
    """Plot `surface` contour corresponding to significance `sigma`.

    Parameters
    ----------
    ax : Axes
        matplotlib axes on which contours will be plotted.
    surface : Surface
        cafplot.surface.Surface which contour should be shown.
        Surface object must have `.level` method implemented.
    kwargs : dict, optional
        Values to pass to the `plot_rhist2d_contour` function

    Returns
    -------
    pyplot.contour.QuadContourSet
        matplotlib contour set
    """

    level = surface.level(sigma)
    return plot_rhist2d_contour(ax, surface.rhist, level, **kwargs)

