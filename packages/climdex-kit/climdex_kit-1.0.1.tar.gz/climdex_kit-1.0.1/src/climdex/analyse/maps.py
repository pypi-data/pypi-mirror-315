#!/usr/bin/env python

"""
Abstract handler of the MAP analysis types.

Actual functionality is implemented in other modules depending on the 
type of input data: local NetCDFs, openEO, rasdaman, etc.
"""

from . import maps_nc
from .enums import SrcType, FmtType

# constants
DEFAULT_OFMT = FmtType.nc
ALLOWED_OFMTS = [
        FmtType.stdout,
        FmtType.json,
        FmtType.nc,
        FmtType.png
]

FCALLS = {
    SrcType.local  : maps_nc._extract_map,
    SrcType.openeo : None,
    SrcType.wcps   : None
}

def get_default_format():
    """ Gets the default output format for MAPS analysis artifacts."""
    return DEFAULT_OFMT


def get_allowed_out_formats():
    """ Gets the default output format for MAPS analysis artifacts."""
    return ALLOWED_OFMTS


def get_worker_function(src_type:SrcType):
    """
    Gets the reference to the function actually implementing the analysis
    for the given type of source index data.
    """    
    return FCALLS[src_type] if src_type is not None else None


def validate_args(**kwargs):
    """
    Maps' specific argument validation checks.
    """
    taggr  = kwargs['taggr']  if 'taggr'  in kwargs else None
    eaggr  = kwargs['eaggr']  if 'eaggr'  in kwargs else None
    xyaggr = kwargs['xyaggr'] if 'xyaggr' in kwargs else None
    models = kwargs['models'] if 'models' in kwargs else None
    tint   = kwargs['tint']   if 'tint'   in kwargs else [None,]

    if xyaggr is not None:
        raise ValueError("Spatial aggregation is not allowed for maps.")

    if eaggr is None and len(models) != 1:
        raise ValueError("Please provide an ensemble aggregation option via 'eaggr' argument.")

    if taggr is None and tint is not None:
        if any([t[0] != t[1] for t in tint]):
            raise ValueError("Please either provide a temporal aggregation option, or a single time-step time filter.")

    if tint is not None and len(tint) > 1:
        raise NotImplementedError("Only 1 time filter per map analysis currently supported.")

    return True
