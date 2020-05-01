"""
This module contains helper functions to handle files.
"""

import os

from .json_rfile import JSONRFile

def load(path):
    """Open file with CAFAna objects.

    This function parses file extension to find an appropriate IRFile object
    for a given file type and loads file using that IRFile.

    Parameters
    ----------
    path : str
        Path to the JSON file to read objects from.

    Returns
    -------
    IRFile
        IRFile object that can be used to load CAFAna objects from file `path`.
    """
    _, ext = os.path.splitext(path)

    if ext == '.json':
        return JSONRFile(path)
    elif ext == '.root':
        # NOTE: import is here to make dependency on uproot runtime optional
        # pylint: disable=import-outside-toplevel
        from .root_file import ROOTFile
        return ROOTFile(path)

    raise ValueError("Umknown file extension '%s'" % (path, ))

