"""
Example of the 1D Spectrum plot.

Usage: spectrum_plot.py FILE PATH
where FILE is a file containing Spectrum to be plotted.
The Spectrum is expected to be found in the PATH directory of the FILE.
"""

import sys
import matplotlib.pyplot as plt

from cafplot      import load
from cafplot.plot import plot_rhist1d, plot_rhist1d_error, adjust_axes_to_hist

root_file = load(sys.argv[1])
spectrum  = root_file.get_spectrum(sys.argv[2])

pot   = 9e20
rhist = spectrum.rhist(pot = pot)

f, ax = plt.subplots()

plot_rhist1d      (ax, rhist, 'Histogram', 'step', color = 'C0')
plot_rhist1d_error(ax, rhist, color = 'C0', err_type = 'bar')

# Fit axes ranges to the histogram
adjust_axes_to_hist(ax, rhist)

ax.set_xlabel(sys.argv[2])
ax.set_ylabel('Events')

ax.legend()

plt.show()

