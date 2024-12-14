"""
Actual implementaions of TRENDS analysis type for
local file-based climate indices.

Input files are assumed to be NetCDFs.
"""
from pathlib import Path

import itertools
import pandas as pd
import numpy as np
import xarray as xr # + import netCDF4
import rioxarray as rxr
from shapely.geometry.base import BaseGeometry
from pyproj import CRS
import geopandas as gpd

from climdex import cmodels
from climdex.nc import *
from climdex.utils import *
from climdex.constants import *
from climdex.analyse import xarrays
from climdex.analyse.utils import *
from climdex.analyse.filesystem import *
from climdex.analyse.enums import OpType

# TEST REPL ###################################################
# import importlib_resources
# import pandas as pd
# utils.setup_logging( level=logging.DEBUG, path=None, env_key=None )
#
# __package__ = 'climdex'
# idir = importlib_resources.files(__package__) / '..' / '..' / 'tests' / 'testdata' / 'INDICES'
# dem  = idir / '..' / 'DEM_1km_LAEA.nc'
#
# #idir = Path('/mnt/CEPH_PROJECTS/FACT_CLIMAX/CORDEX-Adjust/INDICES/')
# #dem  = idir / 'DEM_1km_LAEA.nc'
#
# tnst = Path('/home/pcampalani@eurac.edu/data/TrentinoAltoAdige.json')
# xyclip_id = 'com_catasto_code'
# xyclip = gpd.read_file(tnst)
# xyclip.set_index( xyclip_id, inplace=True)
# xyclip.set_crs('epsg:4326', inplace=True)
#
# eaggr = ['med'] # None # ['q1', 'q2', 'q3']
#
# index = 'amt'
# rcp = 'rcp85'
# xyaggr = 'avg'
# tint  = [['2071', '2076'], ['2081', '2086']]
# tint  = [['2071', '2076']]
# models = None
# hfilter = None #[None,1000]
# baseline = None #['1981', '1986']
# baseline_op = None #OpType('diff')
# taggr = 'med'
# lenient = False
#
# # LONG TIME SERIES:
# #tint  = [['2041', '2070'], ['2071', '2100']]
# #baseline = ['1981', '2010']
#
# sign_test = None #[ TIME_DIM, MODELS_DIM ]
# sign_conf = None #68
#
# # TEST CLIPPING
# from climdex.analyse import trends_nc
# out_dss = trends_nc._extract_trend(index, idir=idir, scenario=rcp, tint=tint, xyaggr='min', eaggr='avg', xyclip=xyclip[:2])
# out_dss = trends_nc._extract_trend(index, idir=idir, scenario=rcp, tint=tint, xyaggr='min', eaggr=['min','max'], xyclip=xyclip[:2])
# ## then:
# from climdex.actions import analyse
# fcoll = analyse._build_geojson(out_dss, xyclip[:2], core_dim=TIME_DIM, keep_attrs=True)
# fcoll = analyse._build_geojson(out_dss, xyclip[:2], core_dim=TIME_DIM, keep_attrs=True, discard_cols='id')
#
# # UP TO SERIALIZATION:
# tr = AnalysisType.trend
# analyse.do_extract_information(tr, index, src=idir, src_type='local', scenario=rcp, tint=tint, xyaggr='min', eaggr='avg', xyclip=xyclip[:2], xyclip_id=xyclip_id)
# analyse.do_extract_information(tr, index, src=idir, src_type='local', scenario=rcp, tint=tint, xyaggr='min', eaggr=['min','max'], xyclip=xyclip[:2], xyclip_id=xyclip_id)
#
# index_dir = idir / index
# scenario_dir = index_dir / rcp
# models_rgx = NETCDF_RGX
# ensemble_files = fetch_index_files( scenario_dir, rgx=models_rgx)
# target_ds = xarrays.data_preparation_procedure(
#    ensemble_files,  index=index,
#    models=models,   baseline=baseline,  baseline_op=baseline_op,
#    tint=tint,       xyclip=None,
#    hfilter=hfilter, dem=dem,
#    sign_test=sign_test, sign_conf=sign_conf,
#    lenient=lenient)
#
# x_dim = target_ds.rio.x_dim
# y_dim = target_ds.rio.y_dim
# target_ds = apply_aggr( target_ds, xyaggr, [x_dim,y_dim], keep_attrs=True )
#
# baseline_ds = target_ds.sel( time = slice(*baseline) )
# baseline_ds = baseline_ds.rio.write_crs( target_ds.rio.crs )
# target_ds = target_ds.drop_sel( time = baseline_ds[TIME_DIM] )
# target_ds = target_ds.rio.write_crs( baseline_ds.rio.crs )
#
# baseline_ds = apply_aggr( baseline_ds, taggr, TIME_DIM )
# target_ds[index] = target_ds[index].groupby(TIME_DIM).map(\
#         lambda x : apply_op( x, baseline_da=baseline_ds[index], op=baseline_op ))
#
# if tint is not None:
#     subtarget_dss = [None]*len(tint)
#     for i,t in enumerate(tint):
#         print("Applying '{}' time aggregation to '{}' interval...".format(taggr, t))
#         subtarget_dss[i] = apply_aggr( target_ds.loc[{ TIME_DIM:slice(*t) }], taggr, TIME_DIM, keep_attrs=True )
#     target_ds = xr.concat( subtarget_dss, pd.Index([f'{t[0]}-{t[1]}' for t in tint], name=TIME_DIM) )
#
# if eaggr is not None:
#     subtarget_dss = [None]*len(eaggr)
#     for i,aggr in enumerate(eaggr):
#         print("Applying '{}' ensemble aggregation...".format(aggr))
#         subtarget_dss[i] = apply_aggr( target_ds, aggr, MODELS_DIM, keep_attrs=True )
#     target_ds = xr.concat( subtarget_dss, dim=pd.Index([f'ensemble-{e}' for e in eaggr], name=MODELS_DIM ))
#
# target_ds.attrs[CREATED_ATTR] = format_datetime()
# if eaggr is not None:
#     new_cell_method = f"{MODELS_DIM}: {eaggr}"
#     utils.add_or_append_attr(target_ds[index], attr=CMETHODS_ATTR, value=new_cell_method)
#
# baseline_ds.close()
#
# ------------------------------------------------------------------------------

