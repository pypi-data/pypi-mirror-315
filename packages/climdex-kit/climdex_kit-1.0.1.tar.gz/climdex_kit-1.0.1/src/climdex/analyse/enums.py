#!/usr/bin/env python

from enum import Enum
from climdex.utils import MyEnumMeta


# enums

class AnalysisType(Enum, metaclass=MyEnumMeta):
    """Enumeration of analysis types offered by the package."""
    map2d = 'map'
    trend = 'trn'
    uncertainty = 'unc'

class SrcType(Enum, metaclass=MyEnumMeta):
    """Enumeration of climate index input types."""
    local  = 'local' # file-based NetCDFs
    openeo = 'openeo'
    wcps   = 'wcps'

class OpType(Enum, metaclass=MyEnumMeta):
    """Enumeration of operations types (eg. for baseline comparisons)."""
    diff      = 'diff'
    perc_diff = 'perc_diff'
    ratio     = 'ratio'

class AggrType(Enum, metaclass=MyEnumMeta):
    """Enumeration of data aggregation types."""
    avg = 'avg'
    med = 'med'
    min = 'min'
    max = 'max'
    quartile   = 'q[0-3]'
    percentile = 'p[0-9][0-9]'
    range = 'range'
    perc_pos = 'perc_pos'
    perc_neg = 'perc_neg'

class FmtType(Enum, metaclass=MyEnumMeta):
    """Enumeration of datasets formats."""
    nc   = 'nc'
    json = 'json'
    geojson = 'geojson'
    png  = 'png'
    stdout = '-'

