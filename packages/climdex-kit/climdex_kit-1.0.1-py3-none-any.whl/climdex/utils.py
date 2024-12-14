import argparse
import logging
import logging.config
import os
import re
import sys
import yaml

import xarray as xr

from datetime import datetime
from pathlib import Path
from configparser import ConfigParser
from enum import IntEnum, EnumMeta
from .constants import *
from .nc import NETCDF_EXT, NETCDF_RGX, NETCDF_NAMING_SCHEME

# default application log conf
default_log_level = logging.INFO
default_log_fmt   = '%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s'
default_data_fmt  = '%Y-%m-%dT%H:%M:%S'
use_log_color     = DEFAULT_USE_LOG_COLORS

# ------------------------------------------------------------------------------
# log levels

class DebugLevels(IntEnum):
    NO_DEBUG = 0
    NORMAL = 1
    VERBOSE = 2

# global DEBUG configuration
__DEBUG_LEVEL  = DebugLevels.NO_DEBUG # 0:normal 1:debug 2:DEBUG

def debug_level() -> DebugLevels:
    """Debug mode of the program."""
    return __DEBUG_LEVEL

def set_debug_level(l:DebugLevels):
    """Update the debug mode of the program."""
    global __DEBUG_LEVEL
    __DEBUG_LEVEL = l

def set_default_log_level(level):
    """
    Sets the new default level for loggers fetched via utils.get_logger().

    Returns
    -------
    The previous default log level.
    """
    global default_log_level
    old_level         = default_log_level
    default_log_level = level

    return old_level

# ------------------------------------------------------------------------------
# get the logger, optionally setting a non-default level
#
# NOTE: logging from multiple process -> SocketHandler TODO
# @see https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes
def get_logger(name, level=None):
    """
    Gets the application logger attached to the given name.
    Set level to either None or logging.NOTSET (0) to apply the default level.
    """
    logger = logging.getLogger(name)
    if level is not None and level != logging.NOTSET:
        logger.setLevel(level)
    else:
        logger.setLevel(default_log_level)
    return logger

# ------------------------------------------------------------------------------
# configure the logger based on either an external configuration file set via input
# or environment variable

def setup_logging(
    path   ='logging.yaml',
    level  = default_log_level,
    env_key='LOG_CFG'
):
    """
    Setup global logging configuration
    """

    global default_log_level
    default_log_level = level

    path = Path(path) if path is not None else None
    env_value = os.getenv(env_key, None) if env_key is not None else None

    if env_value:
        #print(f"LOG_CFG={value}")
        path = env_value
    if path is not None and path.exists():
        #print(f"log configuration file: {path}")
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        #print(f"log configuration:  {config}")
    else:
        #print(f"log basic {logging.getLevelName(level)} stdout handler")
        root       = logging.getLogger()
        format_str = default_log_fmt

        if use_log_color:
            # set level (default is WARNING)
            # console handler
            #log_format = logging.Formatter(format_str)
            log_format = ColoredFormatter(default_log_fmt, default_data_fmt, color_msg=True, color_time=True)
            handler = logging.StreamHandler()#sys.stdout)
            #handler.setLevel(level) -> NO: otherwise LOGGER.setLevel() since handler's level is not inherited from parent
            handler.setFormatter(log_format)
            root.addHandler(handler) # (root) logger to console
            root.setLevel(level)
            #print(f'root logger: {root}')
        else:
            logging.basicConfig(format=format_str, level=level)
            #print(f'root logger: {logging.getLogger()}')

        #root.info("stdout logger set")

# ------------------------------------------------------------------------------
# get the path of a module

def module_path():
    encoding = sys.getfilesystemencoding()
    #return os.path.dirname(unicode(__file__, encoding))
    return os.path.dirname(__file__)


# path of this module
MODULE_PATH = module_path()

# ------------------------------------------------------------------------------
# console colored log format

# @credits https://stackoverflow.com/a/384125/1329340

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
#The background is set with 40 plus the number of the color, and the foreground with 30

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}

# for file-based config
def coloredFormatterFactory(format:str, datefmt:str, color_msg:bool, color_time:bool):
      return ColoredFormatter(msg_fmt=format, datefmt=datefmt, color_msg=color_msg, color_time=color_time)