def _extract_trend(index:str, idir:str, scenario:str,
        models=None,    baseline=None,  baseline_op:OpType=None, taggr=None,
        tint=None,      xyclip=None,    xyclip_limit=None,
        hfilter=None,   dem=None,
        xyaggr=None,    eaggr=None,
        sign_test=None, sign_conf=None,
        perc_pos=None,  perc_neg=None,
        lenient=False,  **kwargs) -> xr.Dataset:
    """
    See climdex.analyse.do_extract_information(...).

    'eaggr' can either be None to show trends of the selected models,
    a single agggregator, or a sequence of aggregators to be computed
    in batch in the same analysis task.

    'taggr' in this case is only used to aggregate the possible baseline
    time interval for comparison/normalization of output.

    NOTE: **kwargs used as bin for unused arguments that are
    set by the general analysis operation caller.

    Returns
    -------
    The resulting trend as a (set of) 1D xarray Dataset(s).
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

    if xyclip is not None:
        is_geom = isinstance(xyclip, BaseGeometry)
        is_gpd  = isinstance(xyclip, gpd.base.GeoPandasBase)
        if not is_geom and not is_gpd:
            raise ValueError("Please provide spatial clipping as either a Geometry or a GeoSeries/GeoDataFrame.")
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

    # force list of intervals as input
    do_taggr = False
    if tint is not None:
        if len(tint) == 0:
            tint = None
        if not any(isinstance(x, list) for x in tint):
            tint = [tint]
        for i,t in enumerate(tint):
            #if len(t) == 1:
            #    tint[i].append(t[0])
            if len(t) != 2:
                raise ValueError("Invalid time interval definition: {}".format(t))
        if taggr is not None:
            do_taggr = len(tint) >= 2 
            if len(tint) == 1:
                if baseline is None:
                    do_taggr = True
                    LOGGER.warn("'%s' time aggregation provided on single interval and no baseline: will apply it on target.", taggr)
                else:
                    LOGGER.info("'%s' time aggregation will be applied to baseline only.", taggr)
    
    if eaggr is not None and not isinstance(eaggr, list):
        eaggr = [eaggr]

    if xyaggr is None:
        raise ValueError("Please provide a spatial aggregator.")

    for aggr in [taggr]:
        if isinstance(aggr, list) and len(aggr) > 1:
            raise NotImplementedError("Only single aggregator per analysis currently supported: '{}'".format(aggr))

    taggr  = taggr[0]  if isinstance(taggr,  list) else taggr  # validate_args ensures at most 1 taggr
    xyaggr = xyaggr    if isinstance(xyaggr, list) else [xyaggr,]

    if eaggr is None and ((perc_pos is not None) or (perc_neg is not None)):
         raise ValueError("A percentage pos/neg filter is asked on the ensemble without eaggr option.")

    # - - - - - - - - - -

    LOGGER.debug("File-based [%s] TREND analysis request ... ", index)

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

    # xy-clipping?
    n_out_dss = 1
    if xyclip is not None:
        ngeoms     = len(xyclip.geometry)
        xyclip_gs  = gpd.GeoSeries(xyclip.geometry) # crs and index are inherited
        n_out_dss  = ngeoms
        if (xyclip_limit is not None) and (xyclip_limit < n_out_dss):
            n_out_dss = xyclip_limit
            LOGGER.info("XY clipping geometries limit set to %d", n_out_dss)
    target_dss = [None,] * n_out_dss
    #
    # TODO parallelize computation
    for out_i in range(n_out_dss):
        LOGGER.info("DATA PREPARATION STAGE (#%d)", out_i)

        xyclip_el = xyclip_gs.iloc[out_i:out_i+1] if xyclip is not None else None
        LOGGER.debug("xyclip geom: %s (%s)", xyclip_el, xyclip_el.crs if xyclip_el is not None else '-')

        # trimming (not slicing) to keep GeoSeries type (so crs goes through piggy-backed)
        # TODO use preprocess callable to filter before loading to memory
        target_ds = xarrays.data_preparation_procedure(
                ensemble_files,  index=index,
                models=models,   baseline=baseline,  baseline_op=baseline_op,
                tint=tint,       xyclip=xyclip_el,
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

        LOGGER.info("DATA PROCESSING STAGE (#%d)", out_i)

        # spatial aggregation
        x_dim = target_ds.rio.x_dim
        y_dim = target_ds.rio.y_dim
        if 1 == len(xyaggr):
            LOGGER.debug("Applying '%s' spatial aggregation...", xyaggr[0])
            target_ds = apply_aggr( target_ds, xyaggr[0], [x_dim,y_dim], keep_attrs=True ) # TODO to constants
        else:
            subtarget_dss = [None]*len(xyaggr)
            for i,aggr in enumerate(xyaggr):
                LOGGER.debug("(#%d) Applying '%s' spatial aggregation...", i, aggr)
                subtarget_dss[i] = apply_aggr( target_ds, aggr, [x_dim,y_dim], keep_attrs=True )
            # stack all back together, setting the coords of the new dimension (the time intervals):
            target_ds = xr.concat( subtarget_dss, dim=pd.Index([f'xyaggr-{a}' for a in xyaggr], name=XY_DIMS ), coords='minimal')
            for ds in subtarget_dss:
                ds.close()

        # re-split baseline from target: separate aggregations required from now on
        #
        if baseline is not None:
            LOGGER.debug("Separating baseline from target...")
            # baseline
            baseline_ds = target_ds.sel( time = slice(*baseline) )
            baseline_ds = baseline_ds.rio.write_crs( target_ds.rio.crs )
            # target
            target_ds = target_ds.drop_sel( time = baseline_ds[TIME_DIM] )
            target_ds = target_ds.rio.write_crs( baseline_ds.rio.crs )
            # baseline aggregation
            if taggr is not None:
                LOGGER.debug("Applying '%s' time aggregation to baseline...", taggr)
                baseline_ds = apply_aggr( baseline_ds, taggr, TIME_DIM )
            else:
                LOGGER.warn("No time aggregation set on baseline.") # TODO error? 

        # time filter
        #
        if (tint is not None) and len(tint)==1 and (tint[0][0] == tint[0][1]):
            # if tint is a single time-step, dissolve dimension to return 2D:
            target_ds = target_ds.min( dim=TIME_DIM, keep_attrs=True )

        # relative comparison with baseline
        #
        if baseline is not None:
            LOGGER.debug("Applying '%s' comparison with baseline...", baseline)
            # baseline is time-aggreagated, whereas target dataset is not:
            LOGGER.debug("TARGET: '%s'  / BASELINE: '%s'", target_ds[index], baseline_ds[index])
            target_ds[index] = target_ds[index]   \
                .groupby(TIME_DIM, squeeze=False) \
                .map(lambda tslice:               \
                    apply_op( tslice.squeeze(TIME_DIM), baseline_da=baseline_ds[index], op=baseline_op ))
            # NOTE: need to manually squeeze as it has been deprecated and defaults to False since 2024.01.0
            # @see https://docs.xarray.dev/en/stable/whats-new.html#id114

        # time aggregations (only with N input time-intervals, otherwise time dimension gets lost)
        #
        if do_taggr and (TIME_DIM in target_ds):
            subtarget_dss = [None]*len(tint)
            for i,t in enumerate(tint):
                LOGGER.debug("Applying '%s' time aggregation to '%s' interval...", taggr, t)
                sub_ds = target_ds.loc[{ TIME_DIM:slice(*t) }]
                subtarget_dss[i] = apply_aggr( sub_ds, taggr, TIME_DIM, keep_attrs=True )
            # stack all back together, setting the coords of the new dimension (the time intervals):
            target_ds = xr.concat( subtarget_dss, dim=pd.Index([f'{t[0]}-{t[1]}' for t in tint], name=TIME_RANGE_DIM ), coords='minimal')
            for ds in subtarget_dss:
                ds.close()

        # percentage positive/negative mask
        #
        if (perc_pos is not None) or (perc_neg is not None):
            LOGGER.debug("Computing mask of percentage of data %s0...", ">" if perc_neg is None else "<")
            perc_ds = apply_perc_positive(target_ds, dim=[MODELS_DIM], negative=(perc_neg is not None)) 

        # ensemble aggregation
        #
        if eaggr is not None:
            subtarget_dss = [None]*len(eaggr)
            for i,aggr in enumerate(eaggr):
                LOGGER.debug("(#%d) Applying '%s' ensemble aggregation...", i, aggr)
                subtarget_dss[i] = apply_aggr( target_ds, aggr, MODELS_DIM, keep_attrs=True )
                # concat: quantiles cuts out lambert_azimuthal dimension so concatting breaks (or put "coords='minimal'")
                #LOGGER.debug("DS    COORDS: %s", target_ds.coords)
                #LOGGER.debug("SUBDS COORDS: %s", subtarget_dss[i].coords)
            # stack all back together, setting the coords of the new dimension (the models stats):
            target_ds = xr.concat( subtarget_dss, dim=pd.Index([f'ensemble-{e}' for e in eaggr], name=MODELS_STAT_DIM ), coords='minimal')
            for ds in subtarget_dss:
                ds.close()
            # if just 1 aggr, dissolve the models dimension:
            if len(eaggr) <= 1:
                target_ds = target_ds.min( dim=MODELS_STAT_DIM, keep_attrs=True )
            #
            # percentage positive/negative filter
            #
            if (perc_pos is not None) or (perc_neg is not None):
                LOGGER.debug("Filtering values in the ensemble where %d%%%s0", perc_pos or perc_neg, ">" if perc_neg is None else "<")
                threshold = perc_pos if perc_pos is not None else perc_neg
                target_ds = target_ds.where(perc_ds >= threshold)

        # close dataset?
        #
        if baseline is not None:
            baseline_ds.close()

        # add to list
        target_dss[out_i] = target_ds.copy(deep=(n_out_dss>1))

        # cleanup
        if n_out_dss>1:
            target_ds.close()

    LOGGER.debug("Trend done. Bye..")

    # unbox if single dataset
    return target_ds if len(target_dss) == 1 else target_dss

