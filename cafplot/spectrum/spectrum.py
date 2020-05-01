"""
This module defines a Spectrum object corresponding to the CAFAna Spectrum.
"""

import copy

class Spectrum:
    """Spectrum object corresponding to the CAFAna Spectrum.

    Spectrum is a container that holds a histogram RHist together with
    its normalization in terms of either POT or Livetime.

    Parameters
    ----------
    rhist : RHist
        Histogram.
    pot : float or None
        POT value for the histogram `rhist`.
    livetime : float or None
        Livetime value for the histogram `rhist`.
    """

    def __init__(self, rhist, pot, livetime):
        self._rhist = rhist
        self._pot   = pot
        self._lt    = livetime

    def rhist(self, pot = None, livetime = None):
        """Get normalized histogram from the spectrum.

        This function returns normalized histogram by either `pot` or
        `livetime` from a given Spectrum.

        Parameters
        ----------
        pot : float or None, optional
            POT value to normalize histogram to. Default: None.
        livetime : float or None, optional
            POT value to normalize histogram to. Default: None.

        Returns
        -------
        RHist
            A normalized histogram

        Raises
        ------
        ValueError
            If supplied `pot` and `livetime` are both None, or both are not
            None this function will raise ValueError.
        """
        if (pot is None) == (livetime is None):
            raise ValueError("Either POT or Livetime should be specified")

        result = copy.deepcopy(self._rhist)

        if pot is not None:
            result.scale(pot / self._pot)
        else:
            result.scale(livetime / self._lt)

        return result

    def _check_other(self, other):
        """Verify binary operation is possible between `self` and `other`."""
        # pylint: disable=protected-access
        if not isinstance(other, Spectrum):
            raise RuntimeError(
                "Tried to binop Spectrum and %s" % (type(other))
            )

        if (self._pot is None) != (other._pot is None):
            raise RuntimeError(
                "Tried to binop Spectra with nonconformant POT"
            )

        if (self._lt is None) != (other._lt is None):
            raise RuntimeError(
                "Tried to binop Spectra with nonconformant Livetimes"
            )

    def _combine_pot_lt(self, other):
        # pylint: disable=protected-access
        pot   = None if (self._pot is None) else (self._pot + other._pot)
        lt    = None if (self._lt  is None) else (self._lt  + other._lt)

        return (pot, lt)

    def __add__(self, other):
        # pylint: disable=protected-access
        self._check_other(other)
        rhist = self._rhist + other._rhist

        return Spectrum(rhist, *self._combine_pot_lt(other))

    def __sub__(self, other):
        # pylint: disable=protected-access
        self._check_other(other)
        rhist = self._rhist - other._rhist

        return Spectrum(rhist, *self._combine_pot_lt(other))