class ColoredFormatter(logging.Formatter):

    # for file-based log config
    color_msg  = True
    color_time = False

    def __init__(self, msg_fmt, datefmt, color_msg=True, color_time=False):
        logging.Formatter.__init__(self, fmt=msg_fmt, datefmt=datefmt)
        self.color_msg  = color_msg
        self.color_time = color_time
        self.color_whole_line = color_time and color_msg

    def format(self, record):
        levelname = record.levelname
        message   = record.msg
        #datetime  = record.asctime FIXME asctime not availale at this point

        if levelname in COLORS:
            if self.color_whole_line:
                fmt_str = logging.getLogger().handlers[0].formatter._fmt
                log_fmt = COLOR_SEQ % (30 + COLORS[levelname]) + fmt_str + RESET_SEQ
                formatted_record = logging.Formatter(log_fmt).format(record)
            else:
                levelname_color  = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
                record.levelname = levelname_color
                if self.color_msg:
                    msg_color    = COLOR_SEQ % (30 + COLORS[levelname]) + message + RESET_SEQ
                    record.msg   = msg_color
                if self.color_time:
                    pass # TODO
                    #time_color     = COLOR_SEQ % (30 + COLORS[levelname]) + datetime + RESET_SEQ
                    #record.asctime = time_color
                formatted_record = logging.Formatter.format(self, record)
        else:
            formatted_record = logging.Formatter.format(self, record)

        return formatted_record


# ------------------------------------------------------------------------------
# multiprocessing

# (keywords)<->(n) mapping
__kwds2cpus = {
    PARALLELISM_KWDS[0]: MAX_CPUS,
    PARALLELISM_KWDS[1]: max(1, MAX_CPUS-1),
    PARALLELISM_KWDS[2]: 1,
}

# (keywords)<->(n) converter
def ncpus_of(cpus) -> int:
    """
    Determines the number of CPU cores associated with the given input.

    cpus : int or str
        The requested number of CPU cores, either by direct number or by keyword.
        See PARALLELISM_KWDS.

    Returns
    -------
    The real number of CPU cores that shall be used.
    """
    if type(cpus) is int:
        return min(cpus, MAX_CPUS)

    if cpus not in PARALLELISM_KWDS:
        raise ValueError(f'Unknown parallelism keyword: {cpus}')

    return __kwds2cpus[cpus]

# ------------------------------------------------------------------------------
# enum utils
class MyEnumMeta(EnumMeta):
    def __contains__(cls, item):
        """True if item is enum or string with value listed in the enumeration."""
        try:
            contained = item.value in cls.values()
        except AttributeError:
            contained = item in cls.values()
        return contained
    def values(cls):
        return [v.value for v in cls.__members__.values()]

# ------------------------------------------------------------------------------
#
def search_files(idir, input_vars, scenario, regex):
    """
    Gets actual paths to all input files defined by a scenario,
    and for the given input ($-signed) variables.

    Parameters
    ----------
    idir : str or Path
        The input root folder
    input_vars
        $-signed name of input variable (eg. $tasmin)
    scenario : str
        The scenario framing the input data ([!] idir/varname/scenario structure assumed)
    regex : str
        Regular expression for filter the input models (NOTE: no '*' pre-/post-poned automatically)

    Returns
    -------
    A dictionary mapping models names to the file paths (keyed by variable names),
    plus a dictionary mapping variables to scenario-independent input files.
    E.g.
             INPUT                                        OUTPUT
     input_vars: [$pr $landuse]    --->   model_A -> { pr:/idir/pr/rcp45/pr_model_A_day_19702100_rcp45.nc }
     scenario  : rcp45                    model_B -> { pr:/idir/pr/rcp45/pr_model_B_day_19702100_rcp45.nc }
                                          $landuse   -> /idir/landuse/landuse.nc
    """
    LOGGER = get_logger(__name__)

    input_vars_dict, const_vars_dict = _input_varnames_to_paths(idir, input_vars, scenario)
    #       |               |--(const1) -> /path/to/file1.nc
    #       |
    #       |--(var1) -> /path/to/var1/scenario/
    #       |--(var2) -> /path/to/var2/scenario/
    LOGGER.debug("scenario-based input: %s", input_vars_dict)
    LOGGER.debug("const input: %s", const_vars_dict)

    # drop const vars from dictionary of scenario/model dependent input variables:
    input_vars = [ var for var in input_vars if not var in const_vars_dict ]

    # store paths and "names" of models for each input var
    # path : /path/to/CORDEX-Adjust/QDM/tasmin/rcp45/tasmin_EUR-11_CNRM-CERFACS-CNRM-CM5_CLMcom-CCLM4-8-17_r1i1p1_v1_day_19702100_rcp45.nc
    # file : tasmin_EUR-11_CNRM-CERFACS-CNRM-CM5_CLMcom-CCLM4-8-17_r1i1p1_v1_day_19702100_rcp45.nc
    # name :        EUR-11_CNRM-CERFACS-CNRM-CM5_CLMcom-CCLM4-8-17_r1i1p1_v1_day_19702100
    #        (VAR )_(---------------------   MODEL NAME   ---------------------------)_res_YYYYYYYY_(SCENARIO).nc
    models_paths_dict = dict(zip(input_vars, [sorted(input_vars_dict[var].glob(regex)) for var in input_vars]))

    # extract model name from file name
    #   (model name) -> { var1:model_path, var2:model_path ... }
    models_names_dict = _extract_models_names(models_paths_dict, scenario, lenient=True)
    LOGGER.debug("Models names extracted: %s", list(models_names_dict.keys()))

    return models_names_dict, const_vars_dict

