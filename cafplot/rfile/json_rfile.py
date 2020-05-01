"""
A class for loading CAFAna objects from ROOT files.
"""

import json
import numpy as np

from cafplot.rhist    import RHist1D, RHist2D
from cafplot.spectrum import Spectrum
from cafplot.surface  import FSurface

from .irfile import IRFile

class JSONRFile(IRFile):
    """A class for loading CAFAna objects from ROOT files.

    This object loads CAFAna objects from the JSON files. JSON files can
    be produced from the ROOT files by using supplied program `to_json`.

    Parameters
    ----------
    path : str
        Path to the JSON file to read objects from.
    """

    def __init__(self, path):
        super(JSONRFile, self).__init__()

        with open(path, 'r') as f:
            self._dict = json.load(f)

    def close(self):
        pass

    @staticmethod
    def _get_dict_by_path(path, d):
        address = path.split('/')
        result  = d

        for part in address:
            result = result[part]

        return result

    @staticmethod
    def _load_rhist1d(rhist_dict):
        hist   = np.array(rhist_dict['values'])
        err_sq = np.array(rhist_dict['err_sq'])
        bins   = np.array(rhist_dict['bins'])

        # Strip overflow/underflow bins
        hist   = hist[1:-1]
        err_sq = err_sq[1:-1]
        bins   = [bins,]

        return RHist1D(bins, hist, err_sq)

    @staticmethod
    def _load_rhist2d(rhist_dict):
        hist   = np.array(rhist_dict['values'])
        err_sq = np.array(rhist_dict['err_sq'])
        bins_x = np.array(rhist_dict['bins_x'])
        bins_y = np.array(rhist_dict['bins_y'])

        # Strip overflow/underflow bins
        hist   = hist[1:-1,1:-1]
        err_sq = err_sq[1:-1,1:-1]
        bins   = [bins_x, bins_y]

        return RHist2D(bins, hist, err_sq)

    @staticmethod
    def _load_surf_internals(surf_dict):
        rhist = JSONRFile._load_rhist2d(
            JSONRFile._get_dict_by_path('hist', surf_dict)
        )

        fit_vals = surf_dict['minValues']
        val = float(fit_vals[0])
        x   = float(fit_vals[1])
        y   = float(fit_vals[2])

        return (rhist, val, x, y)

    @staticmethod
    def _load_rhist(path, d):
        rhist_dict = JSONRFile._get_dict_by_path(path, d)

        if 'bins_y' in rhist_dict:
            return JSONRFile._load_rhist2d(rhist_dict)
        else:
            return JSONRFile._load_rhist1d(rhist_dict)

    def get_rhist1d(self, path):
        d = JSONRFile._get_dict_by_path(path, self._dict)
        return JSONRFile._load_rhist1d(d)

    def get_rhist2d(self, path):
        d = JSONRFile._get_dict_by_path(path, self._dict)
        return JSONRFile._load_rhist2d(d)

    def get_spectrum(self, path):
        spectr_dict = self._get_dict_by_path(path, self._dict)

        rhist = self._load_rhist('hist', spectr_dict)
        pot   = float(spectr_dict['pot']     ['values'][1])
        lt    = float(spectr_dict['livetime']['values'][1])

        return Spectrum(rhist, pot, lt)

    def get_fsurface(self, path):
        surf_dict = JSONRFile._get_dict_by_path(path, self._dict)
        return FSurface(*JSONRFile._load_surf_internals(surf_dict))

