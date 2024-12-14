"""
Actual implementaions of MAPS analysis type for
local file-based climate indices.

Input files are assumed to be NetCDFs.
"""
from pathlib import Path

import itertools
import numpy as np
import xarray as xr # + import netCDF4
import rioxarray as rxr
from shapely.geometry.base import BaseGeometry
import geopandas as gpd
#from rasterio.enums import Resampling

from ..nc import *
from ..utils import *
from ..constants import *
from . import xarrays
from .utils import *
from .filesystem import *
from .enums import OpType

# ------------------------------------------------------------------------------

def _extract_map(index:str, idir:str, scenario:str,
        models=None,    baseline=None,  baseline_op:OpType=None,
        tint=None,      xyclip=None,    xyclip_limit=None,
        hfilter=None,   dem=None,
        taggr=None,     eaggr=None,
        sign_test=None, sign_conf=None,
        perc_pos=None,  perc_neg=None,
        lenient=False,  **kwargs) -> xr.Dataset:
    """
    See climdex.analyse.do_extract_information(...).

    NOTE: **kwargs used as bin for unused arguments that are
    set by the general analysis operation caller.

    Returns
    -------
    The resulting map as a 2D xarray Dataset.
    """
    # - - - - - - - - - -
    LOGGER = utils.get_logger(__name__)
    # - - - - - - - - - -
    if index is None:
        return None

    if idir is None:
        raise ValueError("Please provide an input directory.")

    idir = Path(idir)
    if not idir.exists():
        raise ValueError("Input directory does not exists: '{}'".format(idir))

    if scenario is None:
        raise ValueError("Please provide a climate scenario for the input datasets.")

    # force list of intervals as input
    if tint is not None:
        if len(tint) == 0:
            tint = None
        if not any(isinstance(x, list) for x in tint):
            tint = [tint]
        if len(tint) >= 2:
            raise NotImplementedError("Maximum 1 time interval maps currently implemented.")
        for i,t in enumerate(tint):
            #if len(t) == 1:
            #    tint[i].append(t[0])
            if len(t) != 2:
                raise ValueError("Invalid time interval definition: {}".format(t))

    if xyclip is not None:
        is_geom = isinstance(xyclip, BaseGeometry)
        is_gpd  = (type(xyclip) is gpd.GeoSeries)
        is_gpd  = isinstance(xyclip, gpd.base.GeoPandasBase)
        if not is_geom and not is_gpd:
            raise ValueError("Please provide spatial clipping as either a Geometry or a GeoSeries.")
        # CRS assumptions:
        assume_wgs84  = is_geom
        assume_wgs84 |= is_gpd and (xyclip.crs is None)
        if assume_wgs84:
            LOGGER.warning("Assuming WGS84 lat/lon coords for input clipping.")

    if hfilter is not None and dem is None:
        raise ValueError("Please provide DEM if you need to filter by altitude.")

    if (baseline is not None) and (baseline_op is None):
        raise ValueError("Please provide a baseline comparison operator.")

    if (baseline_op is not None) and (baseline_op not in OpType):
        raise ValueError("Invalid '{}' baseline comparison operator. Allowed: {}".format(baseline_op, OpType.values()))

    for aggr in [eaggr, taggr]:
        if isinstance(aggr, list) and len(aggr) > 1:
            raise NotImplementedError("Only single aggregator per analysis currently supported: '{}'".format(aggr))

    eaggr = eaggr[0] if isinstance(eaggr, list) else eaggr
    taggr = taggr[0] if isinstance(taggr, list) else taggr
            
    if eaggr is None and ((perc_pos is not None) or (perc_neg is not None)):
         raise ValueError("A percentage pos/neg filter is asked on the ensemble without eaggr option")

    # - - - - - - - - - -

    LOGGER.debug("File-based [%s] MAP analysis request ... ", index)

    # fetch input folder
    index_dir = idir / index
    if not index_dir.exists():
        raise ValueError("Index input directory not found: '{}'".format(index_dir))

    scenario_dir = index_dir / scenario
    if not scenario_dir.exists():
        raise ValueError("Scenario input directory not found: '{}'".format(scenario_dir))

    # fetch input files (all *.nc if models is None else ... LUT/regex)
    models_rgx = NETCDF_RGX
    ensemble_files = fetch_index_files( scenario_dir, rgx=models_rgx)
    LOGGER.debug("%d input [%s] models time-series found.", len(ensemble_files), index)

    if len(ensemble_files) == 0:
        raise ValueError("No valid input files ('{}') were found in folder: '{}'"
                .format(models_rgx, scenario_dir))

    # models filtering
    #
    if models is not None:
        ensemble_files = fetch_index_files( scenario_dir, rgx=models_rgx, models=models)
        LOGGER.debug("%d filtered input [%s] models found.", len(ensemble_files), index)

    if len(ensemble_files) == 0:
        if lenient:
            LOGGER.warn("No input files found at: '%s/%s' [models ids:%s]", scenario_dir, models_rgx, models)
            return None
        else:
            raise ValueError("No models were found in filter: {}".format(models))

    # load the data and stack them together (4D: model, time, x, y)
    # TODO use preprocess callable to filter before loading to memory
    LOGGER.info("DATA PREPARATION STAGE")
    target_ds = xarrays.data_preparation_procedure(
            ensemble_files,  index=index,
            models=models,   baseline=baseline,  baseline_op=baseline_op,
            tint=tint,       xyclip=xyclip,      xyclip_limit=xyclip_limit,
            hfilter=hfilter, dem=dem, 
            sign_test=sign_test,
            sign_conf=sign_conf,
            lenient=lenient)

    if target_ds is None:
        LOGGER.error("No dataset could be found with the given filters.")
        return None

    # End of DATA PREPARATION
    #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#
    #
    # Begin DATA AGGREGATIONS
    #

    LOGGER.info("DATA PROCESSING STAGE")

    # re-split baseline from target: separate aggregations required from now on
    # NOTE: since aggregators might want to be applied on the already baseline-compared vlaues,
    #       (e.g. perc_pos), we need to sort this before the other aggregators
    if baseline is not None:
        LOGGER.debug("Separating baseline from target...")
        # baseline
        baseline_ds = target_ds.sel( time = slice(*baseline) )
        baseline_ds = baseline_ds.rio.write_crs( target_ds.rio.crs )
        # target
        target_ds = target_ds.drop_sel( time = baseline_ds[TIME_DIM] )
        target_ds = target_ds.rio.write_crs( baseline_ds.rio.crs )

    # time aggregation
    #
    if taggr is not None:
        # TODO apply aggregation for any tint provided (new dimension on target_ds!!)
        LOGGER.debug("Applying '%s' time aggregation...", taggr)
        target_ds = apply_aggr( target_ds, taggr, TIME_DIM, keep_attrs=True )
        if baseline is not None:
            LOGGER.debug("Applying '%s' time aggregation to baseline...", taggr)
            baseline_ds = apply_aggr( baseline_ds, taggr, TIME_DIM, keep_attrs=True )
    else:
        # if time interval is a single time-step, dissolve dimension to return 2D:
        if (tint is not None) and len(tint)==1 and (tint[0][0] == tint[0][1]):
            target_ds = target_ds.min( dim=TIME_DIM, keep_attrs=True )
        # .. same for baseline:
        if (baseline is not None) and len(baseline)==1 and (baseline[0][0] == baseline[0][1]):
            baseline_ds = baseline_ds.min( dim=TIME_DIM, keep_attrs=True )

    if baseline is not None:
        # comparison with baseline:
        LOGGER.debug("Applying '%s' comparison with baseline...", baseline)
        target_ds[index] = apply_op( target_ds[index], baseline_da=baseline_ds[index], op=baseline_op )

    # percentage positive/negative mask
    #
    if (perc_pos is not None) or (perc_neg is not None):
        LOGGER.debug("Computing XY mask of percentage of data %s0...", ">" if perc_neg is None else "<")
        perc_ds = apply_perc_positive(target_ds, dim=[MODELS_DIM] , negative=(perc_neg is not None)) 

    # ensemble aggregation
    #
    # TODO warning on "unusual" ensemble aggregation + min. recommended number of models
    if eaggr is not None:
        LOGGER.debug("Applying '%s' ensemble aggregation...", eaggr)
        target_ds = apply_aggr( target_ds, eaggr, MODELS_DIM, keep_attrs=True )

    # relative comparison with baseline
    #
    # TODO: posticipate b-comparison after T/E aggregations to allow time intervals of difference lenghts!!
    #       (remember to apply aggregations on both Datasets up here)
    #
    #if baseline is not None:
    #    LOGGER.debug("Applying '%s' comparison with baseline...", baseline)
    #    target_ds[index] = apply_op( target_ds[index], baseline_da=baseline_ds[index], op=baseline_op )

    #
    # percentage positive/negative filter
    if (perc_pos is not None) or (perc_neg is not None):
        LOGGER.debug("Filtering values in the ensemble where %d%%%s0", perc_pos or perc_neg, ">" if perc_neg is None else "<")
        threshold = perc_pos if perc_pos is not None else perc_neg
        target_ds = target_ds.where(perc_ds >= threshold, drop=False)
                             #.transpose( *list(target_ds.dims) ) # for NetCDF serialization: do not let where() reshape the structure, it's delicate
        # TODO adjust trends_nc and also all unit tests!

    # close dataset?
    #
    if baseline is not None:
        baseline_ds.close()

    # clean attrs
    if CMETHODS_ATTR in target_ds[index].attrs:
        del target_ds[index].attrs[CMETHODS_ATTR]

    LOGGER.debug("Map done. Bye..")

    return target_ds