# ------------------------------------------------------------------------------
#
def _input_varnames_to_paths(idir, input_vars, scenario):
    """
    Translates dollar-signed variable names ot actual models paths.
    This method assumes the following input data structure:

    + idir/
        |--- var/   (eg. pr, temp, ...)
               |--scenario_X
               |     |---model_A.nc
               |     |---model_B.nc
               |     |---model_C.nc
               |     :
               |
               |--scenario_Y
               |     |---model_A.nc
               |     |---model_B.nc
               |     |---model_C.nc
               |     :
               :
    Parameters
    ----------
    idir : str or Path
        Root input files folder.
    input_vars : list
        1+ dollar-signed input variable names.
    scenario : str
        Name of the climate scenario framing the input.

    Returns
    -------
    Two dictionaries, one mapping variable to input models folders, the other
    one mapping "constant" variables mapping to single files.
    E.g.
       $pr    --> idir/pr/scenario/      <-- models folders
       $temp  --> idir/temp/scenario/    <--    "  "     "  "
       $foo   --> idir/foo/foo.nc        <-- constant scenario-independent file
    """
    LOGGER = get_logger(__name__)

    LOGGER.debug("vars: %s", input_vars)
    input_vars_dict = dict.fromkeys(input_vars, None)
    const_vars_dict = dict() # variables defined in index configuration (eg. landmask=/path/to/landmask)

    for var in input_vars:
        var_dir      = idir / var[1:]
        scenario_dir = var_dir / scenario
        input_vars_dict[var] = scenario_dir
        LOGGER.debug("%s -> %s", var, scenario_dir)
        # check file system:
        if not var_dir.exists():
            raise ValueError(f"Cannot find variable {var}'s folder in {idir}.""")
        if not scenario_dir.exists():
            # is it a scenario-independent single-file constant?
            globbed = list(var_dir.glob(NETCDF_RGX))
            if len(globbed) == 0:
                raise ValueError(f"Cannot find scenario {scenario}'s folder for variable {var}.")
            elif len(globbed) > 1:
                default_const_file = var_dir / '{}{}'.format(var[1:], NETCDF_EXT)
                if default_const_file.exists():
                    const_vars_dict[var] = default_const_file
                    input_vars_dict[var] = var_dir
                else:
                    raise ValueError("Multiple NetCDF ({}) found in '{}', and default '{}' is not found."
                            .format(NETCDF_RGX, var_dir, default_const_file.name))
            else:
                LOGGER.info("Assuming %s as scenario/model-independent constant image under %s", var, var_dir)
                const_vars_dict[var] = globbed[0]
                input_vars_dict[var] = var_dir

    return input_vars_dict, const_vars_dict

