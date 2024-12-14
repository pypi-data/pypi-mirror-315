
"""
Re-usable operations on xarray Datasets for the climdex.analyse module.
"""

import re
import itertools
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry.base import BaseGeometry
import xarray as xr
from pyproj import CRS
from rasterio.enums import Resampling
from scipy import stats

from ..utils import *
from ..constants import *
from .enums import AggrType
from .enums import AnalysisType
from .enums import FmtType
from .enums import OpType
from .utils import *

# >>> help(xr.DataArray.quantile)
# {"linear", "lower", "higher", "midpoint", "nearest"}
DEFAULT_QUANTILE_INTERP = 'midpoint'
DEFAULT_RESAMPLING = Resampling.med

# ------------------------------------------------------------------------------
#
def data_preparation_procedure(ensemble_files, index,
        models=None,    baseline=None,  baseline_op:OpType=None,
        tint=None,      xyclip=None,    xyclip_limit=None,
        hfilter=None,   dem=None,
        sign_test=None, sign_conf=None,
        lenient=False) -> xr.Dataset:
    """
    Data preparation procedure shared by all kinds of analysis, which includes:

      - filtering of "empty" input layers (they can be added to let rasdaman WCS-T based
        ingestion work with a regular "models" dimension)

      - CRS information extraction

      - input time interval subsetting

      - baseline interval subsetting

      - horizontal XY and vertical H (through DEM) spatial filtering

    Parameters
    ----------
    ensemble_files : str, Path or list
       The file(s) that compoundly represent the input datacube.

    index : str
       The name of the variable in the dataset that contains the climate index values.

    See climdex.analyse.do_extract_information() for details on input arguments.

    Returns
    -------
    The preprocessed and filtered input stacked ensamble dataset, including
    the target (and baseline when requested) time periods.
    """
    # - - - - - - - - - -
    LOGGER = utils.get_logger(__name__)
    # - - - - - - - - - -
    if ensemble_files is None:
        return None

    if index is None:
        raise ValueError("Please provide the label of the index variable in the dataset.")

    if isinstance(ensemble_files, str) or \
       isinstance(ensemble_files, Path):
        ensemble_files = [ ensemble_files ]

    ensemble_files = [ Path(x) for x in ensemble_files ]

    if isinstance(sign_test, str):
        sign_test = [sign_test]
    # - - - - - - - - - -

    LOGGER.debug("Loading datasets...")
    # decode_times might decode not only time coords, but variables too, hard to control: better off then manually decode TIME_DIM
    ensemble_ds = xr.open_mfdataset(
                     ensemble_files, parallel=False, engine='netcdf4',
                     concat_dim=MODELS_DIM, combine='nested',
                     decode_times=False)
    LOGGER.debug("Datasets metadata loaded. Variables: %s / Dims: %s", list(ensemble_ds), list(ensemble_ds.dims))

    # decoding TIME dimension if it exists:
    if TIME_DIM in ensemble_ds:
        from xarray.coding import times
        units    = ensemble_ds[TIME_DIM].attrs['units']       if 'units' in ensemble_ds[TIME_DIM].attrs else None
        calendar = ensemble_ds[TIME_DIM].attrs['calendar'] if 'calendar' in ensemble_ds[TIME_DIM].attrs else None
        LOGGER.debug("Decoding time coordinates '%s' (%s)", units, calendar)
        ensemble_ds[TIME_DIM] = times.decode_cf_datetime(ensemble_ds[TIME_DIM], units=units, calendar=calendar)


    # remove all_NAs slices: they might be there for rasdaman datacube model (fill in all models to make wcs_import work)
    #
    empty_models = find_empty_models( ensemble_ds[index] )
    if len(empty_models) > 0:
        # empty_models_str = [ cmodels.get_model(x) for x in empty_models ]  # NO: model indices are already faked by pre-load model filtering above
        LOGGER.warning("Discarding empty (rasdaman placeholders / all NAs) models found in the ensemble: #%d (%s)", len(empty_models), empty_models)
        ensemble_ds = ensemble_ds.drop_sel(model=empty_models, errors='raise')

    # keep only index variable
    #
    assert index in ensemble_ds
    extra_vars = list(ensemble_ds.keys())
    extra_vars.remove(index)
    ensemble_ds = ensemble_ds.drop_vars( extra_vars )
    LOGGER.debug("Discarded extra-variables: %s", extra_vars)

    # get spatial ref
    #
    LOGGER.info("Fetching coordinate reference system...")
    if ensemble_ds.rio.crs is None:
        native_crs = get_crs( ensemble_files[0] )
        LOGGER.debug("Native input CRS found: %.40s...", native_crs)
        ensemble_ds = ensemble_ds.rio.write_crs( native_crs )

    native_crs = CRS( ensemble_ds.rio.crs ) # I want pyproj, not rasterio

    # input time range
    tmin = ensemble_ds.coords[TIME_DIM][0].values
    tmax = ensemble_ds.coords[TIME_DIM][-1].values
    LOGGER.debug("Input data time range: [%s, %s]", tmin, tmax)

    # time filter
    #
    if tint is None:
        target_ds = ensemble_ds.copy( deep=False )
    else:
        # handle multiple time-intervals
        subtarget_dss = [None]*len(tint)
        for i,t in enumerate(tint):
            # integrity checks
            #
            if (len(t) != 2):
                raise ValueError("'tint' time filter shall be an array/tuple of 2 elements (from,to): {}".format(t))
            if (t[0] > t[1]):
                raise ValueError("Invalid time filter: first element shall be prior to the second:{}".format(t))
            if ((np.datetime64(t[0]) > tmax) or
                (np.datetime64(t[1]) < tmin)) and not lenient:
                raise ValueError("Input time filter {} does not overlap with input range: {}-{}".format(
                    t, tmin, tmax))
            if ((np.datetime64(t[0]) < tmin) or
                (np.datetime64(t[1]) > tmax)) and not lenient:
                raise ValueError("Input time filter {} does not fully overlap with input range: {}-{}".format(
                    t, tmin, tmax))
            # actual filtering
            #
            LOGGER.debug("Applying '%s' time filter...", t)
            subtarget_dss[i] = ensemble_ds.loc[{ TIME_DIM:slice(*t) }]

        # stack all back together
        #target_ds = xr.merge( subtarget_dss ) --> MEMORY LEAK
        target_ds = xr.combine_by_coords( subtarget_dss ) 
        tsteps    = target_ds.dims[TIME_DIM]
        LOGGER.info("Filtered input over %s: %d time-steps left.", tint, tsteps)

        if (tsteps == 0):
            if lenient:
                return None
            else:
                raise ValueError("Input time filter {} does not intersect with input range: {}-{}"
                        .format(tint, tmin, tmax))

    # re-set crs
    target_ds = target_ds.rio.write_crs( ensemble_ds.rio.crs )

    # baseline
    #
    if baseline is not None:
        # ensure all baseline time range is present
        if ((np.datetime64(baseline[0]) < tmin) or
            (np.datetime64(baseline[1]) > tmax)):
            raise ValueError("Input baseline {} does not fully overlap with input range: {}-{}".format(
                baseline, tmin, tmax))

        baseline_ds = ensemble_ds.loc[{ TIME_DIM:slice(*baseline) }]
        baseline_ds = baseline_ds.rio.write_crs( ensemble_ds.rio.crs )
        bsteps    = baseline_ds.dims[TIME_DIM]
        LOGGER.debug("Baseline dataset extracted: %d time-steps.", bsteps)

        # merge with target time interval to run pre-processing on a single xarray:
        # NOTE: Dataset.merge causes memory leak -> use Dataset.concat?
        #target_ds.update( baseline_ds ) #--> no, different behaviour!
        #target_ds = xr.merge([baseline_ds, target_ds]) 
        target_ds = xr.combine_by_coords([baseline_ds, target_ds]) 
        tsteps    = target_ds.dims[TIME_DIM]
        LOGGER.info("Target merged with baseline: %d time-steps overall.", tsteps)
        baseline_ds.close()

    # load dem
    #
    if dem is not None:
        LOGGER.debug("Loading DEM file '%s'...", dem)
        xyslice_da = target_ds[index][{ MODELS_DIM:0, TIME_DIM:0 }]
        xyslice_da = xyslice_da.rio.write_crs( target_ds.rio.crs )
        dem_ds = load_dem( dem, match_da=xyslice_da )
        dem_var = list(dem_ds)[0] # TODO

    # final coords:
    timesteps = target_ds[TIME_DIM].values
    models_id = target_ds[MODELS_DIM].values

    # spatial xy clipping:
    #
    if xyclip is not None:
        xyclip = to_gpd_series( xyclip, \
                    crs_if_none='epsg:4326', \
                    target_crs=target_ds.rio.crs )
                   # crs_if_none=target_ds.rio.crs, 
        # xyclip.set_crs('epsg:4326', inplace=True)
        if (xyclip_limit is not None) and (xyclip_limit < len(xyclip)):
            xyclip = xyclip[:xyclip_limit]
            LOGGER.info("XY clipping geometries limit set to %d", len(xyclip))

    if xyclip is not None:
        # TODO verify overlap or try/catch for 'rioxarray.exceptions.NoDataInBounds: No data found in bounds.' error
        LOGGER.info("Applying spatial mask...")
        LOGGER.debug("Clipping geometry: %.30s...  [%.10s...]", xyclip, xyclip.crs)
        target_ds = target_ds.rio.clip(xyclip, crs=xyclip.crs, all_touched=True, drop=True, invert=False)
        LOGGER.debug("XY clip set. Now grid is: %s", target_ds.rio.shape)
        # add clipping information in metadata
        xyclip_attr = f"{[ v for v in xyclip.index.values ]}"
        if  xyclip.index.name is None:
            xyclip.index.name = 'index'
        utils.add_or_append_attr(target_ds, attr=xyclip.index.name, value=xyclip_attr)

    # apply height-filter mask (not clipping here, just masking)
    #
    if hfilter is not None:
        LOGGER.info("Applying %s elevation filter...", hfilter)
        # dem has same shape as input data (reprojec_match), so we can apply mask directly
        assert dem_ds.rio.shape == target_ds.rio.shape
        count_pre = target_ds[index].count().to_dict()['data'] # how to get the count() value from count() output
        if hfilter[0] is not None:
            target_ds = target_ds.where(dem_ds[dem_var] >= hfilter[0])

        if hfilter[1] is not None:
            target_ds = target_ds.where(dem_ds[dem_var] <= hfilter[1])
        #
        count_post = target_ds[index].count().to_dict()['data'] # how to get the count() value from count() output
        count_xyout = (count_pre-count_post) / (len(timesteps)*len(models_id))
        LOGGER.debug("Filter applied: %d pixels excluded by mask.", count_xyout)
        # re-set CRS which gets lost here:
        target_ds = target_ds.rio.write_crs( native_crs )


    # filter values that are significantly different from baseline
    if (sign_test is not None) and (len(sign_test) > 0):
        assert(baseline is not None)
        baseline_ds  = target_ds.loc[{ TIME_DIM:slice(*baseline) }]
        for t in tint:
            subtarget_ds = target_ds.loc[{ TIME_DIM:slice(*t) }]
            # compute significant pixels
            LOGGER.info("Selecting only statistically different values of %s with respect to baseline (%d%% confidence)...", t, sign_conf)
            robust_da = filter_significant(
                            subtarget_ds[index],
                            baseline_ds[index],
                            core_dim   = sign_test,
                            conf_level = sign_conf)
            # assign new values back to original dataset: back to original dataset:
            target_ds[index].loc[{ TIME_DIM:slice(*t) }] = robust_da

    LOGGER.debug("Extracted dataset: %s", target_ds)

    # cleanup
    ensemble_ds.close()
    if baseline is not None:
        baseline_ds.close()

    return target_ds


