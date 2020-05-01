"""
A collection of plotting functions
"""

from .funcs import (
    adjust_axes_to_hist, make_plotdir, save_fig, remove_bottom_margin,
    make_figure_with_ratio
)
from .nphist import plot_nphist1d_base, plot_nphist2d
from .ratio  import plot_rhist1d_ratios, compute_ratios_range
from .rhist  import (
    plot_rhist1d, plot_rhist1d_error, plot_rhist2d, plot_rhist2d_contour
)

__all__ = [
    'adjust_axes_to_hist', 'plot_rhist1d', 'plot_rhist1d_error',
    'plot_nphist1d_base', 'make_plotdir', 'save_fig', 'remove_bottom_margin',
    'make_figure_with_ratio', 'plot_rhist1d_ratios', 'plot_nphist2d',
    'plot_rhist2d', 'plot_rhist2d_contour', 'compute_ratios_range'
]

