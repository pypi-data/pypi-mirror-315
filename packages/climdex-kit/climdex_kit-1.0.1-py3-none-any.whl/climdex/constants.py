
"""
Constants.
"""

import logging
import multiprocessing
import pkg_resources

from climdex import utils

# application
RET_OK=0

# indices
INDICES_ALL = 'all'

# general settings
DEFAULT_LOGLEVEL       = logging.INFO
DEFAULT_USE_LOG_COLORS = True
DEFAULT_CDO_LOGS_DIR   = './cdo_logs'
DEFAULT_CDO_TMP_DIR = '/tmp/cdo/'

DEFAULT_INDEXCONF_PATH = pkg_resources.resource_filename(__name__, 'etc/indices.ini')
LOGGING_CONF           = pkg_resources.resource_filename(__name__, 'etc/logging.yaml')
MODELS_LUT_PATH        = pkg_resources.resource_filename(__name__, 'etc/models_lut.json')

# indices conf
NC_TITLE = 'nc.title'
NC_INSTI = 'nc.institution'
NC_SOURC = 'nc.source'
NC_HISTO = 'nc.history'
NC_REFER = 'nc.references'
NC_LONGN = 'nc.long_name'
NC_STNDN = 'nc.standard_name'
NC_UNITS = 'nc.units'
NC_FREQN = 'nc.frequency'
NC_COMMN = 'nc.comment'
NC_MD_FIELDS = [
    NC_TITLE, NC_INSTI, NC_SOURC,
    NC_HISTO, NC_REFER, NC_LONGN,
    NC_STNDN, NC_UNITS, NC_FREQN,
    NC_COMMN]

# datasets attributes (metadata)
TITLE_ATTR   = 'Title'
INST_ATTR    = 'Institution'
SRC_ATTR     = 'Source'
HISTORY_ATTR = 'History'
REFS_ATTR    = 'References'
COMMENT_ATTR = 'Comment'
CREATED_ATTR = 'Created on'
FREQ_ATTR    = 'frequency'
#
LNAME_ATTR = 'long_name'
SNAME_ATTR = 'standard_name'

# time
CREATED_ON_FMT   = '%a %b %d %X %Y' # eg. "Wed Aug 25 03:29:12 2021" @see https://strftime.org/
COMPACT_TIME_FMT = '%Y%m%dT%H%M'
NC_REFTIME = 'nc.reftime'
DATETIME_FS = 'T'

# CPU parallelism
PARALLELISM_KWDS = ['all', 'all_but_one', 'one']
MAX_CPUS=multiprocessing.cpu_count()

# ND datacube dimensions
MODELS_DIM = 'model' 
MODELS_STAT_DIM = 'models_stat'
TIME_DIM   = 'time'
TIME_RANGE_DIM   = 'time_range'
XY_DIMS    = 'xy'
GEOM_DIM   = 'geom'
DEM_VAR = 'dem'
CRS_VAR = 'crs'
PROJ4_ATTR = 'proj4'
SPREF_ATTR = 'spatial_ref'
CMETHODS_ATTR = 'cell_methods'

# default significance confidence level
DEFAULT_SIGNIFICANCE_CONF = 95 # [%]