# ------------------------------------------------------------------------------
#

def add_baseline_attr(data, baseline, baseline_op:OpType, taggr) -> xr.DataArray:
    """
    Adds information on the baseline operation in the input dataset ('history' attribute).

    Parameters
    ==========
        data : xr.DataArray or xr.Dataset
    """
    # - - - - - - - - - -
    if data is None:
        return None
    if baseline is None:
        return None
    if baseline is None:
        raise ValueError("Missing baseline comparison operator.")
    if isinstance(taggr, list):
        if len(taggr) > 1:
            raise ValueError("Only single aggregator accepted: {}".format(taggr))
        else:
            taggr = taggr[0]
    # - - - - - - - - - -

    bint = f"{baseline[0]}-{baseline[1]}"
    bline_attr = f"{baseline_op.name} with {taggr} time-aggregated {bint} baseline"
    utils.add_or_append_attr(data, attr=HISTORY_ATTR, value=bline_attr)

    return data

# ------------------------------------------------------------------------------
#

def add_hfilter_attr(data, hfilter) -> xr.DataArray:
    """
    Adds information on the altitude filtering applied to a dataset ('history' attribute).

    Parameters
    ==========
        data : xr.DataArray or xr.Dataset
    """
    # - - - - - - - - - -
    if data is None:
        return None
    if hfilter is None:
        return None
    # - - - - - - - - - -

    hfilter_attr = f"{hfilter} altitude pre-filtering"
    utils.add_or_append_attr(data, attr=HISTORY_ATTR, value=hfilter_attr)

    return data

