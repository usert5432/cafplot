"""
This module contains general purpose plot functions
"""

import os
import matplotlib.pyplot as plt

def make_plotdir(outdir):
    """Make directory 'plot' in the `outdir` and return its path"""
    plotdir = os.path.join(outdir, "plots")
    os.makedirs(plotdir, exist_ok = True)

    return plotdir

def save_fig(f, fname, ext):
    """Save figure `f` to a file named `fname`

    Parameters
    ----------
    f : plt.Figure
        Matplotlib figure to be saved
    fname : str
        File name to save figure to
    ext : str or list of str
        If `ext` is str, then figure will be saved to `fname`.`ext`.
        If `ext` is a list of str, then a number of files will be produced
          one for each extension in the list.
    """
    if isinstance(ext, list):
        for e in ext:
            save_fig(f, fname, e)
    else:
        f.savefig("%s.%s" % (fname, ext), bbox_inches = 'tight')

def remove_bottom_margin(ax):
    """Set bottom of plot to 0 y value."""
    ylim = (0, ax.get_ylim()[1])
    ax.set_ylim(*ylim)

def adjust_axes_to_hist(ax, rhist):
    """Remove bottom/left/right margins from the 1D histogram plot."""
    remove_bottom_margin(ax)
    ax.set_xlim(rhist.bins_x[0], rhist.bins_x[-1])

def make_figure_with_ratio():
    """Create a vertically split (3 to 1) figure"""

    f, (ax, axr) = plt.subplots(
        nrows       = 2,
        sharex      = True,
        gridspec_kw = { 'height_ratios' : [3,1] }
    )

    f.tight_layout(h_pad = 0.1, pad = 2.0)

    return f, ax, axr

