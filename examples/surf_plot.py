"""
Example of the FrequentistSurface plot.

Usage: surf_plot.py FILE
where FILE is a file containing Surface to be plotted. The surface is expected
to be found in the `/surface` directory of the FILE.
"""

import sys
import matplotlib.pyplot as plt

from cafplot import load
from cafplot.plot.surface import (
    plot_surface, plot_surface_best_fit, plot_surface_gauss_contour
)

root_file = load(sys.argv[1])
surface   = root_file.get_fsurface('surface')

f, ax = plt.subplots()

im = plot_surface(ax, surface)

plot_surface_best_fit(ax, surface, color = 'red', marker = '*')
plot_surface_gauss_contour(
    ax, surface, sigma = 1, color = 'red', label = r'1$\sigma$'
)

ax.set_xlabel(r'$\sin^2 \theta_{23}$')
ax.set_ylabel(r'$\Delta m^2_{32}$')

ax.legend()

f.colorbar(im)

plt.show()