# ------------------------------------------------------------------------------
#
def _extract_models_names(models_paths_dict, scenario, file_ext=NETCDF_EXT, lenient=False):
    """
    Extracts the name of the model from all input files, following the
    naming scheme: '{variable}_{model_name}_{scenario}{file_ext}'
    Eg. "tasmin_MODEL_A_rcp45.nc" --> "MODEL_A"

    Parameters
    ----------
    models_paths_dict : dict
        Mapping of ($-signed) variable names to models' direct root folder.
    scenario : str
        Name of the climate scenario of the input files.
    file_ext : str
        The extension of the input model files (dot included)
    lenient:
        Be lenient if models among the input variables do not match exactly
        (exception is raised otherwise).

    Returns
    -------
    A dictionary mapping model models names to actual input files,
    mapped as a sub-dictionary keyed by input variables
    (same keys as models_paths_dict input).
    """

    LOGGER = get_logger(__name__)

    input_vars = models_paths_dict.keys()

    # (var) -> [models]
    models_names_dict = dict.fromkeys(input_vars)

    for var in models_names_dict:
        ifiles = [ path.name for path in models_paths_dict[var] ]
        ####################################################################################
        filename_regex = __nc_name_rgx(varname=var[1:], scenario=scenario)
        m = re.compile(filename_regex)
        ####################################################################################
        names = list()
        for ifile in ifiles:
            res = m.match(ifile)
            if res is None:
                LOGGER.error("File breaks naming scheme '%s': %s", filename_regex, ifile)
                return 0
            # read match groups
            model_name = res.group(2)
            time_res   = res.group(3)
            time_range = '{}{}'.format(res.group(4), res.group(5))
            # check
            if len(model_name) == 0:
                LOGGER.error(f"Cannot extract model name from: {ifile}")
                return 0
            # store
            names.append('{}_{}_{}'.format(model_name, time_res, time_range))
        # store all
        models_names_dict[var] = names

    if 1 != len(set([ len(names) for names in models_names_dict.values() ])):
        LOGGER.warning(f"Mismatch in model provided by {input_vars} for scenario {scenario}")
        # TODO log WARNING + work on models intersection ?
        if not lenient:
            raise RuntimeError("Input files mismatch for {input_vars} / {scenario}")
        else:
            # discard models which are not available for all vars:
            common_models     = set.intersection(*map(set, models_names_dict.values()))
            models_names_dict = models_names_dict.fromkeys(models_names_dict.keys(), common_models)
            LOGGER.debug("%d intersecting models found.", len(common_models))

    # [!] keep it sorted as sorted is also the models files listing in models_paths_dict
    models_names = sorted(set([ el for ls in models_names_dict.values() for el in ls ]))

    # (model name) -> { var1:model_path, var2:model_path ... }
    model_name2file = dict.fromkeys(models_names)
    for name in models_names:
        i = models_names.index(name)
        model_name2file[name] = dict(zip(input_vars, [ el[i] for el in models_paths_dict.values() ]))

    return model_name2file

# ------------------------------------------------------------------------------
# file names naming scheme

def __nc_name_rgx(varname:str=None, modelname:str=None, timeres:str=None,
        yearstart:int=None, yearend:int=None, scenario:str=None, extratxt:str=None):
    """
    Returns the regular expression matching the name of an input NetCDF projection file.
    The naming scheme of all temperature and precipitation input files is as follows:

        <varname>_<modelname>_<timeres>_<yearstart><yearend>_<scenario>[_<extratxt>].nc

    Being:
        1. <varname>   : the name of the variable of the dataset (eg. pr, tasmin)
        2. <modelname> : the name of the model used for the projection
                      (eg. CNRM-CERFACS-CNRM-CM5_CLMcom-CCLM4-8-17_r1i1p1_v1)
        3. <timeres  > : temporal resolution of each time step (eg. day)
        4. <yearstart>
        5. <yearend>   : start/end years (YYYY) of the time-series (eg. 1970)
        6. <scenario>  : the name of the projection's scenario (eg. rcp85)
        7. <extratxt>  : optional extra text

    The regular expression is designed so to let extract each information piece
    via match group, whose number is equal to that of the listing above.

    More specific pattern matching can be achieved by specifying input arguments.

    Example
    -------
    >>> rgx = __nc_name_rgx()
    >>> m = re.compile(rgx)
    >>> res = m.match('pr_EUR-11_ICHEC-EC-EARTH_CLMcom-ETH-COSMO-crCLIM-v1-1_r12i1p1_v1_day_19702100_rcp85.nc')
    >>> res.group(1)
    'pr'
    >>> res.group(6)
    'rcp85'

    >>> rgx = __nc_name_rgx(varname='tasmin', scenario='rcp45')
    >>> m = re.compile(rgx)
    >>> res = m.match('pr_EUR-11_ICHEC-EC-EARTH_CLMcom-ETH-COSMO-crCLIM-v1-1_r12i1p1_v1_day_19702100_rcp85.nc')
    >>> res is None
    True
    >>> res = m.match('tasmin_EUR-11_ICHEC-EC-EARTH_CLMcom-ETH-COSMO-crCLIM-v1-1_r12i1p1_v1_day_19702100_rcp45.nc')
    >>> res.group(2)
    'EUR-11_ICHEC-EC-EARTH_CLMcom-ETH-COSMO-crCLIM-v1-1_r12i1p1_v1'
    """
    # translate None to regex "anything"
    varname   = '[a-zA-Z0-9]+' if varname is None else varname
    modelname = '[a-zA-Z0-9-_]+' if modelname is None else modelname
    timeres   = '[a-zA-Z0-9]+' if timeres is None else timeres
    yearstart = '[0-9]{4}' if yearstart is None else yearstart
    yearend   = '[0-9]{4}' if yearend is None else yearend
    scenario  = '[a-zA-Z0-9]+' if scenario is None else scenario
    extratxt  = '[a-zA-Z0-9-_]*' if extratxt is None else extratxt

    # create regex
    nc_rgx = NETCDF_NAMING_SCHEME.format(
                 varname, modelname, timeres,
                 yearstart, yearend, scenario, extratxt)
    return nc_rgx

