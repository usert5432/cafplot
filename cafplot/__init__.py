"""
cafplot
=======

A package for plotting CAFAna objects using python/numpy/matplotlib stack.

Available subpackages
---------------------
plot
    Plotting functions for various CAFAna objects.
rfile
    Classes and functions for loading CAFAna from files.
rhist
    Classes corresponding to the ROOT histograms.
spectrum
    Classes corresponding to the CAFAna Spectrum.
stats
    Statistical helper functions.
surface
    Classes corresponding to the CAFAna Surface.
"""

from .rfile    import load
from .rhist    import RHist1D, RHist2D
from .spectrum import Spectrum
from .surface  import FSurface

__all__ = [ 'load', 'FSurface', 'RHist1D', 'RHist2D', 'Spectrum' ]

