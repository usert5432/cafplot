"""
An abstract class to load CAFAna objects from files.
"""

class IRFile:
    """An abstract class to load CAFAna objects from files. """

    def __init__(self):
        pass

    def get_rhist1d(self, path):
        """Load ROOT 1D histogram RHist1D specified by `path`."""
        raise NotImplementedError

    def get_rhist2d(self, path):
        """Load ROOT 2D histogram RHist2D specified by `path`."""
        raise NotImplementedError

    def get_spectrum(self, path):
        """Load CAFAna Spectrum specified by `path`."""
        raise NotImplementedError

    def get_fsurface(self, path):
        """Load CAFAna FrequentistSurface specified by `path`."""
        raise NotImplementedError

    def close(self):
        """Close file and release resources."""
        raise NotImplementedError