# ------------------------------------------------------------------------------
# file names naming scheme

# ------------------------------------------------------------------------------
#
def build_nc_dict(nc_filename:str):
    """
    Extracts the information encoded in NetCDF climate time-series files.

    Parameters
    ==========
    nc_filename:str
        The basename of the NetCDF sample file.

    Returns
    =======
    A dictionary containing the information extracted from the input file name.
    """
    rgx = __nc_name_rgx()

    m   = re.compile(rgx)
    res = m.match(nc_filename)

    if res is None:
        return None

    if len(res.groups()) != 7:
        raise RuntimeError(f"NC regex expects 6 groups. Found: {len(res.groups())}")

    nc_dict = {
        'varname'  : res.group(1),
        'model': res.group(2),
        'timeres'  : res.group(3),
        'yearstart': res.group(4),
        'yearend'  : res.group(5),
        'scenario' : res.group(6)
    }

    return nc_dict

# ------------------------------------------------------------------------------
#
def build_metadata_cdo_chain(index_conf):
    """
    Sets the CDO operators chaining that can be used to set the
    metadata fields of an index.
    """

    if len(index_conf.name) == 0:
        raise RuntimeError("Missing name attribute in index conf.")

    INDEX = index_conf.name

    missing_fields = [el for el in NC_MD_FIELDS if el not in index_conf]
    if 0 != len(missing_fields):
        raise ValueError(f"Missing metadata fields in {INDEX} configuration: {missing_fields}")

    cdo_md = ['-setattribute']
    cdo_md.append("{}=\"{}\"".format(TITLE_ATTR,   index_conf[NC_TITLE].replace("\n", " ")))
    cdo_md.append("{}=\"{}\"".format(INST_ATTR,    index_conf[NC_INSTI].replace("\n", " ")))
    cdo_md.append("{}=\"{}\"".format(SRC_ATTR,     index_conf[NC_SOURC].replace("\n", " ")))
    cdo_md.append("{}=\"{}\"".format(HISTORY_ATTR, index_conf[NC_HISTO].replace("\n", " ")))
    cdo_md.append("{}=\"{}\"".format(REFS_ATTR,    index_conf[NC_REFER].replace("\n", " ")))
    cdo_md.append("{}=\"{}\"".format(COMMENT_ATTR, index_conf[NC_COMMN].replace("\n", " ")))
    cdo_md.append("{}=\"{}\"".format(FREQ_ATTR,    index_conf[NC_FREQN].replace("\n", " ")))
    cdo_md.append("\"{}\"@{}=\"{}\"".format(INDEX, LNAME_ATTR, index_conf[NC_LONGN]))
    if (len(index_conf[NC_STNDN]) > 0):
        cdo_md.append("\"{}\"@{}=\"{}\"".format(INDEX, SNAME_ATTR, index_conf[NC_STNDN]))
    set_attrs = ",".join([ attr.replace(',','\,') for attr in cdo_md ]) # escape commas

    cdo_md = [set_attrs]
    # http://cfconventions.org/Data/cf-conventions/cf-conventions-1.7/cf-conventions.html#units -> Dimensionless Variables
    unit = '1' if len(index_conf[NC_UNITS]) == 0 else index_conf[NC_UNITS] # otherwise CDO asks for unit interactively
    cdo_md.append("-setunit,\"{}\"".format(unit))
    #cdo_md.append("-setunit,".format(index_conf[NC_UNITS])) # DEGUG SIGINT
    cdo_md.append("-setname,\"{}\"".format(INDEX))

    # ref, time: some CDO operators silently shift the time datum, so we need to re-set it
    reftime = index_conf[NC_REFTIME].split(DATETIME_FS)
    cdo_md.append("-setreftime,\"{0}\",\"{1}\"".format(reftime[0], reftime[1]))

    # TODO remove spurious global attributes
    # > cdo delete,param="Title,Created on"  ifile.nc ofile.nc # NOT WORKING

    return " ".join(cdo_md)

