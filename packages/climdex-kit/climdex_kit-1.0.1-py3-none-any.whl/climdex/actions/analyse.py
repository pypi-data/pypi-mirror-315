#!/usr/bin/env python

"""
Handler of the {analyse,an} action.
"""

import os
import sys
import argparse
import re
import signal
import json

from multiprocessing import Pool
from abc import ABC
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import geopandas as gpd
from shapely import wkt, box
from shapely import GEOSException

from climdex import indices, utils
from climdex.analyse import maps, trends, xarrays
from climdex.analyse.enums import AnalysisType, SrcType, OpType, FmtType
from climdex.analyse.utils import *
from climdex.constants import *
from climdex.utils import DebugLevels, MODULE_PATH

#
# constants
#

ANALYSIS_MODULES = {
    AnalysisType.map2d : maps,
    AnalysisType.trend : trends,
    AnalysisType.uncertainty : None
}

DEFAULT_OFMT = FmtType.stdout.value

# args
map_types = [AnalysisType.map2d.value]
trn_types = [AnalysisType.trend.value, 'trend']
unc_types = [AnalysisType.uncertainty.value, 'uncertainty']
TYPES = [*map_types, *trn_types, *unc_types]

SOURCES = [ *SrcType.values() ]

BASELINE_OPS = [ *OpType.values() ]

# parallelism
from multiprocessing import Lock
__lock__ = Lock()

# signals
# SIGPIPE: when redirecting output to file + CTRL-C (KeyboardInterrupt),
# then logging will raise a BrokenPipeError.
# Workaround: ignore the broken pipes, though logging does not
# happen in the KeyboardInterrupt exception handler. FIXME
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def validate_args(args) -> bool:
    """
    Arguments validation for the {analyse,an} action.
    """

    # analysis type
    # skip: argparse checks already in place

    # CSV string to list
    if len(args.index) == 0:
        raise ValueError("Please specify at least one climate index (--index arg)")
    args.index = args.index.split(',')

    LOGGER = utils.get_logger(__name__)
    LOGGER.info("To analyse %d indices: %s", len(args.index), args.index)

    # check 'all' keyword is not mixed with actual indices
    if INDICES_ALL in args.index:
        if len(args.index) > 1:
            raise ValueError("'{}' keyword among indices: please select either '{}' or valid indices."
                    .format(INDICES_ALL, INDICES_ALL))
            return False # or raise Exception?
        else:
            LOGGER.debug("Replacing '%s' with actual indices.", INDICES_ALL)
            args.index = indices.list_indices()

    # source of indices
    if args.src_type == SrcType.local:
        # check path exists
        sdir = Path(args.src)
        if not sdir.exists():
            raise ValueError("'{}' does not exist.".format(args,src))
    else:
        # check URL is alive
        u = urlparse(args.src)
        # ...

    # output dir
    is_stdout = (args.odir == FmtType.stdout.value)
    if not is_stdout:
        odir = Path(args.odir)
        if not odir.exists():
            LOGGER.debug("'%s' does not exist: creating it.", args.odir)
            if args.dry_run:
                LOGGER.info("[dry-run] mkdir '%s'", odir)
            else:
                try:
                    odir.mkdir(parents=True, exist_ok=False)
                except:
                    raise ValueError("Cannot create output folder '{}'. Check your permissions on the file system and retry.".format(odir))


    # check scenario exists
    # TODO find -type d -maxdepth 2 -name $scenario
    LOGGER.debug("Scenarios: %s", args.scenario)

    # parallelism
    if args.multiprocessing not in PARALLELISM_KWDS:
        try:
            args.multiprocessing = int(args.multiprocessing)
        except ValueError:
            raise ValueError("'%s' not recognized as multiprocessing option.")

    # time filter
    if args.tint is not None:
        LOGGER.debug("Input time interval(s): %s", args.tint)
        for i,tint in enumerate(args.tint):
            tint = [ s.strip() for s in tint.split(',') ]
            if len(tint) > 2:
                raise ValueError("Maximum 2 time steps allowed in --tint filter: {}".format(tint))
            elif len(tint) == 1:
                tint.append( tint[0] )
            args.tint[i] = tint
            LOGGER.debug("Target time interval: %s", args.tint[i])


    # baseline
    has_op = (args.baseline_op is not None)
    has_bl = (args.baseline is not None)
    if args.baseline is not None:
        args.baseline = [ s.strip() for s in args.baseline.split(',') ]
        if len(args.baseline) != 2:
            raise ValueError("2 time steps required in --baseline filter: {}".format(args.baseline))
        LOGGER.debug("Baseline time interval: %s", args.baseline)

    # spatial filter
    has_bbox = args.bbox is not None
    has_wg84 = args.wgs84_bbox is not None
    has_clip = args.clip is not None

    if (has_bbox + has_wg84 + has_clip) > 1:
        raise ValueError("Either specify at most one among a clipping geometry and a bounding-box (native coordinates or WGS84 lat/lon) filter.")
    if has_wg84:
        args.wgs84_bbox = [ s.strip() for s in args.wgs84_bbox.split(',') ]
        if len(args.wgs84_bbox) != 4:
            raise ValueError("WGS84 bounding box shall be 4 values. Found: {}".format(args.wgs84_bbox))
        LOGGER.debug("WGS84 latitude/longitude bbox: %s", args.wgs84_bbox)
    elif has_bbox:
        args.bbox = [ s.strip() for s in args.bbox.split(',') ]
        if len(args.bbox) != 4:
            raise ValueError("Bounding box shall be 4 values. Found: {}".format(args.bbox))
        LOGGER.debug("Native-coordinates bbox: %s", args.bbox)

    # clip geometry
    clip_geom = None
    if has_clip:
        try:
            args.clip = args.clip.strip() # JIC
            clip_path = Path( args.clip )
            if clip_path.exists():
                if args.clip_id is None:
                    LOGGER.warn("Clipping file provided with no ID field set (--clip-id).")
            else:
                # direct command-line WKT string:
                clip_geom = wkt.loads( args.clip )
        except GEOSException as ex:
            raise ValueError("Invalid clipping geometry provided: {}".format(repr(ex)))
        LOGGER.debug("Clipping geometry parsed: %s", clip_geom)

    # height/altitude filter
    has_hfilter = (args.hfilter is not None)
    has_dem = args.dem is not None
    if has_hfilter and not has_dem:
        raise ValueError("Please specify a Digital Elevation Model (DEM, --dem arg) in order to filter pixels by altitude.")
    if has_dem and not has_hfilter:
        LOGGER.warn("Ignoring --dem argument as min/max height not specified.")
        args.dem = None
        has_dem = False
    if has_dem:
        args.dem = args.dem.strip()
        dem_path = Path( args.dem )
        if not dem_path.exists():
            raise ValueError("Provided DEM file not found: '{}'".format(args.dem))
        LOGGER.debug("DEM file: '%s'", dem_path )
    if has_hfilter:
        # turn string into [minh, maxh] array
        args.hfilter = [ s.strip() for s in args.hfilter.split(',') ]
        if len(args.hfilter) != 2:
            raise ValueError("Height filter shall have at most 2 values and must have comma. Found: {}".format(args.hfilter))
        args.hfilter = [ None if len(s)==0 else s for s in args.hfilter ]
        LOGGER.debug("Height (altitude) filter: %s", args.hfilter)

    # aggregation types
    for aggr_opt in [ args.xyaggr, args.taggr, args.eaggr ]:
        if aggr_opt is not None:
            for aggr_el in aggr_opt:
                LOGGER.debug("Checking aggregator: '%s'...", aggr_el)
                if not check_aggr_type(aggr_el):
                    ... # raise ValueError("Invalid aggregation type: {}".format(aggr_opt))
    if args.xyaggr is not None: LOGGER.debug("Spatial XY aggregation type: %s", args.xyaggr)
    if args.taggr  is not None: LOGGER.debug("Temporal T aggregation type: %s", args.taggr)
    if args.eaggr  is not None: LOGGER.debug("Ensemble E aggregation type: %s", args.eaggr)

    # stat significance
    if (args.significant is not None) and (args.conf_level is None):
        args.conf_level = DEFAULT_SIGNIFICANCE_CONF
        LOGGER.debug("Set default confidence level to %i\%.", args.conf_level)
    #
    if args.conf_level is not None:
        if args.significant is None:
            raise ValueError("Confidence level provided without specifying which dimension(s) where to apply the test (--significant).")
        if args.conf_level not in range(1,100):
            raise ValueError("Confidence level must be in [1-99] range [%]: {}".format(args.conf_level))
        if args.conf_level < 60:
            if args.lenient:
                LOGGER.warn("Unusual confidence level found: %d%% (typical values are 95%%, 99%%).", args.conf_level)
            else:
                raise ValueError("Invalid confidence level found [%]: {} (use --lenient to allow the analyis anyway)".format(args.conf_level))
    if (args.significant is not None) and (args.baseline is None):
        raise ValueError("Missing baseline for the requested statistical significance test.")

    if (args.perc_pos is not None) and (args.perc_neg is not None):
        raise ValueError("Cannot provide both perc_pos and perc_neg arguments.")

    for p in [args.perc_pos, args.perc_neg]:
        if p is not None and p not in range(1,101):
            raise ValueError("Percentage filter  must be in [1-100] range [%]: {}".format(p))

    return True


