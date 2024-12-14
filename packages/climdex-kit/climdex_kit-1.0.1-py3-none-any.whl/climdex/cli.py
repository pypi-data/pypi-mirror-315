#!/usr/bin/env python
"""
Command line arguments parsers.
"""

import argparse
import logging

from pathlib import Path

from climdex._version import version
from climdex.constants import (
        PARALLELISM_KWDS, INDICES_ALL,
        DEFAULT_INDEXCONF_PATH, LOGGING_CONF,
        DEFAULT_SIGNIFICANCE_CONF)
from climdex.actions import compute, list as ls, show, analyse, mlut
from climdex.nc import NETCDF_RGX
from climdex.utils import MODULE_PATH
from climdex.analyse.enums import FmtType
from climdex import indices, utils

# ------------------------------------------------------------------------------
#
def climdex_parser():
    """Main parser for the climdex tool."""

    parser = argparse.ArgumentParser(
        prog="climdex",
        description="Compute one or more climate indices on time-series of temperature and precipitation forecasts.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    #
    # action-independent args
    #
    # --list turned to {list,ls} sub-command
    #parser.add_argument('-l', '--list', help="List all indices",
    #    action='store_true',
    #    required=False)

    parser.add_argument('-d', help="Enable debug mode (append multiple 'd' for more verbose debugging)",
         action='store_true',
         dest='debug',
         required=False) # SET LOGGING LEVEL/HANDLER [+cdo.debug=True]

    parser.add_argument('--version', help="Get the version number of the program",
        action='version',
        version=f'%(prog)s {version}')

    # TODO (and mind the -d debug mode option)
    #parser.add_argument('-v', '--verbose',
    #    action='store_true',
    #    required=False)

    # alternative indices.ini file
    parser.add_argument('-c', '--idx-conf',
        help="Alternative indices configuration file (.ini)",
        type=str,
        dest='idx_conf',
        default=indices.settings_path,
        required=False)

    # alternative logging.yaml file
    parser.add_argument('-L', '--log-conf',
        help="Alternative logging configuration file (.yaml)",
        type=str,
        dest='log_conf',
        default=Path(MODULE_PATH, LOGGING_CONF),
        required=False)

    # TODO
    # colored output switch

    #
    # sub-parsers
    #
    actions_subparsers = parser.add_subparsers(
            title='actions',
            description='valid actions to execute',
            dest='action_name')
            #parser_class=CustomArgumentParser)

    #
    # sub-commands
    #
    co_parser = add_climdex_co_subparser( actions_subparsers )
    ls_parser = add_climdex_ls_subparser( actions_subparsers )
    sh_parser = add_climdex_sh_subparser( actions_subparsers )
    lu_parser = add_climdex_lu_subparser( actions_subparsers )
    an_parser = add_climdex_an_subparser( actions_subparsers )

    return parser

# ------------------------------------------------------------------------------
#
def add_climdex_co_subparser(subparsers_group):
    """Adds the sub-parser of the {compute,co} action to the given group of sub-parsers."""

    compute_parser = subparsers_group.add_parser('compute', aliases=['co'])
    compute_parser.set_defaults(
            validate=compute.validate_args,
            run=compute.run)

    compute_parser.add_argument('-i', '--index', help="Indices to compute (comma-separated list, see {list,ls} for a full listing)",
        #choices = [ INDICES_ALL ] + indices.list_indices(), clutter the help: do manually
        action=IndicesListAction, #"extend",
        nargs="?", # should be +, but to have compat help, I'll manually -> required
        default='',
        type=str)

    compute_parser.add_argument('--multiprocessing',
        help="CPU parallelism: set either a keyword among {} or the desired number of CPU/cores."
            .format(PARALLELISM_KWDS),
        type=str, #choices=PARALLELISM_KWDS,
        default='1', # no parallelism by default
        required=False)

    # input dir
    compute_parser.add_argument('--idir',
        help="Root folder where to look for input files (expected structure: $input_dir/variable/scenario/*.nc).",
        required=True)

    # output dir
    compute_parser.add_argument('-o', '--odir',
        help="Root folder where to store indices files tree.",
        required=True)

    # scenario
    compute_parser.add_argument('-s', '--scenario',
        help="White-space separated list of scenarios (it shall coincide with input sub-folder name)",
        action='extend',
        type=str,
        nargs='+')

    # filter
    compute_parser.add_argument('-x', '--regex',
        help="Filter input files with regex expression (NOTE: regex will be used as-is: no '*' signs will be prepended/appended).",
        default=NETCDF_RGX,
        type=str,
        required=False)

    # metadata_only
    compute_parser.add_argument('-m', '--metadata-only',
        help="Only re-set the output attributes (metadata) on existing indices files.",
        action='store_true',
        dest='metadata_only',
        required=False)

    # dry_run
    compute_parser.add_argument('-n', '--dry-run',
        help="Dry-run: only print jobs to output without doing anything.",
        action='store_true',
        dest='dry_run',
        required=False)

    # force
    compute_parser.add_argument('-f', '--force',
        help="Force overwrite of existing output indices files and tmp folders (otherwise execution is stopped).",
        action='store_true',
        required=False)

    return compute_parser

# ------------------------------------------------------------------------------
#
def add_climdex_ls_subparser(subparsers_group):
    """Adds the sub-parser of the {list,ls} action to the given group of sub-parsers."""

    list_parser = subparsers_group.add_parser('list', aliases=['ls'])
    list_parser.set_defaults(
            validate=ls.validate_args,
            run=ls.run)

    # TODO any filtering option for instance?

    return list_parser

# ------------------------------------------------------------------------------
#
def add_climdex_sh_subparser(subparsers_group):
    """Adds the sub-parser of the {show,sh} action to the given group of sub-parsers."""

    show_parser = subparsers_group.add_parser('show', aliases=['sh'])
    show_parser.set_defaults(
            validate=show.validate_args,
            run=show.run)

    show_parser.add_argument('index',
        help="The index to be shown (see {list,ls} for a full listing)",
        action='store')

    return show_parser

# ------------------------------------------------------------------------------
#
def add_climdex_lu_subparser(subparsers_group):
    """Adds the sub-parser of the {mlut} action to the given group of sub-parsers."""

    mlut_parser = subparsers_group.add_parser('mlut', aliases=[])
    mlut_parser.set_defaults(
            validate=mlut.validate_args,
            run=mlut.run)

    return mlut_parser

# ------------------------------------------------------------------------------
#
def add_climdex_an_subparser(subparsers_group):
    """Adds the sub-parser of the {analyse,an} action to the given group of sub-parsers."""

    analyse_parser = subparsers_group.add_parser('analyse', aliases=['an'])
    analyse_parser.set_defaults(
            validate=analyse.validate_args,
            run=analyse.run)

    analyse_parser.add_argument('-t', '--type',
        help="Type of analysis to be requested.",
        choices=analyse.TYPES,
        required=True)

    analyse_parser.add_argument('-i', '--index',
        help="Indices to analyse (comma-separated list, see {list,ls} for a full listing)",
        action=IndicesListAction, #"extend",
        nargs="?", # should be +, but to have compat help, I'll manually -> required
        default='',
        type=str)

    analyse_parser.add_argument('--src-type',
        help="The type of the source of indices: either file-based or as online catalogue.",
        choices=analyse.SOURCES,
        required=True)

    analyse_parser.add_argument('--src',
        help="""Source of the climate indices: either a URL of the openeo/wcps endpoint, or the folder where to look
                for input files (expected structure: $input_dir/variable/scenario/*.nc).""",
        required=True)

    analyse_parser.add_argument('-o', '--odir',
        help="Root folder where to store the output file(s) (use - for stdout)",
        default=".",
        required=False)

    analyse_parser.add_argument('--o-fs-routing',
        dest="ofs_routing",
        help="Employ file system routing in output files, with --odir as root), on index and scenario values.",
        action='store_true',
        required=False)

    analyse_parser.add_argument('--oformat',
        help="Format of the 1+ requested outputs.",
        choices=FmtType.values(),
        #default=FmtType.nc.value, -> analysis modules set their default
        required=False)

    analyse_parser.add_argument('-s', '--scenario',
        help="White-space separated list of scenarios (it shall coincide with input sub-folder name)",
        action='extend',
        type=str,
        nargs='+')

    analyse_parser.add_argument('-m', '--model',
        help="White-space separated list of climate models indices (see 'python -m climdex mlut')",
        action='extend',
        type=str,
        nargs='+')

    analyse_parser.add_argument('--ifreq',
        help="Input time frequency",
        required=False) # TODO is this necessary?

    analyse_parser.add_argument('--multiprocessing',
        help="CPU parallelism: set either a keyword among {} or the desired number of CPU/cores."
            .format(PARALLELISM_KWDS),
        type=str, #choices=PARALLELISM_KWDS,
        default='1', # no parallelism by default
        required=False)


    analyse_parser.add_argument('-n', '--dry-run',
        help="Dry-run: only print jobs to output without doing anything.",
        action='store_true',
        dest='dry_run',
        required=False)

    analyse_parser.add_argument('-f', '--force',
        help="Force overwrite of existing output indices files and tmp folders (otherwise execution is stopped).",
        action='store_true',
        required=False)

    analyse_parser.add_argument('-l', '--lenient',
        help="Silently accept empty outputs when input filters are not overlapping with input domain (otherwise exceptions are raised).",
        action='store_true',
        required=False)

    #
    # actual analysis definition
    #

    analyse_parser.add_argument('--tint', metavar="t0[,t1]",
        help="Time filter in the form of a single time step 't' or a time interval 't0,t1'", # TODO make it also ",t1" for T-trends
        action='extend',
        type=str,
        nargs='*')

    analyse_parser.add_argument('--bbox', metavar="xmin,ymin,xmax,ymax",
        help="Horizontal bounding-box filter in data native projection.",
        required=False)

    analyse_parser.add_argument('--wgs84-bbox', metavar="lat_min,lon_min,lat_max,lon_max",
        help="Horizontal latitude-longitude WGS84 bounding-box filter.",
        dest='wgs84_bbox',
        required=False)

    analyse_parser.add_argument('--clip', metavar="{WKT || path}",
        help="Well-Known Text (WKT) or path to a geospatial file containing geometries for spatial clipping.",
        required=False)

    analyse_parser.add_argument('--clip-id', metavar='FIELD',
        help="(if clip is path to a file with geometries) The field in the provided clipping file which serves as ID for the geometries. Ordinal numbers are used if missing.",
        required=False)

    analyse_parser.add_argument('--clip-limit', metavar='N',
        help="Limit the clipping to the first N geometries (more for testing purposes).",
        type=utils.argparse_check_positive,
        required=False)

    analyse_parser.add_argument('--clip-split',
        help="Flag argument to store in separate files the analysis outputs of each input clip geometry of --clip argument.",
        action='store_true',
        required=False)

    analyse_parser.add_argument('--hfilter', metavar="[h],[H]",
        help="Minimum/maximum height (altitude) filter (omit one of the values to remove constraint). A DEM file must be provided: see --dem.",
        required=False)

    analyse_parser.add_argument('--dem',
        help="Path to the Digital Elevation Model (DEM) to be used to filter ranges of altitude/height.",
        required=False)

    analyse_parser.add_argument('--baseline', metavar="t0,t1",
        help="Time interval to be used as baseline reference (use in association with --tint and --baseline-op).",
        required=False)

    analyse_parser.add_argument('--baseline-op',
        help="Operation to be computed with respect to the baseline (see --baseline).",
        choices=analyse.BASELINE_OPS,
        dest="baseline_op",
        required=False)

    # TODO accept multiple aggregations to be run in batch
    analyse_parser.add_argument('--xyaggr',
        help="Spatial (horizontal) aggregation type (accepts: avg, med, min, max, qX, pXX, range, perc_pos, perc_neg).",
        action='extend',
        type=str,
        nargs='*')

    # TODO accept multiple aggregations to be run in batch
    analyse_parser.add_argument('--taggr',
        help="""
            Temporal aggregation type (accepts: avg, med, min, max, qX, pXX, range, perc_pos, perc_neg).
            Applied on trends only with multiple input --tint intervals.""",
        action='extend',
        type=str,
        nargs='*')

    # not relevant use-case:
    #analyse_parser.add_argument('--saggr',
    #    help="Scenarios aggregation type (accepts: avg, med, min, max, qX, pXX, range, perc_pos, perc_neg).",
    #    action='extend',
    #    type=str,
    #    nargs='*')

    analyse_parser.add_argument('--eaggr',
        help="Ensemble aggregation type (accepts: avg, med, min, max, qX, pXX, range, perc_pos, perc_neg).", # TODO only at least 3 models
        action='extend',
        type=str,
        nargs='*')

    # statistical significance test
    analyse_parser.add_argument('--significant', metavar='DIM',
        help="""Work only on statistically significant pixels, applying statistical significance (Wilconcox)
                tests along the provided dimension(s). See '--conf-level' for customising confidence level of test.""",
        required=False,
        action='extend',
        type=str,
        nargs='+')

    analyse_parser.add_argument('--conf-level',
        dest='conf_level',
        help=f"Confidence level for statistical significance test ('--significant' argument) (default {DEFAULT_SIGNIFICANCE_CONF}%%)",
        #default=DEFAULT_SIGNIFICANCE_CONF -> apply it downstream, so I can alert user when conf level is given and significant argument no
        type=int,
        required=False)

    analyse_parser.add_argument('--perc-pos', metavar='PERC',
        dest='perc_pos',
        help="Keep only the values in the ensemble where PERC%% of the pixels is positive (>0).",
        type=int,
        required=False)

    analyse_parser.add_argument('--perc-neg', metavar='PERC',
        dest='perc_neg',
        help="Keep only the values in the ensemble where PERC%% of the pixels is negative (<0).",
        type=int,
        required=False)

    #
    # output formatting options
    #
    analyse_parser.add_argument('--decimals', metavar='N',
        help="Number of decimal places to round the output values to.",
        type=utils.argparse_check_positive,
        required=False)

    analyse_parser.add_argument('--datetime-unit', metavar='UNIT',
        dest='dt_unit',
        help="The resolution of the formatted timestamp coordinates in the output file.",
        choices=('Y','M','W','D','h','m','s','ms','ns','auto'), # https://numpy.org/doc/stable/reference/arrays.datetime.html#datetime-units
        required=False)

    analyse_parser.add_argument('--discard-attrs',
        help="Discard metadata attributes of input climate indices on the output files.",
        dest='keep_attrs',
        action='store_false')

    analyse_parser.add_argument('--discard-clip-attrs',
        help="Discard metadata attributes of input spatial clipping on the output files.",
        dest='keep_clip_attrs',
        action='store_false')

    analyse_parser.add_argument('--json-indent', metavar='N',
        dest='json_indent',
        help="Indentation of output (geo)json files. Ignore argument for compact 1-line marshalling.",
        type=utils.argparse_check_positive,
        required=False)

    # TODO add --rolling=n_steps parameter -> xr.Dataset.rolling(... dim=TIME_DIM)
    # useful for: month-based indices (e.g. spi12), to get yearly trends ds.rolling(12).mean
    #         or: get seasonality (index - ds.rolling(12).mean)
    # ...

    return analyse_parser

# ------------------------------------------------------------------------------
#
def validate_climdex_args(args) -> bool:
    """
    Validate CLI arguments.
    """

    # index conf file exists
    idx_conf = Path(args.idx_conf)
    if not idx_conf.exists():
        raise ValueError(f"Indices configuration file could not be found: '{args.idx_conf}'.")

    # logging conf file exists
    if args.log_conf is not None:
        log_conf = Path(args.log_conf)
        if not log_conf.exists():
            raise ValueError(f"Logging configuration file could not be found: '{args.log_conf}'.")

    # action-specific checks
    args.validate(args)

    return True


# ------------------------------------------------------------------------------
#
class IndicesListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        #print('I give up')
        setattr(namespace, self.dest, values)