# ------------------------------------------------------------------------------
#
def replace_keywords(string:str, keywords:dict, camelcase=None):
    """
    Given a string with possible $-signed keywords, replace them with
    their actual value.

    Parameters
    ==========
    string: str
        The input string containing $-signed keywords
    keywords: dict
        Dictionary of keywords (**$-signed excluded**) and their actual value.
    camelcase: list
        List of keywords whose words should be capitalized ('hello ugly world' -> 'Hello Ugly World')

    Returns
    =======
    The input string, where all keywords where replaced by their value,
    as per given input dictionary.

    Example
    =======
    >>> replace_keywords('Hello $name!', {'name':'Otto'})
    Hello Otto!
    """

    if type(camelcase) is str:
        camelcase = [camelcase]

    for key in camelcase:
        if key in keywords:
            keywords[key] = ' '.join(word.capitalize() for word in keywords[key].split())

    for k,v in keywords.items():
        string = string.replace('${}'.format(k), v) # replaces all occurrences

    return string

# ------------------------------------------------------------------------------
#
def build_kw_dict(index_conf, sample_nc_name):
    """
    Creates the dictionary of allowed keywords that can be
    used in the configuration of an index ($-signed).
    This dictionary includes all fields of the index configuration itself,
    plus the fields encoded in the name of the sample file.

    Parameters
    ==========
    index_conf: Section
        The configuration of the index (from configparser)
    sample_nc_name: str or Path
        The name of a sample input or output NetCDF file name,
        which encodes multiple information like emissions scenario,
        model name, etc.

    Returns
    =======
    A dictionary where keys are keywords ($-sign excluded), and values
    are their actual values.
    """
    # TODO input check

    kw_dict = dict(index_conf)
    nc_dict = build_nc_dict(sample_nc_name)

    if nc_dict is not None:
        kw_dict.update(nc_dict)
    # else: RuntimeError? be pedantic on input file name?

    return kw_dict

# ------------------------------------------------------------------------------
#
def format_created_on_attr(timestamp=None, fmt=CREATED_ON_FMT) -> str:
    """
    Formats the "Created on" attribute.

    Parameters
    ==========
    timestamp : (optional) str or datetime
        The target time to be formatted (now-time if `None`)

    fmt : str
        The timestamp format (see `datetime.strftime`)

    Returns
    =======
    The "Created on" attribute.
    """
    attr = "\"{}\"=\"{}\"".format(CREATED_ATTR, format_datetime( timestamp, fmt=fmt ) )

    return attr

# ------------------------------------------------------------------------------
#
def add_or_append_attr(data, attr:str, value, fs=', '):
    """
    Adds or appends an attribute to an input xarray data structure.

    Parameters
    ==========
    data : xr.DataArray or xr.Dataset
        The data structure to be edited. If a dataset is provided
        then the attirbute will be "global", whereas with DataArrays
        the attribute is going to be variable-specific.

    attr : str
        The name of the attribute to be added/modified.

    value : any
        The value of the attribute to be added/appended.

    fs : char or str
        The Field Separator, to be used when the attribute already exists
        in the dataset.
 
    Returns
    =======
    The final attribute value stored (including possible existing prepended values).

    Example
    -------
    >>> add_or_append_attr(ds['temp'], "coordinates", "lat")
    lat
    >>> add_or_append_attr(ds['temp'], "coordinates", "lon", fs=' ')
    lat lon
    """
    # - - - - - - - - - -
    if data is None:
        return None

    if attr is None:
        raise ValueError("Please provide an attribute.")

    if (not isinstance(data, xr.Dataset) and
        not isinstance(data, xr.DataArray)):
           raise ValueError("Input data shall be an xarray data structure.")
    # - - - - - - - - - -

    if attr in data.attrs and data.attrs[attr] != "None":
        data.attrs[attr] += f"{fs} {value}"
    else:
        data.attrs[attr] = f"{value}"

    return data.attrs[attr]


