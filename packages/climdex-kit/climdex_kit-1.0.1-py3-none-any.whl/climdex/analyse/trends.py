#!/usr/bin/env python

"""
Handler of the TREND analysis types.

Actual functionality is implemented in other modules depending on the 
type of input data: local NetCDFs, openEO, rasdaman, etc.
"""

from . import trends_nc
from .enums import SrcType, FmtType

# constants
DEFAULT_OFMT = FmtType.json
ALLOWED_OFMTS = [
        FmtType.stdout,
        FmtType.json,
        FmtType.geojson,
        FmtType.nc
]

FCALLS = {
    SrcType.local  : trends_nc._extract_trend,
    SrcType.openeo : None,
    SrcType.wcps   : None
}

def get_default_format():
    """ Gets the default output format for TRENDS analysis artifacts."""
    return DEFAULT_OFMT


def get_allowed_out_formats():
    """ Gets the default output format for TRENDS analysis artifacts."""
    return ALLOWED_OFMTS


def get_worker_function(src_type:SrcType):
    """
    Gets the reference to the function actually implementing the analysis
    for the given type of source index data.
    """    
    return FCALLS[src_type] if src_type is not None else None


def validate_args(**kwargs) -> bool:
    """
    Maps' specific argument validation checks.
    """
    taggr  = kwargs['taggr']    if 'taggr'    in kwargs else None
    eaggr  = kwargs['eaggr']    if 'eaggr'    in kwargs else None
    xyaggr = kwargs['xyaggr']   if 'xyaggr'   in kwargs else None
    bline  = kwargs['baseline'] if 'baseline' in kwargs else None
    tint   = kwargs['tint']     if 'tint'     in kwargs else [None,]

    if tint is not None and not isinstance(tint[0],list):
        tint = [tint,]

    if (taggr is not None) and len(taggr) > 1:
        raise NotImplementedError("Only 1 'taggr' time aggregation per analysis currently supported.")
        # TODO also allow multiple taggr

    if bline is not None and taggr is None:
        raise ValueError("Please provide a temporal aggregation for the baseline comparison.")

    if xyaggr is None:
        raise ValueError("Please provide a spatial aggregation option via 'xyaggr' argument.")

    if eaggr is None:
        #    raise ValueError("Please provide an ensemble aggregation option via 'eaggr' argument.")
        # -> No, I might want to want to see each model's trend
        ...
    elif len(eaggr) > 1 and len(xyaggr) > 1:
        raise ValueError("At most 1 multiple aggregation among 'eaggr' and 'xyaggr'.")


    return True