# ------------------------------------------------------------------------------
#

def add_aggregation_attr(ds:xr.Dataset, index, dim, aggr, lenient=True) -> xr.DataArray:
    """
    Adds information on the aggregation applied to a dataset over a given dimension
    ('history' and 'cell_methods' attributes).
    """
    # - - - - - - - - - -
    if ds is None:
        return None
    if index not in ds:
        raise ValueError("'{}' not found in dataset.".format(index))
    if dim is None:
        return None
    if aggr is None:
        return None
    if isinstance(aggr, list):
        if len(aggr) > 1:
            if not lenient:
                raise ValueError("Only single aggregator accepted: {}".format(aggr))
            else:
                return None
        else:
            aggr = aggr[0]
    # - - - - - - - - - -

    aggr_attr = f"{aggr} aggregator over {dim} dimension"
    utils.add_or_append_attr(ds, attr=HISTORY_ATTR, value=aggr_attr)

    new_cell_method = f"{dim}: {aggr}"
    utils.add_or_append_attr(ds[index], attr=CMETHODS_ATTR, value=new_cell_method)

    return ds


# ------------------------------------------------------------------------------
#
def filter_significant(x_da:xr.DataArray, y_da:xr.DataArray, core_dim, conf_level=DEFAULT_SIGNIFICANCE_CONF, **kwargs) -> xr.DataArray:
    """
    Runs a (Wilconcox) statistical significance test on an input dataset against a reference,
    along the dim dimension(s): the null hypothesis is that the two related paired samples
    come from the same distribution.

    By default the test is two-sided, use the kwargs to change the behaviour
    (see `scipy.stats.wilcoxon`).

    NOTE: X and Y shall have the same shape for the Wilcoxon ranked test to be feasible.
    TODO: find alternative tests for unequal related (not independent) sample sizes.

    Parameters
    ----------
    x_da : xr.DataArray
        The data X to be tested and filtered.

    y_da : xr.DataArray
        The reference data Y against which to test the change change of location of X.

    core_dim : str or sequence of str (or None)
        When not None, the (sequence of) dimension(s) along which to group the
        data values for a statistical significant testing with respect
        to the baseline reference.

    conf_level : numeric
        The confidence level [%] to be used as threshold for filtering statistically significant
        values along the provided 'core_dim' dimensions.

    **kwargs are passed on to the scipy.stats.wilcoxon(...) function.

    Return
    ------
    A data array with the same shape as the input X, with suppression (to nan) of the not statistically
    significant values.

    Examples
    --------
    >>> filter_significant(x_da, y_da, 't', conf_level=95)
    >>> filter_significant(x_da, y_da, ['x','y'], conf_level=99, alternative="greater", mode="approx")

    """
    # - - - - - - - - - -
    if x_da is None:
        return None

    if y_da is None:
        raise ValueError("Missing reference dataset y_da.")

    if core_dim is None or len(core_dim) == 0:
        raise ValueError("Please provide 1+ dimensions along which to test statistical significance.")

    if isinstance(core_dim, str):
        core_dim = [core_dim]

    if conf_level not in range(1,100):
        raise ValueError("Confidence level shall be in the [1,100[ range. Found: {}".format(conf_level))

    if x_da.shape != y_da.shape:
        raise ValueError("Input data shall have the same shape for Wilcoxon ranked test. Found: {} Vs {}.".format(x_da.shape, y_da.shape))

    if x_da.dims != y_da.dims:
        raise ValueError("Input data shall have the same dimensions for Wilcoxon ranked test. Found: {} Vs {}.".format(x_da.dims, y_da.dims))

    if len(set(core_dim)) >= len(set(x_da.dims)):
        raise ValueError("Test dimension(s) should be a subset of the available array dimensions: {}".format(core_dim))

    if any(d not in x_da.dims for d in core_dim):
        raise ValueError("Not all input test dimensions were found in input dataset: {}".format(core_dim))

    LOGGER = utils.get_logger(__name__)
    # - - - - - - - - - -

    wilcoxon_kwargs = { 'alternative':'two-sided' }
    wilcoxon_kwargs.update(kwargs)

    # compute difference between target and baseline
    diff_da = x_da.copy( deep=True )
    diff_da.values = diff_da.values - y_da.values
    diff_da = diff_da.chunk({d:len(diff_da.coords[d]) for d in core_dim}) # rechunk optimization
    is_dask = (diff_da.chunk is not None)

    #### UFUNC wrapper######################################
    def do_wilcoxon(da, **kwargs):
        LOGGER.debug("Running Wilcoxon test on input with shape %s (kwargs:%s)", da.shape, kwargs)
        w_res = stats.wilcoxon(x = np.ndarray.flatten(da), **kwargs)
        return w_res
    ########################################################
    # TODO optimization : dropna along x/y ,then compute, then restore NAs ?
    w_scores, w_pvalues = xr.apply_ufunc(
                    do_wilcoxon, 
                    diff_da, 
                    input_core_dims=[core_dim],
                    output_core_dims=[[], []], # wicoxon returns score + p-value
                    kwargs=wilcoxon_kwargs,
                    vectorize=True,
                    dask='parallelized')

    # FIXME remove this, very verbose
    LOGGER.debug("w-scores: %s", np.ndarray.flatten(w_scores.values))
    LOGGER.debug("p-values: %s", np.ndarray.flatten(w_pvalues.values))

    # suppress non robust elements, i.e. p-value is > alpha level
    # NOTE: W score can also be 0 but it does not mean that the "difference"
    #       between X and Y median is 0. Wilcoxon is based on ranks.
    alpha_level = (1 - (conf_level / 100.))
    beyond_alpha = (w_pvalues.values > alpha_level).sum()
    sample_size = np.prod([ len(x_da.coords[dim]) for dim in core_dim ])

    #LOGGER.warn("BEFORE: %s", np.ndarray.flatten(x_da.values))
    LOGGER.debug("Suppressing %d (%d-sized) samples with p > %.2f...", beyond_alpha, sample_size, alpha_level)
    filtered_da = x_da.where( w_pvalues <= alpha_level, drop=False )
    #LOGGER.warn("AFTER : %s", np.ndarray.flatten(x_da.values))

    #PROBLEM: this trend returns only 1 value (instead of 40): why?
    #    >>> trends._extract_trend(index, idir=IDIR, scenario=rcp, tint=years, baseline=bline, baseline_op=enums.OpType.ratio, sign_test=[MODELS_DIM, 'x', 'y'], sign_conf=30, taggr='max', xyaggr='max', eaggr='max')[
    return filtered_da.load()