# ------------------------------------------------------------------------------
#
def drop_attr(ds:xr.Dataset, attr:str, var=None):
    """
    Drops an attribute from the input dataset, if found.
    Nothing happens if the attribute is not found.

    Parameters
    ==========
    data : xr.Dataset
        The data structure to be edited.

    attr : str
        The name of the attribute to be dropped.

    var : str or list or 'all' (default: None)
        The variable(s) whose attribute shall be dropped;
        set to None to imply a global variable, or 'all'
        to remove the attribute from all variables found (not global attributes)
 
    Returns
    =======
    The value(s) of the attribute(S) that were dropped, None when not found.

    Example
    -------
    >>> drop_attr(ds, "grid_mapping", var='amt')
    'lambert_azimuthal_equal_area'
    >>> drop_attr(ds, "long_name", var='all')
    ['extreme precipitation total (95-th wet days)', 'y coordinate of projection', 'x coordinate of projection']
    >>> drop_attr(ds, "this_is_an_impossible_global_attribute")
    >>>
    """
    # - - - - - - - - - -
    ALL ='all'

    if ds is None:
        return None

    if attr is None:
        raise ValueError("Please provide an attribute.")

    if (var is not None) and var != ALL and (var not in ds):
        raise ValueError("'{}' not found in input data. Available variables: {}".format(var, [v for v in ds]))

    if not isinstance(ds, xr.Dataset):
        raise ValueError("Input data shall be an xarray Dataset.")

    if var == ALL:
        var = [v for v in ds]

    if not isinstance(var, list):
        var = [var]
    # - - - - - - - - - -

    attr_value = list()

    for v in var:
        attrs = ds.attrs if v is None else ds[v].attrs
        if attr in attrs:
            attr_value.append( attrs[attr] )
            del attrs[attr]

    return attr_value if len(attr_value) != 1 else attr_value[0]

# ------------------------------------------------------------------------------
# misc

def _index_odir(root, index, scenario):
    """The directory where to store the indices of the given input conditions."""
    return root / index / scenario

def _index_ofile(index, scenario, model):
    """The (base)name of the NetCDF file storing the index of the given input conditions."""
    return f'{index}_{model}_{scenario}.nc'

def _tmp_odir(root, index, scenario, model):
    """The directory where to store temporary results of the given input conditions."""
    return _index_odir(root, index, scenario) / model

def _tmp_filename(scenario, index, year):
    return f'{index}_{scenario}_{year}{NETCDF_EXT}'

def _tmp_file_regex(scenario, index):
    return f'{index}_{scenario}_*{NETCDF_EXT}'

def _subdict(input_dict, sub_keys):
    """Extracts items from input dictionary whose keys are listed in sub_keys."""
    sub_dict = { key:value for key, value in input_dict.items() if key in sub_keys }
    return sub_dict

def trunc(string, max_chars, ellipsis='...'):
    """Prints the input string, truncating it to its first max_chars character if longer."""
    if string is None:
        return None
    truncated = string if len(string)<max_chars else f'{string[:max_chars]}{ellipsis}'
    return truncated

def to_number(xx):
    """Parses (each element of a list of) strings to an integer/float number(s)."""
    if type(xx) == str:
        xx = [xx]
    return [None if x is None else int(x) if x.isdigit() else float(x) for x in xx]

def glob_or(pathname, patterns=list()):
    """Same as pathlib.glob but with multiple OR-wise patterns."""
    pathname = Path(pathname)
    matched  = list()
    for p in patterns:
        matched.extend( list(pathname.glob(p)) )
    return list(set(matched))

def format_datetime(timestamp=None, fmt=CREATED_ON_FMT) -> str:
    """Formats a timestamp (fallback: current time)"""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime( fmt )

def lambda_raise(ex):
    """`raise` call that can be used inside lambda functions."""
    raise ex

def argparse_check_positive(value):
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError("%s is not a positive integer" % value)
    return ivalue
# ------------------------------------------------------------------------------
