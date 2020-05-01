"""
Helper functions to simplify plots of RHist1D ratios
"""

import numpy as np
from .rhist import plot_rhist1d, plot_rhist1d_error

def compute_ratios_range(
    list_of_ratio_rhists, range_percentile_loss = 5, range_margin = 0.1
):
    """Find range of RHist1D ratios by clipping outliers.

    This function will try to find an optimal range of RHist1D ratios plot
    by discarding (2 * `range_percentile_loss` %) points from both ends of the
    RHist1D ratios.

    Parameters
    ----------
    list_of_ratio_rhists : list of RHist1D
        List of RHist1D containing histogram ratios
    range_percentile_loss : float, optional
        Fraction of points (in %) to be discarded for each RHist1D in
        `list_of_ratio_rhists`. Default: 5.
    range_margin : float, optional
        Pad RHist1D obtained after discarding outliers by `range_margin`.

    Returns
    -------
    (range_min, range_max) : (float, float)
        Calculated range.
        Algorithm may fail and return return (-np.inf, np.inf).

    """
    max_ratio = -np.inf
    min_ratio =  np.inf

    for ratio_rhist in list_of_ratio_rhists:
        ratio = ratio_rhist.hist[~np.isinf(ratio_rhist.hist)]

        max_ratio = max(
            max_ratio, np.nanpercentile(ratio, 100 - range_percentile_loss)
        )
        min_ratio = min(
            min_ratio, np.nanpercentile(ratio,  range_percentile_loss)
        )

    ratio_range = (max_ratio - min_ratio)

    max_ratio += ratio_range * range_margin
    min_ratio -= ratio_range * range_margin

    if np.isclose(min_ratio, max_ratio):
        return (-np.inf, np.inf)

    return (min_ratio, max_ratio)

def plot_rhist1d_ratios(
    ax, list_of_rhists, list_of_colors, hist_kwargs = None, err_kwargs = None
):
    """Plot ratios of RHist1D histograms.

    This function will calculate ratios of each histogram in the
    `list_of_rhists[1:]` to the `list_of_rhists[0]` and plot them.

    Parameters
    ----------
    ax : Axes
        matplotlib axes on which contours will be plotted.
    list_of_rhists : list of RHist1D
        List of histograms, ratios of which are to be plotted.
        First histogram in the `list_of_rhists` will be used as a denominator.
    list_of_colors : list of str
        List of colors corresponding to each RHist1D in `list_of_rhists`.
    hist_kwargs : dict or None, optional
        Additional parameters that will be passed to `plot_rhist1d` when
        plotting ratios. Default: None.
    err_kwargs : dict or None, optional
        Parameters that will be passed to `plot_rhist1d_error` when plotting
        error bars of the ratios. If None then no error bars will be plotted.
        Default: None.

    Returns
    -------
    list of RHist1D
        List of the calculated histogram ratios corresponding to the.
        `list_of_rhists[1:]` / `list_of_rhists[0]`.
    """

    ax.axhline(1, 0, 1, linestyle = 'dashed', color = list_of_colors[0])

    list_of_ratio_rhists = [
        rhist / list_of_rhists[0] for rhist in list_of_rhists[1:]
    ]

    hist_kwargs = hist_kwargs or {}

    for idx,ratio_rhist in enumerate(list_of_ratio_rhists):
        color = list_of_colors[idx + 1]
        plot_rhist1d(
            ax, ratio_rhist,
            label    = None,
            histtype = 'line',
            marker   = None,
            zorder   = idx,
            color    = color,
            **hist_kwargs
        )

        if err_kwargs is not None:
            plot_rhist1d_error(
                ax, ratio_rhist, color = color, **err_kwargs, **hist_kwargs
            )

    return list_of_ratio_rhists

