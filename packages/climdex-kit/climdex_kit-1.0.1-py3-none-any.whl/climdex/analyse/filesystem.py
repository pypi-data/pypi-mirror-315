
"""
Utilities and procedures for dealing with files in the local file system
for the climdex.analyse module.
"""

from pathlib import Path

from .. import cmodels
from ..utils import *
from ..nc import *

def fetch_index_files( idir, rgx:str=NETCDF_RGX, models=None):
    """
    Fetch climate index data paths.

    Parameters
    ----------
    idir : str or Path
        The path to the input directory where to look for the
        input files (non-recursively).

    rgx : str
        The regular expression to be used to filter files in idir
        (default: .nc)

    models : int or list (optional)
        List of climate models indices to further filter the files
        found in idir. See models_lut.json file (or climdex.cmodels module)
        for the mapping to actual climate models labels.

    Returns
    -------
    The list of absolute paths to the files.

    Examples
    --------
    >>> from pathlib import Path
    >>> idir = Path('/path/to/climate/data/')
    >>> fetch_index_files( idir, rgx="*.tif", models=[1, 3, 7] )
    """
    # - - - - - - - - - -
    idir = Path(idir)

    if models is not None and isinstance(models, int):
        models = [models]
    # - - - - - - - - - -

    match_files = []

    if models is not None:
        # from models ID to model name for matching the filenames:
        models_str = [ cmodels.get_model(x) for x in models ]
        models_rgx = [ f"*{m}{rgx}"         for m in models_str ]
        match_files = glob_or(idir, models_rgx)
    else:
        match_files = list(idir.glob( rgx ))

    return match_files