# ------------------------------------------------------------------------------
#
def run(args) -> bool:
    """
    Executes the configured {analyse,an} action.
    """
    # to dict: >>> vars(args)

    # reload logger (level might have changed) # FIXME debug option setting should be done before logger is loaded
    LOGGER = utils.get_logger(__name__)

    # print header with all configuration
    LOGGER.debug("Executing '%s' analysis now for indices: %s", args.type, args.index)

    # PRINT HEADER with all input conditions
    log_header()

    tasks_ok = tasks_error = 0

    # TODO enable multiprocessing for parallel extraction of N outputs
    try:
        # FIXME encapsulate this
        if args.type in map_types:
            an_type = AnalysisType.map2d
        elif args.type in trn_types:
            an_type = AnalysisType.trend
        elif args.type in unc_types:
            an_type = AnalysisType.uncertainty
        else:
            LOGGER.error("[!] Unreachable.")
            raise RuntimeError("Unhandled '{}' type".format(args.type));

        worker = AnalysisWorker()
        worker.setup()

        LOGGER.debug("%s requested...", an_type.name.upper())
        tasks_ok, tasks_error = worker.extract_information(
                an_type   = an_type,
                indices   = args.index,
                scenarios = args.scenario,
                src_type  = args.src_type,
                src       = args.src,
                odir      = args.odir,
                ofs_routing = args.ofs_routing,
                oformat     = args.oformat,
                cpus        = args.multiprocessing,
                models      = args.model,
                baseline    = args.baseline,
                baseline_op = args.baseline_op,
                tint        = args.tint,
                bbox        = args.bbox,
                wgs84_bbox  = args.wgs84_bbox,
                xyclip      = args.clip,
                xyclip_id   = args.clip_id,
                xyclip_limit= args.clip_limit,
                xyclip_split= args.clip_split,
                hfilter     = args.hfilter,
                dem         = args.dem,
                taggr       = args.taggr,
                eaggr       = args.eaggr,
                xyaggr      = args.xyaggr,
                sign_test   = args.significant,
                sign_conf   = args.conf_level,
                perc_pos    = args.perc_pos,
                perc_neg    = args.perc_neg,
                decimals    = args.decimals,
                dt_coords_unit    = args.dt_unit,
                keep_attrs        = args.keep_attrs,
                keep_xyclip_attrs = args.keep_clip_attrs,
                json_indent       = args.json_indent,
                dry_run = args.dry_run,
                force   = args.force,
                lenient = args.lenient)

    except Exception as err:
        if utils.debug_level() > DebugLevels.NO_DEBUG:
            LOGGER.exception("ERROR: %s", err)
        else:
            LOGGER.error("ERROR: %s", err)

    finally:
        log_report(args.type, tasks_ok, tasks_error, args.dry_run)

    LOGGER.info("Analysis done.")

# ------------------------------------------------------------------------------

