"""
This module defines an abstract Surface class corresponding to ISurface in
CAFAna
"""

class Surface:
    """An abstract class corresponding to the CAFAna ISurface

    Parameters
    ----------
    rhist : RHist2D
        2D histogram containing surface "heights".
    best_value : float
        Best fit value for the surface. Typically a minimum of `rhist.
    best_x : float
        X-coordinate of the best fit value for the surface.
    best_y : float
        Y-coordinate of the best fit value for the surface.
    """
    def __init__(self, rhist, best_value, best_x, best_y):
        self._rhist    = rhist
        self._best_val = best_value
        self._best_x   = best_x
        self._best_y   = best_y

    @property
    def rhist(self):
        """RHist2D containing surface "heights"."""
        return self._rhist

    @property
    def best_value(self):
        """Best fit value of the surface."""
        return self._best_val

    @property
    def best_fit(self):
        """Coordinates (x,y) of the Best fit value of the surface."""
        return (self._best_x, self._best_y)

    def level(self, sigma = 1, best_value = None):
        """Calculate surface level corresponding to `sigma` significance."""
        raise NotImplementedError

