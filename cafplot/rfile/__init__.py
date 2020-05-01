"""
This module contains classes and functions to load CAFAna objects from files.
"""

import importlib

from .json_rfile import JSONRFile
from .funcs      import load

__all__ = [ 'JSONRFile', 'load' ]

# Make `uproot` an optional runtime dependency
if importlib.util.find_spec("uproot") is not None:
    from .root_file import ROOTFile
    __all__.append('ROOTFile')

