"""
A class for loading CAFAna objects from ROOT files.
"""

import uproot

from cafplot.rhist    import RHist1D, RHist2D
from cafplot.spectrum import Spectrum
from cafplot.surface  import FSurface

from .irfile import IRFile

class ROOTFile(IRFile):
    """A class for loading CAFAna objects from ROOT files.

    This class relies on the uproot library for loading ROOT objects from ROOT
    files.

    Parameters
    ----------
    path : str
        Path to the file to read objects from.
    """

    def __init__(self, path):
        super(ROOTFile, self).__init__()
        self._f = uproot.open(path)

    @staticmethod
    def _load_hist_internals(hist):
        values = hist.values
        err_sq = hist.variances
        bins   = hist.edges

        return (bins, values, err_sq)

    @staticmethod
    def _load_rhist1d(path, d):
        bins, values, err_sq = ROOTFile._load_hist_internals(d.get(path))
        return RHist1D([bins,], values, err_sq)

    @staticmethod
    def _load_rhist2d(path, d):
        return RHist2D(*ROOTFile._load_hist_internals(d.get(path)))

    @staticmethod
    def _load_rhist(path, d):
        hist = d.get(path)
        ndim = hist.values.ndim
        args = ROOTFile._load_hist_internals(hist)

        if ndim == 1:
            bins, values, err_sq = args
            return RHist1D([bins,], values, err_sq)

        elif ndim == 2:
            return RHist2D(*args)

        else:
            raise NotImplementedError

    @staticmethod
    def _load_surf_internals(surf_dir):
        rhist    = ROOTFile._load_rhist2d('hist', surf_dir)
        fit_vals = surf_dir.get('minValues')

        # TODO: find how to unpack TVector properly
        # pylint: disable=protected-access
        val = fit_vals._fElements[0]
        x   = fit_vals._fElements[1]
        y   = fit_vals._fElements[2]

        return (rhist, val, x, y)

    def get_rhist1d(self, path):
        return ROOTFile._load_rhist1d(path, self._f)

    def get_rhist2d(self, path):
        return ROOTFile._load_rhist2d(path, self._f)

    def get_spectrum(self, path):
        spectr_dir = self._f.get(path)

        rhist = self._load_rhist('hist', spectr_dir)
        pot   = spectr_dir.get('pot')     .values[0]
        lt    = spectr_dir.get('livetime').values[0]

        return Spectrum(rhist, pot, lt)

    def get_fsurface(self, path):
        return FSurface(*ROOTFile._load_surf_internals(self._f.get(path)))

    def close(self):
        self._f.close()

