#!/usr/bin/env python

"""
Climate models Look-Up Table.
"""

import os
import re

import json
from pathlib import Path

from climdex import utils
from climdex.constants import MODELS_LUT_PATH


# the configurations of all indices
models_s2i = dict()
models_i2s = dict()

# LUT file
lut_path = MODELS_LUT_PATH

# ------------------------------------------------------------------------------
# show the index/model name mappings
def show_lut() -> list:
    load_lut()
    global models_s2i
    return [ f"  #{v:02} --> {k}" for k,v in models_s2i.items() ]

# ------------------------------------------------------------------------------
# load the LUT
def get_model(model_id:int, force_reload=False) -> str:
    """Gets the model name from its identifier (`None` if the index is not in LUT)"""
    load_lut(force_reload=force_reload)
    s = None
    model_id = int(model_id)
    if model_id in models_i2s:
        s = models_i2s[ model_id ]
    return s

# ------------------------------------------------------------------------------
#
def get_model_id(model:str, force_reload=False) -> int:
    """Gets the model identifier from its name (`None` if the name is not in LUT)"""
    load_lut(force_reload=force_reload)
    mid = None
    if model in models_s2i:
        mid = models_s2i[ model ]
    return mid

# ------------------------------------------------------------------------------
#
def get_all_models(force_reload=False) -> int:
    """Gets the list of all the models names in the LUT."""
    load_lut(force_reload=force_reload)
    return list(models_s2i.keys())

# ------------------------------------------------------------------------------
#
def get_all_models_ids(force_reload=False) -> int:
    """Gets the list of all the models identifiers in the LUT."""
    load_lut(force_reload=force_reload)
    return list(models_i2s.keys())

# ------------------------------------------------------------------------------
#
def load_lut(force_reload=False):
    """Loads the climate model mappings from the "models_lut.json" file."""
    global models_s2i
    if force_reload or len(models_s2i) == 0:
        models_s2i = __load_lut(lut_path)

# ------------------------------------------------------------------------------
#
def __load_lut(lut_path) -> dict:
    # - - - - - - - - - -
    if lut_path is None:
        raise ValueError("Missing lut path.")

    if not os.path.isabs(lut_path):
        lut_path = os.path.join(os.getcwd(), lut_path)
            #os.path.dirname(os.path.abspath(__file__)),
            #lut_path)

    if not os.path.exists(lut_path):
        raise ValueError(f"Provided climate models LUT file does not exist: {lut_path}.")
    # - - - - - - - - - -

    global models_s2i
    global models_i2s

    with open(lut_path, 'r') as lut_f:
        models_s2i = json.load( lut_f )
        # sort by index
        models_s2i = dict(sorted(models_s2i.items(), key=lambda x : x[1], reverse=False))
        # inverse lut
        models_i2s = { v: k for k,v in models_s2i.items() }

    return models_s2i

# ------------------------------------------------------------------------------
# identify models ID from paths
#
def identify_models( paths, lenient=False, force_reload=False):
    """
    Identifies model IDs from one or more paths.

    Parameters
    ----------
    paths : str or Path or list
        The path(s) of the input files.

    lenient : bool (optional, default=False)
        Whether to be lenient or not in the search, i.e.
        allow to have one or more input files not 
        associated with any model.

    force_reload : bool (optional, default=False)
        Whether to force reloading the model mappings in the lookup table 
        from disk.

    Returns
    -------
    The set of models indices associated with each input file, according
    to the LUT.
    """
    # - - - - - - - - - -
    if paths is None:
        return None

    if type(paths) is str:
        paths = Path(paths)

    if type(paths) is Path:
        paths = list(paths)

    if len(paths) == 0:
        return list()
    else:
        paths = [Path(p) for p in paths]
    # - - - - - - - - - -

    m_ids = dict() # -> path -> id

    filenames = [f.name for f in paths]

    for model in get_all_models( force_reload=force_reload ):
        r = re.compile(model)
        rmatch = list(filter(r.search, filenames))
        if len(rmatch) > 1:
            raise ValueError("Multiple files match the model {model}", model)
        elif len(rmatch) == 1:
            filename = rmatch[0]
            model_id = get_model_id( model )
            m_ids.update({ filename:model_id })
        else:
            pass # OK if no match

    if not lenient:
        if len(m_ids) != len(paths):
            raise RuntimeError("Could find model for {} input files.", len(paths)-len(m_ids))

    return m_ids