class AnalysisWorker(ABC):

    def __init__(self):
        self.LOGGER = utils.get_logger(__name__)
        #self.LOGGER.debug("ANWRK: %s", self.LOGGER)

    def setup(self):
        # report stats
        self.tasks_ok = 0
        self.tasks_error = 0

    def __repr__(self):
        return f'AnalysisWorker[{self}]'

    def __str__(self):
        return "AnalysisWorker"

    def __task_ok(self):
        """One of the tasks has ended successfully."""
        self.tasks_ok += 1 # TODO lock

    def __task_error(self):
        """One of the tasks has ended with error."""
        self.tasks_error += 1 # TODO lock

    def __pool_worker_initializer(self):
        """Ignore SIGINT handler for forked processes, so that SIGINT handler is inherited from parent."""
        #signal.signal(signal.SIGINT, signal.SIG_IGN)

    def __callback_ok(self, res):
        self.LOGGER.debug("%s done : %s", self, res) # TODO add index to params for tracing?
        self.__task_ok()

    def __callback_fail(self, exception):
        self.LOGGER.exception("Exception while executing a task.", exc_info=exception)
        self.__task_error()

    def __cleanup(self):
        ...

    def extract_information(self, an_type:AnalysisType, indices, scenarios, src_type, src, odir, oformat, ofs_routing=False, cpus=1, **kwargs):
        """
        Extracts one or more analysis outputs trends from input climate indices.
        See relayed functions on map, trends, etc. for full arguments description.

        Parameters
        ----------
        an_type : AnalysisType
            The type of analysis to carry out.

        indices : array_like
            Selection of climate indices where to compute the results.

        scenarios : array_like (optional)
            The selection of climate scenarios;
            `None` to select all available scenarios.

        src_type : SrcType or str
            The type of input climate indices data.
            Use `src` arg to specify the actual location of the data.

        src : str
            Either the path (on file-based data type) or the
            URL of the climte indices data endpoint.
            Use `src_type` arg to specify the type of inputs.

        odir : str or Path (optional)
            The path of the directory where to store the results;
            when `None` no file is stored.

        oformat : str (optional)
            The output format of the generated files (when odir is specified).

        ofs_routing : bool
            Whether to use file-system routing in output data structure
            (odir/index/scenario/ is actual output folder for files when True).

        cpus : int or str
            The level of CPU parallelism by either the number of CPU cores to use
            or by means of keyword (see PARALLELISM_KWDS).
            If set to 1/'one' the execution of the program will be synchronous.

        ** kwargs : dict
            Analysis-type-dependent arguments to be delegated to workers.

        Returns
        -------
        The [success,fail] output counters.
        """
        # - - - - - - - - - -
        if an_type is None:
            return None

        if len(indices) == 0:
            self.LOGGER.warning("No indices provided.")
            return 0,0

        # TODO fetch scenarios from input (local/openEO/wcps)
        if scenarios is None: 
            raise NotImplementedError("Fetching input scenarios is not implemented yet.");

        if type(cpus) is int:
            if cpus > MAX_CPUS:
                cpus = MAX_CPUS
                self.LOGGER.warning("Too many CPUs requested. Trimming to %s.", MAX_CPUS)
            ncpus = cpus
        else:
            if type(cpus) is str and cpus not in PARALLELISM_KWDS:
                raise ValueError(f"Invalid cpus argument: {cpus}. Please put either a number or one among: {PARALLELISM_KWDS}.")
            ncpus = utils.ncpus_of(cpus)

        synchronous = (ncpus == 1)
        # - - - - - - - - - -

        # kwargs
        dry_run = kwargs['dry_run'] if 'dry_run' in kwargs else False

        # parallelism
        if not synchronous:
            sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
            an_pool        = Pool(ncpus, self.__pool_worker_initializer)
            signal.signal(signal.SIGINT, sigint_handler)
            self.LOGGER.debug("Parallel processes pool initialized: %s", an_pool)

        # go:
        an_ok = an_err = 0
        i = 0
        try:
            # TODO pythonize this with more clever apply and array-like arg(s) and array-like arg(s)
            for index in indices:
                for scenario in scenarios:
                    try:
                        self.LOGGER.info("#%d) [%s]/%s...", i, index, scenario)
                        if not synchronous:
                        ### TASK CALL-BEGIN ################################################################################
                            opath = an_pool.apply_async(
                                        self.do_extract_information, # [!] shall not be private "__func()"
                                        kwds={
                                            'an_type'  : an_type,
                                            'index'    : index,
                                            'src_type' : src_type,
                                            'src'      : src,
                                            'scenario' : scenario,
                                            'odir'     : odir,
                                            'oformat'  : oformat,
                                            'ofs_routing' : ofs_routing,
                                            **kwargs
                                            },
                                        callback      = self.__callback_ok,
                                        error_callback= self.__callback_fail)
                        # --------------------------------------------------------------------------------------------------
                        else:
                            try:
                                opath = self.do_extract_information(
                                            an_type  = an_type,
                                            index    = index,
                                            src_type = src_type,
                                            src      = src,
                                            scenario = scenario,
                                            odir     = odir,
                                            oformat  = oformat,
                                            ofs_routing = ofs_routing,
                                            **kwargs)
                            except Exception as ex:
                                self.__callback_fail(ex)
                            else:
                                if not dry_run and opath is None:
                                    self.LOGGER.error("[%s]/%s analysis failed.", index, scenario)
                                    self.__task_error()
                                else:
                                    self.__task_ok()
                        # ASYNC CALL-END ####################################################################################
                        # ----------------------------------------------------------------------
                        i += 1
                    except Exception as ex:
                        self.LOGGER.error("A fatal error occurred: quitting...", exc_info=ex)
                        raise ex
                    finally:
                        self.LOGGER.info('|')

            if not synchronous:
                self.LOGGER.info("Waiting for operators tasks to join... ")
                an_pool.close()
                an_pool.join() # TODO deadlock here sometimes
                self.LOGGER.info("All operators tasks terminated.")

        except KeyboardInterrupt as err:
            if utils.debug_level() > DebugLevels.NO_DEBUG:
                self.LOGGER.exception("Interruption caught!")
            else:
                self.LOGGER.error("Interruption caught (%s)", err)
            if not synchronous:
                self.LOGGER.error("Terminating analysis...")
                an_pool.terminate()
                an_pool.join()
                self.LOGGER.info("All subprocesses terminated.")

        except Exception as err:
            if utils.debug_level() > DebugLevels.NO_DEBUG:
                self.LOGGER.exception("ERROR: %s", err)
            else:
                self.LOGGER.error("ERROR: %s", err)

        finally:
            self.__cleanup()

        return self.tasks_ok, self.tasks_error

    # ------------------------------------------------------------------------------

    def do_extract_information(self, an_type:AnalysisType, 
            index, src_type, src, scenario, odir=None, ofs_routing=False, oformat=DEFAULT_OFMT,
            models=None,    baseline=None,  baseline_op=None,
            tint=None,      bbox=None,      wgs84_bbox=None,
            xyclip=None,    xyclip_id=None, xyclip_limit=None, xyclip_split=False,
            hfilter=None,   dem=None,
            taggr=None,     eaggr=None,     xyaggr=None,
            sign_test=None, sign_conf=None,
            perc_pos=None,  perc_neg=None,
            decimals=None,  dt_coords_unit=None,
            keep_attrs=True, keep_xyclip_attrs=True, json_indent=None,
            lenient=False,  dry_run=False,  force=False):
        """
        Sub-routine to extract a single analysis dataset from a climate index.

        Parameters
        ----------
        an_type : AnalysisType
            The type of analysis to carry out.

        index : str
            The identifier of the climate index input.

        src_type : SrcType or str
            The type of input climate indices data.
            Use `src` arg to specify the actual location of the data.

        src : str
            Either the path (on file-based data type) or the
            URL of the climte indices data endpoint.
            Use `src_type` arg to specify the type of inputs.

        scenario : str
            The target climate scenario.

        odir : str or Path (optional)
            The path of the directory where to store the results;
            when `None` no file is stored.

        oformat : str (optional)
            The output format of the generated files (when odir is specified).

        models : str, int, or array_like (optional)
            A single target ensemble model (see LUT); when `eaggr` is set, either specify
            a selection of models to which to apply the aggregation, or `None`
            to aggregate over all available models in the ensemble.

        baseline : array_like (optional)
            [tmin,tmax] array of time steps the define the baseline of the analysis;
            use the `baseline_op` to define the type of comparison to be applied.

        baseline_op : str or OpType (optional)
            The type of operation to be applied with respect to the `baseline`:
            `TARGET baseline_op BASELINE`.

        tint : (one or more) str or array_like (optional)
            The target [tmin,tmax] time-step(s); `None` to include all available
            input time-steps in the analysis.

        bbox : [xmin,ymin,xmax,ymax] (optional)
            The spatial filter (coordinates shall be expressed in input-native CRS).
            `None` to select the full spatial extent of the inputs or to use
            other spatial filter options like `wgs84_bbox` or `xyclip`.

        wgs84_bbox : [lat_min,lon_min,lat_max,lon_max] (optional)
            The spatial filter (coordinates shall be expressed in WGS84 latitude/longitude degrees).
            `None` to select the full spatial extent of the inputs or to use
            other spatial filter options like `bbox` or `xyclip`.

        xyclip : Path or str (optional)
            The spatial clipping filter, either as a spatially explicit file or a
            (latitude/longitude) WKT string.
            Each geometry found in the clipping will generate a separate dataset,
            use Multi* geometries for multiple clipping onm the same dataset.
            `None` to select the full spatial extent of the inputs or to use
            other spatial filter options like `bbox` or `wgs84_bbox`.

        xyclip_id : str
            The optional name of the field in the xyclip file to be used
            as ID for indexing the geometries in the output datasets.

        xyclip_limit : int
            The (optional) maximum number of geometries to get from xyclip.

        xyclip_split : bool
            Whether to store the output of the N analyses associated to the N
            geometries found in the xyclip input to one single file, or N different files.

        hfilter : array_like (optional)
            [minh,maxh] altitude constraints (referred to the `dem` argument);
            set one of the values to `None` to remove the correspondent constraint,
            or set the whole argument to `None` to remove any altitude filtering.

        dem : str or Path (optional)
            Path to the Digital Elevation Model (DEM) file the `hfilter` argument refers to.

        taggr : str or list
            Type of aggregation to be applied along the time axis of the input
            (and optionally `baseline`) data.
            With time trends analyis, the aggregation is applied when multiple
            (at least 2) different `tint` filters are provided, and always applied to
            an optionally given baseline.

        eaggr : str or list
            Type of aggregation to be applied to the ensemble the input
            (and optionally `baseline`) data.

        xyaggr : str
            Type of aggregation to be applied along the planar spatial axis of the input
            (and optionally `baseline`) data.

        sign_test : str or sequence of str (or None)
            When not None, the (sequence of) dimension(s) along which to group the
            data values for a statistical significant testing with respect
            to the baseline reference.

        sign_conf : numeric (or None)
            The confidence level [%] to be used as threshold for filtering statistically significant
            values along the provided 'sign_test' dimensions.

        perc_pos : numeric (or None)
            If not None, keep only those sections where at least perc_pos of the values
            are positive (>0).

        perc_neg : numeric (or None)
            If not None, keep only those sections where at least perc_pos of the values
            are negative (<0).

        decimals : int >= 0
            The number of decimal places to round the dataset values to.
            No rounding applied if None.

        dt_coords_unit : str (choices: seenumpy::datetime_as_strings() for allowed values)
            The maximum resolution of the formatted datetime coordinates t

        keep_attrs : bool (default True)
            True to keep attributes of input dataset in the output file.

        keep_xyclip_attrs : bool (default True)
            True to keep attributes of input clipping file in the output.

        json_indent : int >=0 (default None)
            Newline indentation for (geo)json output files.
            Leave to None for compact one-line serializations.

        dry_run : bool (default False)
            Dry run option: if `True` no action is actually executed, only logged.

        lenient : bool (default False)
            If `True` no exception is raised on degenerate cases when empty maps
            are the result of the filtering; otherwise the function will silently
            (logs aside) return `None`

        force : bool (default `False`)
            Option to force overwriting of existing output files
            (otherwise the data will not be extraced).

        Returns
        -------
        If output directory (and oforamt is not stdout) is provded, then the function
        returns the path to the file where the analysis file is stored (`True` if stdout was chosen);
        otherwise the bag of output xarray Datasets is returned.
        In both cases the function returns `None` if the analysis could not be extracted (e.g. no input files found).
        """
        # - - - - - - - - - -
        if index is None:
            if lenient:
                return None
            else:
                raise ValueError("Please provide a climate index to analyse.")

        an_module = ANALYSIS_MODULES[an_type]
        if an_module is None:
            raise NotImplementedError("'{}' analysis type module not implemented yet.".format(an_type.value))

        if scenario is None:
            raise ValueError("Please provide a climate scenario.")

        if type(src_type) == str:
            src_type = SrcType[src_type]

        if src is None:
            raise ValueError("Please provide a location for the source data (`src`).")

        if scenario is None:
            raise ValueError("Please provide a climate scenario for the input datasets.")

        if odir is not None:
            if oformat is None:
                oformat = an_module.get_default_format()
            else:
                oformat = FmtType( oformat )
            odir = Path(odir)

        if bool(hfilter) and not bool(dem):
            raise ValueError("Please provide a DEM file for the altitude filter {}".format(hfilter))

        if bool(dem) and not bool(hfilter):
            self.LOGGER.warning("Ignoring DEM file as no h-filter was provided: {}".format(dem))
        
        taggr  = taggr  if taggr  is None or isinstance(taggr,list)  else [taggr]
        eaggr  = eaggr  if eaggr  is None or isinstance(eaggr,list)  else [eaggr]
        xyaggr = xyaggr if xyaggr is None or isinstance(xyaggr,list) else [xyaggr]

        for aggr_opt in [ taggr, eaggr, xyaggr ]:
            if aggr_opt is not None:
                for aggr_el in aggr_opt:
                    self.LOGGER.debug("Checking aggregator: '%s'...", aggr_el)
                    if not check_aggr_type(aggr_el):
                        raise ValueError("Invalid aggregation type: {}".format(aggr_el))

        # either 1 timestep or must have aggregation instructions
        # TODO check is better done once the data is collected to check actual time-steps
        if tint is not None and len(tint) != 0:
            if not any(isinstance(x, list) for x in tint):
                tint = [tint]
            for i,t in enumerate(tint):
                if len(t) == 1:
                    tint[i].append(t[0])
                if len(t) > 2:
                    raise ValueError("Invalid time interval definition: {}".format(t))

        # either 1 model or must have aggregation instructions
        if isinstance(models, str):
            models = [models]
        if (models is None or len(models) > 1) and eaggr is None:
            # TODO here if there is no ensemble but just a single file: use --lenient?
            raise ValueError("Please provide an ensemble aggregation option, or a single model.")

        if models is not None and len(models) == 0:
            raise ValueError("Please provide at least one model, or set to None to select the whole ensemble.")

        if hfilter is not None:
            hfilter = to_number(hfilter)
            if dem is None:
                raise ValueError("Please provide DEM if you need to filter by altitude.")

        if baseline_op is not None:
            if baseline_op not in OpType:
                raise ValueError("Invalid '{}' baseline comparison operator. Allowed: {}".format(baseline_op, OpType.values()))
            baseline_op = OpType(baseline_op)

        if (baseline is not None) and (baseline_op is None):
            raise ValueError("Please provide a baseline comparison operator.")

        if (sign_test is not None) and (len(sign_test) > 0) and (baseline is None):
            raise ValueError("Please provide a baseline for statistical significance filtering.")

        # - - - - - - - - - -
        # manage spatial filtering options to a single e.g. georeferenced object (Shapely? Region?)
        if xyclip is not None:
            if (bbox is not None) or (wgs84_bbox is not None):
                raise ValueError("Please provide either an 'xyclip' or a 'bbox'/'wgs84_bbox'.")
            xyclip_is_file = isinstance(xyclip, Path) or os.path.exists(xyclip)
            if xyclip_is_file:
                xyclip_file = Path(xyclip)
                if xyclip_file.exists():
                    xyclip = gpd.read_file(xyclip_file) # GeoDataFrame now
                    # re-index as per user request
                    if xyclip_id is None:
                        self.LOGGER.debug("No xyclip_id provided: using default data index to identify geoms in the new geometry dimension.")
                    elif xyclip_id not in xyclip:
                        raise ValueError("'{}' column not found in input clipping data. Available: {}".format(xyclip_id, xyclip.columns))
                    else:
                        xyclip_ids = list(xyclip[ xyclip_id ])
                        if len(xyclip_ids) != len(set(xyclip_ids)):
                            raise ValueError("'{}' column in input clipping data has redundant values and cannot be a FID.")
                        else:
                            xyclip.set_index( xyclip_id, inplace=True )
                else:
                    raise ValueError(f"Clipping file not found: {xyclip}")
            else:
                NotImplementedError("'xyclip' as a WKT string input not implemented yet.")

        if (bbox is not None) and (wgs84_bbox is not None):
            raise ValueError("Please provide only 1 among `bbox` and `wgs84_bbox` arguments.")

        if bbox is not None:
            if not isinstance(bbox, list) or len(bbox) != 4:
                raise ValueError("Invalid bbox provided: {}".format(bbox))
            poly   = box( *bbox )
            xyclip = gpd.GeoSeries(poly)

        if wgs84_bbox is not None:
            if not isinstance(wgs84_bbox, list) or len(wgs84_bbox) != 4:
                raise ValueError("Invalid WGS84 bbox provided: {}".format(wgs84_bbox))
            wgs84_poly = box( *wgs84_bbox )
            xyclip     = gpd.GeoSeries(wgs84_poly, crs="EPSG:4326")

        if xyclip is not None:
            geom_str = xyclip if isinstance(xyclip, str) else xyclip.geometry.to_wkt().to_string()
            xyclip_str = trunc(geom_str, 60).replace('\n','')
        # - - - - - - - - - -

        with __lock__:
            if (dry_run):
                self.LOGGER.info("~ ~ ~ ~ ~ ~ ~ ~ ((   DRY RUN  )) ~ ~ ~ ~ ~ ~ ~ ~")

            self.LOGGER.info("|------------------- [%s] -------------------|", index)
            self.LOGGER.info("|--+ analysis : %s", an_type.value)
            self.LOGGER.info("|--+ scenario : %s", scenario)
            self.LOGGER.info("|--+ src-type : %s", src_type.name)
            self.LOGGER.info("|--+ src      : %s", src)
            self.LOGGER.info("|--+ odir     : %s", odir)
            self.LOGGER.info("|--+ oformat  : %s", oformat)
            self.LOGGER.info("|--+ xy-clip  : %s (aggr:%s)", xyclip_str if xyclip is not None else None, xyaggr)
            self.LOGGER.info("|--+ models   : %s (aggr:%s)", str(models or 'all'), eaggr)
            self.LOGGER.info("|--+ timesteps: %s (aggr:%s)", str(tint   or 'all'), taggr)
            self.LOGGER.info("|--+ baseline : %s (op:%s)", baseline, baseline_op.value if baseline else None)
            self.LOGGER.info("|--+ h-filter : %s (dem:%s)", hfilter, dem)
            self.LOGGER.info("|--+ stat.conf: %s", f"{sign_conf}% (along:{sign_test})" if sign_test is not None else None)
            self.LOGGER.info("|--+ perc.pos : %s", f"{perc_pos}%" if perc_pos is not None else None)
            self.LOGGER.info("|--+ perc.neg : %s", f"{perc_neg}%" if perc_neg is not None else None)
            self.LOGGER.info("|-------------------")

        #
        # implementation demultiplexer given analysys and input data types:
        #

        fcall = an_module.get_worker_function(src_type)
        if fcall is None:
            raise NotImplementedError("'{}' source type for {} not implemented yet."
                    .format(src_type.value, an_type.value))

        # module-specific input args validation
        an_module.validate_args(taggr=taggr, eaggr=eaggr, xyaggr=xyaggr, baseline=baseline, models=models, tint=tint)
        self.LOGGER.debug("Arguments are valid.")

        # init
        out_path = None
        out_ds   = None

        if dry_run:
            out_dss = '<dry-run placeholder>'
        else:
            try:
                out_dss = fcall(
                    index, src, scenario,
                    models=models,    baseline=baseline,  baseline_op=baseline_op,
                    tint=tint,        xyclip=xyclip,      xyclip_limit=xyclip_limit,
                    hfilter=hfilter,  dem=dem,
                    taggr=taggr,      eaggr=eaggr, xyaggr=xyaggr,
                    sign_test=sign_test,
                    sign_conf=sign_conf,
                    perc_pos=perc_pos,
                    perc_neg=perc_neg,
                    lenient=lenient)

                n_dss = len(out_dss) if out_dss is not None else 0
                self.LOGGER.debug("Returned datasets count: %s", n_dss)

            except Exception as ex:
                self.LOGGER.error("ERROR: %s", ex)
                raise ex

        if out_dss is None:
            self.LOGGER.error("Information failed to be extracted.")
        else:
            self.LOGGER.debug("Setting metadata attributes on the returned dataset...")
            if not isinstance(out_dss,list):
                out_dss = [out_dss,]
            if not dry_run:
                for ds in out_dss:
                    # set metadata (attributes)
                    ds.attrs[CREATED_ATTR] = format_datetime()
                    #
                    if baseline is not None:
                        xarrays.add_baseline_attr(ds, baseline, baseline_op, taggr)
                    #
                    if hfilter is not None:
                        xarrays.add_hfilter_attr(ds, hfilter)
                    #
                    if eaggr is not None:
                        xarrays.add_aggregation_attr(ds, index, MODELS_DIM, eaggr)
                    #
                    if taggr is not None:
                        xarrays.add_aggregation_attr(ds, index, TIME_DIM, eaggr)
                    #
                    if xyaggr is not None:
                        xarrays.add_aggregation_attr(ds, index, XY_DIMS, xyaggr)

                    # FIXME: time is always mean.. what is that?
                    # for History: variable@cell_methods should describe the aggregations on time/model

        debug = utils.debug_level() > DebugLevels.NO_DEBUG

        with __lock__:
            if oformat is FmtType.stdout:
                self.LOGGER.info(">>> BEGIN OUTPUT >>>>>>>>>>>>>>>>>")
                self.LOGGER.info("---- summary ---------------------")
                self.LOGGER.info(f"{out_dss}")
                self.LOGGER.info("---- data ------------------------")
                self.LOGGER.info(out_dss[0][index].values if not dry_run else '...')
                self.LOGGER.info("<<< END OUTPUT <<<<<<<<<<<<<<<<<<<")
            elif debug:
                self.LOGGER.debug(">>> BEGIN OUTPUT >>>>>>>>>>>>>>>>>")
                self.LOGGER.debug("---- summary ---------------------")
                self.LOGGER.debug(f"{out_dss}")
                self.LOGGER.debug("<<< END OUTPUT <<<<<<<<<<<<<<<<<<<")

        # output datetime coords format
        if not dry_run and dt_coords_unit is not None:
            for i,ds in enumerate(out_dss):
                if TIME_DIM in ds.coords:
                    out_dss[i] = ds.assign_coords({TIME_DIM : np.datetime_as_string(ds.coords[TIME_DIM], dt_coords_unit)})
                    self.LOGGER.info("Converted time coordinates of %d-th dataset to '%s' resolution.", i, dt_coords_unit)

        # output values rounding
        if not dry_run and decimals is not None:
            for i,ds in enumerate(out_dss):
                out_dss[i] = ds.map(lambda a: np.round(a, decimals=decimals), keep_attrs=True)
                self.LOGGER.info("Rounded %d-th dataset values '%s' decimal places.", i, decimals)

        # FIXME: should the function return the datasets? We lose the opath information
        #        but otherwise the xarray datasets are lost: less practical for devs.
        if oformat is FmtType.stdout:
            out = True
        elif odir is None:
            self.LOGGER.info("No output directory provided: NOP.")
            out = out_dss
        else:
            if ofs_routing:
                odir = odir / index / scenario
                self.LOGGER.info("File-system routing applied. Actual output folder: '%s'", odir)

            ofname = craft_file_name(an_type, index, scenario,
                       tint=tint, baseline=baseline, baseline_op=baseline_op,
                       hfilter=hfilter, taggr=taggr, eaggr=eaggr, xyaggr=xyaggr,
                       ofmt=oformat)
            out_path  = odir / ofname

            # return opath(s) to the client in this case, not the data:
            out_paths = [ out_path.with_stem(f'{out_path.stem}_{xyclip.index.values[i]}') for i in range(len(out_dss)) ] if xyclip_split else None
            out = out_paths if xyclip_split else out_path

            # 2 options: all in 1 big file, or N separate files for each clipping geometry:
            nout_files = len(out_paths) if xyclip_split else 1
            self.LOGGER.debug("Storing data to: %d files.", nout_files)

            for i in range(nout_files):
                xyclip_i   = xyclip.iloc[i:i+1] if xyclip_split else xyclip  # [!] trim [a:b] and not slice [a], otherwise index info is lost
                out_path_i = out_paths[i]       if xyclip_split else out_path
                out_dss_i  = out_dss[i]         if xyclip_split else out_dss

                # check if exists AND not force THEN (log.warn && skip)
                with __lock__:
                    if out_path_i.exists():
                        if force:
                            self.LOGGER.warning("Deleting existing namesake file: %s", out_path_i)
                            if not dry_run:
                                out_path_i.unlink()
                        else:
                            out_path_i = out_path_i.with_stem('{}_{}'.format(out_path.stem, datetime.now().strftime(COMPACT_TIME_FMT)))
                            self.LOGGER.warning("Output file already exists. Storing to: %s", out_path_i)

                self.LOGGER.info("Storing data to: '%s'", out_path_i)
                if not dry_run:
                    ok = self._store_ds_to_file(out_dss_i, out_path_i, oformat, an_type, xyclip_i,
                        keep_ds_attrs=keep_attrs,
                        keep_xyclip_attrs=keep_xyclip_attrs,
                        json_indent=json_indent)
                    self.LOGGER.info("Done (success = %s)", ok)

        self.LOGGER.debug("[%s:%s/%s] task done.", an_type.value.upper(), index, scenario)

        return out


    # ------------------------------------------------------------------------------

    def _store_ds_to_file(self, ds:xr.Dataset, opath, fmt:FmtType, an_type:AnalysisType, xyclip=None,
            keep_ds_attrs=True, keep_xyclip_attrs=True, json_indent=None) -> bool:
        """
        Stores the input dataset to the given path.

        Parameters
        ----------
        ds : xr.Dataset
            The Xarray dataset to be serialized.

        opath : Path or str
            The path to the file; if the path does not exists
            an attempt to be created will be done.

        fmt : FmtType
            The format of the output file.

        an_type : AnalysisType
            The type of analysis which was used to craft the dataset.

        xyclip : GeoDataFrame or GeoSeries
            The clipping geometry/geometries.

        keep_ds_attrs : bool (default True)
            True to keep attributes of input dataset in the output file.

        keep_xyclip_attrs : bool (default True)
            True to keep attributes of input clipping file in the output.

        json_indent : int >=0 (default None)
            Newline indentation for (geo)json output files.
            Leave to None for compact one-line serializations.

        Returns
        -------
        True if the dataset was successfully saved to the given path;
        False otherwise.
        """
        # - - - - - - - - - -
        self.LOGGER = utils.get_logger(__name__)

        if ds is None:
            return False

        dss = list()
        if isinstance(ds,list): # or tuple?
            dss = ds
            if fmt is not FmtType.geojson:
                if len(ds) > 1:
                    raise ValueError("Multiple datasets serialization only valid for GeoJSON format.")
                else:
                    ds = ds[0]
        else:
            dss = [ds,]

        if fmt is FmtType.geojson and xyclip is None:
            raise ValueError("Please provide input clipping in order to serialize dataset to GeoJson.")

        if opath is None:
            return ValueError("Please provide a path.")

        if fmt is None:
            return ValueError("Please provide an output format.")

        if fmt is FmtType.stdout:
            return ValueError("stdout is not a valid format for serialization to file.")

        opath = Path(opath)

        # - - - - - - - - - -
        odir = opath.parent
        with __lock__:
            if not odir.exists():
                try:
                    odir.mkdir(parents=True, exist_ok=False)
                except:
                    raise ValueError("Cannot create output folder '{}'. Check your permissions on the file system and retry.".format(odir))

        an_module = ANALYSIS_MODULES[an_type]
        allowed_formats = an_module.get_allowed_out_formats()
        if fmt not in allowed_formats:
            raise NotImplementedError("'{}' output format for {} is not implemented.".format(fmt.value, an_type.value))

        if not keep_ds_attrs:
            for ds in dss:
                idx_name  = xyclip.index.name
                idx_value = ds.attrs[idx_name]
                ds.attrs  = { idx_name : idx_value } # keep all but this one to ensure join

        # try: TODO try/except
        if fmt is FmtType.nc:
            try:
                ds.to_netcdf( path=opath )
            except ValueError:
                # 'grid_mapping' is not accepted for serialization: https://stackoverflow.com/q/69676744/1329340
                # as it CAN BE added automatically by the to_netcdf() function: it depends on the structure/ordering of var/dims.
                # QGIS detects the CRS this way: with grid_mapping as by CF convention.
                # NOTE: sometimes to_netcdf adds 'coordinates' rather than 'grid_mapping': why?
                gmap = utils.drop_attr(ds, attr='grid_mapping', var='all')
                self.LOGGER.debug("'grid_mapping' attribute found: '%s'", gmap)
                ds.to_netcdf( path=opath )

        elif fmt is FmtType.png:
            from PIL import Image
            im = Image.fromarray(ds.to_array()[0].to_numpy())
            #im.astype(np.uint8) ?
            im = im.convert("L") # ?
            im.save( opath )

        elif fmt is FmtType.json:
            if TIME_DIM in ds.coords and type(ds.coords[TIME_DIM].values[0]) == np.datetime64:
                # overcome "Object of type datetime is not JSON serializable" error
                ds.coords[TIME_DIM] = ds.coords[TIME_DIM].dt.strftime("%Y-%m-%d")
                #ds = ds.assign(time = lambda x: x.time.astype(str))

            with open(opath, 'w') as json_file:
                json.dump( ds.to_dict(), json_file, cls=NpJSONEncoder, indent=json_indent )

        elif fmt is FmtType.geojson:
            multiple_geometries = True # TODO (xyclip is not None) and (len(xyclip) > 1)
            is_json_trend = an_type is AnalysisType.trend
            if multiple_geometries and is_json_trend:
                self.LOGGER.debug("Multiple clipping provided + JSON: building a geojson features collection.")
                time_dim = TIME_DIM if TIME_DIM in ds else TIME_RANGE_DIM
                fcoll = self._build_geojson(dss, xyclip, core_dim=time_dim,
                        keep_ds_attrs=keep_ds_attrs,
                        keep_clip_attrs=keep_xyclip_attrs)
                #self.LOGGER.debug("GeoJSON: %s", fcoll)
                with open(opath, 'w') as json_file:
                    json.dump( fcoll, json_file, cls=NpJSONEncoder, indent=json_indent )
            else:
                raise NotImplementedError("Only time trends to geojson are implemented for multi-geometry clipping.")
        else:
            raise RuntimeError("'{}' output format not managed.".format(fmt))

        self.LOGGER.info("Successfully saved analysis as '%s' to: '%s'", fmt.value, opath)

        return True


    # ------------------------------------------------------------------------------
    #
    def _build_geojson(self, dss, xyclip, core_dim=None, keep_ds_attrs=True, keep_clip_attrs=True, discard_cols=None) -> dict:
        """
        Stores the input dataset to the given path.
        The index of the xyclip data is expected to be referenced in each of the
        input datasets in order to be able to join unambiguously.

        Parameters
        ----------
        dss : list of xr.Dataset
            The xarray dataset(s) to be converted to geojson features.

        xyclip : GeoDataFrame or GeoSeries
            The geometries used to clip the datasets.
            The number of geometries shall coincide with the number of datasets.

        core_dim : str
            The core dimension used to group data for each feature in the collection
            (e.g. if model and time dimensions are there, and time is specified as the core
            dimension, then each model value will be a separate property, whose value
            are listed for each timestamp)

        keep_ds_attrs : bool (default True)
            True to keep attributes of input dataset in the output file.

        keep_xyclip_attrs : bool (default True)
            True to keep attributes of input clipping file in the output.

        discard_cols : str or list
            Columns of xyclip data frame to be excluded from the output.

        Returns
        -------
        A geojson-compliant dictionary of one FeatureCollection with as many features
        as the number of input datasets.

        Example
        =======
        >>> _build_geojson(dss, xyclip, core_dim=TIME_DIM)
        {
           "type": "FeatureCollection",
           "metadata": {
               { ... dataset global attrs ... }
           }
           "features": [
               {
                   "type": "Feature",
                   "geometry": {
                       "type": "Point",
                       "coordinates": [-105.01621, 39.57422]
                   },
                   "properties" : {
                       $INDEX_NAME : 'AT456',
                       'amt' : {
                         "min" : {"2020-07-03": 5, "2020-07-04": 6, ...},
                         "q1"  : {"2020-07-03": 11, "2020-07-04": 12, ...},
                         "med" : {"2020-07-03": 33, "2020-07-04": 34, ...},
                         "q3"  : {"2020-07-03": 44, "2020-07-04": 45, ...},
                         "max" : {"2020-07-03": 67, "2020-07-04": 69, ...}
                       },
                       { ... xyclip columns/value pairs ... }
                   }
               }
           ]
        }
        """
        # - - - - - - - - - -
        self.LOGGER = utils.get_logger(__name__)

        if dss is None:
            return False

        if xyclip is None:
            raise ValueError("xyclip geometry required for GeoJSON output.")

        if not isinstance(dss, list): # or tuple?
            dss = [dss,]

        n_dss = len(dss)
        n_xyg = len(xyclip)
        if n_dss != n_xyg:
            self.LOGGER.warn("Number of input datasets and clipping geometries do not match: %d / %d", n_dss, n_xyg)

        if not isinstance(discard_cols, list):
            discard_cols = [discard_cols,]
        # geometry is already described in the features' geometry (not to be repeated in the 'properties')
        discard_cols.append('geometry')
        if None in discard_cols:
            discard_cols.remove(None)
        for col in discard_cols:
            if col not in xyclip:
                raise ValueError("{} field not found in clipping dataframe. Available: {}".format(col, list(xyclip.columns)))

        # - - - - - - - - - -
        import ast
        fcoll_json = dict(type='FeatureCollection')
        features = list()
        idx_name = xyclip.index.name
        #
        # build each feature
        #
        for i,ds in enumerate(dss):
            # checks
            if idx_name not in ds.attrs:
                raise ValueError("{} not found in the {}-th dataset's attributes: cannot join with clipping geometries.".format(idx_name, i))
            if core_dim not in ds:
                raise ValueError("{} dimension not found in dataset. Available: {}".format(core_dim, list(ds.dims)))
            if len(ds) > 1:
                raise NotImplementedError("Maximum single-variable dataset are supported for geojson. Found: {}".format(len(ds)))

            # fetch geometry that clipped this dataset:
            idx_value = ast.literal_eval( ds.attrs[idx_name] ) # (from string representation of array, to array)
            clip_i = xyclip.loc[idx_value]
            if len(clip_i) != 1:
                raise ValueError("{} geometries found with index {}:{}.", len(clip_i), idx_name, idx_value)

            # GeoDataFrame to series  ([idx_value] indexing returns: depends on gpd version!)
            if isinstance(clip_i, gpd.GeoDataFrame):
                clip_i = pd.Series(data=clip_i.iloc[0])

            #self.LOGGER.debug("clip element: %s", type(clip_i))
            #self.LOGGER.debug("clip values : %s", clip_i.values)
            #self.LOGGER.debug("clip keys   : %s", clip_i.index.values)
            self.LOGGER.debug("Feature #%d - %s:%s...", i, idx_name, idx_value)
            f_json = dict()

            # build the json:
            # geom
            geom_json = dict()
            geom_ring = clip_i.geometry
            geom_type = clip_i.geometry.geom_type
            self.LOGGER.debug("Original geometry type: %s", geom_type)
            # TODO we discard coords here for MultiPolygons and Polygons with holes
            if geom_type.startswith('Multi'):
                geom_ring = geom_ring.geoms[0] # first of multi: how to serialize the whole geoms?
                geom_type = geom_ring.geom_type
            if geom_type == 'Polygon':
                geom_ring = geom_ring.exterior
            geom_coords = [[ [c[0],c[1]] for c in reversed(geom_ring.coords) ]]
            # NOTE geojson standards imposes counter-clockwise coordinates for exterior rings
            # TODO add interior rings to (which should be clockwise instead)
            geom_json.update(dict(type=geom_type, coordinates=geom_coords))

            # geom index
            f_properties = { idx_name:idx_value }

            # var data
            vars_dict = dict()
            other_dims = list(ds.dims)
            other_dims.remove(core_dim)
            if other_dims is None:
                other_dims = list()
            if len(other_dims) > 1:
                raise NotImplementedError("Maximum 1 no-core dimensions handled for geojson outputs.")
            outer_dim = other_dims[0] if len(other_dims) == 1 else None
            for var in ds:
                f_data = dict()
                outer_values = ds[var][outer_dim].values if outer_dim is not None else [None,]
                for outer_el in outer_values:
                    #self.LOGGER.debug("ELEMENT: %s", outer_el)
                    slicing = {outer_dim:outer_el} if outer_el is not None else dict()
                    #self.LOGGER.debug("SLICING: %s", slicing)
                    # FIXME how to control output value of numpy array (also decimal precision?)
                    #self.LOGGER.debug("VALUES: %s", ds[var][core_dim].values)
                    # FIXME this can become very slow even for few elements:
                    inner_values = ds[var].loc[{**slicing}].to_numpy()  # <- [!] this is the slow part for long arrays
                    inner_coords = ds[var].loc[{**slicing}][core_dim].values
                    f_innerdata  = dict(zip(inner_coords.astype(str), inner_values))
                    # this is very slow:
                    #f_innerdata = { str(inner_el):float(ds[var].loc[{**slicing, core_dim:inner_el}].values) for inner_el in ds[var][core_dim].values }
                    #self.LOGGER.debug("UPDATING...")
                    if outer_dim is not None:
                        assert(outer_el is not None)
                        f_data.update({outer_el:f_innerdata})
                    else:
                        assert(len(outer_values)==1)
                        f_data.update(f_innerdata)
                    self.LOGGER.debug("DONE: %s", outer_el)
                # all inside the same variable's dictionary
                f_properties.update({var:f_data})
                # NOTE: with multiple variables, all attributes would get mixed together, not scoped

            # attrs
            if keep_clip_attrs:
                # Attributes of the clipping geometry:
                clip_attrs = dict()
                #for col in clip_i.drop(columns=discard_cols):
                for col in clip_i.drop(labels=discard_cols).index.values:
                    #self.LOGGER.debug("Adding '%s' attribute", col)
                    #self.LOGGER.debug("Adding '%s' --> '%s' attribute", col, clip_i[col])
                    clip_attrs.update({col:clip_i[col]})
                f_properties.update(**clip_attrs)

            if keep_ds_attrs:
                # Input ensemble metadata:
                # fcoll cannot have properties but might allow other fields: https://gis.stackexchange.com/a/209263/6998
                fcoll_metadata = {}
                ds.attrs.pop(idx_name, None) # TODO other geometry or model specific attrs shall be removed
                fcoll_metadata.update(**ds.attrs)
                fcoll_json.update(dict(metadata=fcoll_metadata))

            # build the whole feature
            f_json.update(dict(type='Feature', geometry=geom_json, properties=f_properties))
            features.append(f_json)

        # add feature to collection
        fcoll_json.update(dict(features=features))

        return fcoll_json

# ------------------------------------------------------------------------------
#
class NpJSONEncoder(json.JSONEncoder):
    """NumPy-compatible JSON encoder (avoid 'Object of type TYPE is not JSON serializable' errors on serialization)"""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpJSONEncoder, self).default(obj)

# ------------------------------------------------------------------------------
#
def log_header():
    LOGGER = utils.get_logger(__name__)

    LOGGER.info("                           ")
    LOGGER.info("/// climdex-kit / analyse :")
    LOGGER.info("                           ")


def log_report(analysis_type, n_ok, n_error, is_dry_run):
    LOGGER = utils.get_logger(__name__)
    dry_run_str = "" if not is_dry_run else "  (dry-run)"
    LOGGER.info("|")
    LOGGER.info("| Total %s extracted : %d %s", analysis_type.upper(), n_ok, dry_run_str)
    LOGGER.info("| Total %s aborted   : %d %s", analysis_type.upper(), n_error, dry_run_str)
    LOGGER.info("|__")

# ------------------------------------------------------------------------------

