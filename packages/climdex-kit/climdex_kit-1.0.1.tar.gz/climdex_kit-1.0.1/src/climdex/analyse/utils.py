
"""
Utilities for the climdex.analyse module.
"""

import re
from pathlib import Path

import numpy as np
import geopandas as gpd
from shapely.geometry.base import BaseGeometry
import xarray as xr
from pyproj import CRS
from rasterio.enums import Resampling

from ..utils import *
from ..constants import *
from .enums import AggrType
from .enums import AnalysisType
from .enums import FmtType
from .enums import OpType

# >>> help(xr.DataArray.quantile)
# {"linear", "lower", "higher", "midpoint", "nearest"}
DEFAULT_QUANTILE_INTERP = 'midpoint'
DEFAULT_RESAMPLING = Resampling.med
SCENARIO_DIM = 'scenario'
XYCLIP_ATTR = 'clip_geom'

# ------------------------------------------------------------------------------
# Aggregation validity check
#
def check_aggr_type( x ) -> bool:
    """
    `True` if the input is a valid aggregation type; `False` otherwise.
    If input is `None`, returns `False`.
    """
    return x is not None and any(re.match('^{}$'.format(expr), x) for expr in AggrType.values())

def parse_aggr_type(x) -> AggrType:
    """Finds the enumeration associated to aninput string (eg. parse('q3' -> quartile)"""
    matches = { expr:re.match('^{}$'.format(expr), x) for expr in AggrType.values()}
    out = {k:v for k,v in matches.items() if v is not None}
    assert len(out) <= 1
    return AggrType(out.popitem()[0]) if len(out)==1 else None

# enum -> xarray function mappings
xds_funcs = {
    AggrType.min  : xr.Dataset.min,
    AggrType.max  : xr.Dataset.max,
    AggrType.avg  : xr.Dataset.mean,
    AggrType.med  : xr.Dataset.median,
    AggrType.quartile   : xr.Dataset.quantile,
    AggrType.percentile : xr.Dataset.quantile
}

xda_funcs = {
    AggrType.min  : xr.DataArray.min,
    AggrType.max  : xr.DataArray.max,
    AggrType.avg  : xr.DataArray.mean,
    AggrType.med  : xr.DataArray.median,
    AggrType.quartile   : xr.DataArray.quantile,
    AggrType.percentile : xr.DataArray.quantile,
}

def aggr_type_to_dsf( x:AggrType ):
    """Returns the reference to the xarray.Dataset function that implements the given aggregation type."""
    return xds_funcs[x]

def aggr_type_to_dsf( x:AggrType ):
    """Returns the reference to the xarray.DataArray function that implements the given aggregation type."""
    return xda_funcs[x]

# ------------------------------------------------------------------------------
# fetch CRS from NetCDF
#
def get_crs(nc_file) -> CRS:
    """
    Extracts the Coordinate Refrence System from a NetCDF file.

    The method will search for a CRS definition, respectively:

     - as a 'spatial_ref' attribute of one of the file variables, or
     - as 'proj4' attribute of the 'crs' variable

    (Climate and Forecasts CF convention).

    Parameters
    ----------
    nc_file : str or Path
        The path to the NetCDF file.

    Returns
    -------
    The `pyproj.CRS` object if found, `None` otherwise.

    See Also
    --------
    https://corteva.github.io/rioxarray/stable/getting_started/crs_management.html#Search-order-for-the-CRS-(DataArray-and-Dataset)
    """
    # FIXME do as rio package to better stick with CF convention, see link above
    # - - - - - - - - - -
    LOGGER = get_logger(__name__)
    # - - - - - - - - - -
    if nc_file is None:
        return None

    nc_file = Path(nc_file)
    if not nc_file.exists():
        raise ValueError("Input file not found: '{}'".format(nc_file))
    # - - - - - - - - - -

    crs = None

    with xr.open_dataset( nc_file, engine='netcdf4' ) as nc_ds:
        spatial_ref = [ nc_ds[var].attrs for var in nc_ds if SPREF_ATTR in nc_ds[var].attrs ]
        if len(spatial_ref) == 0:
            # alternative: crs var
            if CRS_VAR in nc_ds:
                if PROJ4_ATTR in nc_ds[CRS_VAR].attrs:
                    crs = CRS( nc_ds[CRS_VAR].attrs[PROJ4_ATTR] )
                else:
                    LOGGER.debug("No %s attribute in %s variable found.", PROJ4_ATTR, CRS_VAR)
            else:
                LOGGER.warn("No CRS found in file.")
        elif len(spatial_ref) > 1:
            LOGGER.debug("Multiple CRS definitions found.")
        elif len(spatial_ref) == 1:
            crs = CRS.from_cf( spatial_ref[0] )

    return crs

# ------------------------------------------------------------------------------
# identify "empty models"
#
def find_empty_models(ensemble_da, mdim=MODELS_DIM):
    """
    Identifies models of the ensemble where all data is NaN.
    (eg. when used as filler along the "M" model dimension of a WCS datacube).

    Parameters
    ----------
    ensemble_da : DataArray
        The ND array containg all models of a climate data ensemble.

    Returns
    -------
    The indices (.sel) of the models in the ensemble (`mdim` dimension)
    where each data value in the spatio-temporal sub-cube is `nan`.

    See also
    --------
    np.isnan
    """
    # - - - - - - - - - -
    if ensemble_da is None:
        return None

    if not mdim in ensemble_da.dims:
        raise ValueError("{} dimension not found in input DataArray: {}".format(mdim, ensemble_da.dims))
    # - - - - - - - - - -

    empty_models = list()

    for m in ensemble_da[mdim].values:
        model_np = ensemble_da.sel(model=m).to_numpy()
        is_empty = np.sum(np.logical_not( np.isnan(model_np) )) == 0
        if is_empty:
            empty_models.append(m)

    return empty_models


# ------------------------------------------------------------------------------
# apply aggregation function to xr.Dataset
#
def apply_aggr(ds:xr.Dataset, aggr:str, dim, skipna=True, **kwargs) -> xr.Dataset:
    """
    Applies the given aggregation to a dataset.

    Parameters
    ==========
    ds : xr.Dataset
        The input dataset.

    aggr : str
        The aggregation string.

    dim : str (or sequence of str)
        The dimension(s) of the input dataset along which to apply the aggregation.

    skipna : bool
        Whether to exlude NAs from the computations.

    **kwargs : dict
        Arguments to be passed on to the aggregating function.

    Return
    ======
    The (n-m)-dimensional dataset after applying the selected aggregation
    to the n-dimensional `ds` input along the m dimensions.
    """
    # - - - - - - - - - -
    if ds is None:
        return None

    if aggr is None:
        return ds

    if isinstance(dim, str):
        dim = [dim]

    for d in dim:
        if d not in ds.dims:
            raise ValueError("'{}' not found in the input dimensions: {}".format(dim, list(ds.dims)))

    aggr_type = parse_aggr_type( aggr )
    if aggr_type is None:
        raise ValueError("'{}' is not a valid aggregation expression. Allowed: {}".format(aggr, AggrType.values()))
    # - - - - - - - - - -

    # FIXME can this be made parameterized/one aggregation call? tried with Dataset.map, unsuccessfully
    #       see climdex.analyse.utils.aggr_type_to_dsf( x:AggrType )

    if AggrType.min == aggr_type:
        aggr_ds = ds.min( dim=dim, skipna=skipna, **kwargs ) # skipna? TODO Ask Alice

    elif AggrType.max == aggr_type:
        aggr_ds = ds.max( dim=dim, skipna=skipna, **kwargs )

    elif AggrType.avg == aggr_type:
        aggr_ds = ds.mean( dim=dim, skipna=skipna, **kwargs )

    elif AggrType.med == aggr_type:
        aggr_ds = ds.median( dim=dim, skipna=skipna, **kwargs )

    elif aggr_type in [AggrType.quartile, AggrType.percentile]:
        q = int(aggr[1])*25 / 100. if AggrType.quartile == aggr_type else \
            int(aggr[1:])   / 100.
        aggr_ds = ds.chunk({ x : -1 for x in dim })\
                    .quantile( q=q, interpolation=DEFAULT_QUANTILE_INTERP, dim=dim, skipna=skipna, **kwargs )
        del aggr_ds.coords['quantile'] # I want to manually handle the quantile information
        # CHUNK -> avoid "ValueError: dimension model on 0th function argument to apply_ufunc with dask='parallelized' consists of multiple chunks, but is also a core dimension."
        # [!] 

    elif AggrType.perc_pos == aggr_type:
        aggr_ds = apply_perc_positive(ds, dim)

    elif AggrType.perc_neg == aggr_type:
        aggr_ds = apply_perc_positive(ds, dim, negative=True)

    else:
        raise RuntimeError("(Should not be here) '{}' aggregation not handled.".format(aggr_type))

    # crs gets discarded: need to re-set it
    aggr_ds = aggr_ds.rio.write_crs( ds.rio.crs )

    return aggr_ds


# ------------------------------------------------------------------------------
# compute percentage of positive/negative values of a xr.Dataset along 1+ dimension(s)
#
def apply_perc_positive(ds:xr.Dataset, dim, negative=False, offset=0) -> xr.Dataset:
    """
    Computes the percentage of values that are positive (or negative) along
    one or more dimensions of a dataset.

    Parameters
    ==========
    ds : xr.Dataset
        The input dataset.

    dim : str (or sequence of str)
        The dimension(s) of the input dataset along which to apply the aggregation.

    negative : bool (default False)
        Set to True to compute the percentage of negative (instead of positive)
        values along the given dimension(s).

    offset : numeric
        The offset value with respect to distinguish postive (> offset)
        and negative (< offset).

    Return
    ======
    The (n-m)-dimensional dataset after applying the selected aggregation
    to the n-dimensional `ds` input along the m dimensions.
    """
    # - - - - - - - - - -
    if ds is None:
        return None

    if isinstance(dim, str):
        dim = [dim]

    for d in dim:
        if d not in ds.dims:
            raise ValueError("'{}' not found in the input dimensions: {}".format(dim, list(ds.dims)))
    # - - - - - - - - - -

    # [!]
    # notnull/where etc: they reorders dimensions and this can cause issues in serialization to NetCDF
    # -> re-transpose back to original structure? No: coordinates get flipped and georeference breaks

    nan_mask_da = (ds.notnull()\
    #                .transpose( *list(ds.dims) )\
                    .any( dim=dim ))

    N = np.prod([ ds.dims[d] for d in dim ])
    ok_cond = (ds < offset) if negative else (ds > offset)
    aggr_ds = (ds.where(ok_cond)\
    #             .transpose( *list(ds.dims) )\
                 .count(dim=dim, keep_attrs=True)\
                 * 100) / N

    # preserve all-nan sections:
    aggr_ds = aggr_ds.where(nan_mask_da)

    return aggr_ds



# ------------------------------------------------------------------------------
# apply comparison with baseline
#
def apply_op(da:xr.DataArray, baseline_da:xr.DataArray, op:OpType=None) -> xr.Dataset:
    """
    Applies a selected operation between a target dataset, and the baseline.

    NOTE: that the shapes of the 2 dataset shall coincide.
    NOTE: DataArray (not Dataset) as input to force variable alignment and simplify function.

    Parameters
    ==========
    da : xr.DataArray
        The input dataset.

    baseline_da : xr.DataArray
        The baseline dataset.

    op : OpType
       The operation to be applied: `da <op> baseline_da`

    Return
    ======
    The same input dataset, whose values have been replaced by the
    output of the comparison with the baseline data.
    """
    # - - - - - - - - - -
    if op is None:
        return da

    if baseline_da is None:
        return da

    if da is None:
        raise ValueError("Input dataset is None.")

    if da.dims != baseline_da.dims:
        raise ValueError("Target and baseline datasets' shapes differ: {} / {}".format(da.dims, baseline_da.dims))
    # - - - - - - - - - -

    # will work on the internal NumPy arrays since target and baseline are not aligned (time coord of course is not the same)
    # xr.align(da, baseline_da, join='exact') -> Error

    out_da = da.copy() # deep?

    if OpType.diff == op:
        out_da.data = ( da.data - baseline_da.data )
        # check: out_da.values

    elif OpType.perc_diff == op:
        #da_ref = np.nanmax(da.data) - np.nanmin(da.data)
        da_ref = baseline_da
        #if da_ref == 0:
        #    raise ValueError("Input data range is 0: cannot compute percentage differences.")
        #else:
        out_da.data = 100. * ( da.data - baseline_da.data ) / da_ref.data

    elif OpType.ratio == op:
        out_da.data = ( da.data / baseline_da.data )
        # check: out_da.values

    else:
        raise RuntimeError("(Should not be here) '{}' operation not handled.".format(op))

    return out_da



# ------------------------------------------------------------------------------
# Load DEM
#
def load_dem(dem, dem_var=None, match_da:xr.DataArray=None, xyclip=None) -> xr.Dataset:
    """
    Loads the given DEM from file as an xr.Dataset, matching its
    projection and spatial resolution to the given target.

    Parameters
    ==========
    dem : str or Path
        The path to the DEM file.

    dem_var : str
        The name of the variable containing the DEM information in the input file.
        If None, it will assume the name of the unique variable, or
        the 'dem' variable will be searched for.

    match_da : xr.DataArray
        The 2D dataset onto which spatial grid the DEM will be matched.

    xyclip : gpd.GeoSeries
        Optional spatial clipping to be applied to the DEM extent: pixels outside
        the clipping will be removed.

    Returns
    =======
    The DEM dataset, reprojected and interpolated on the target spatial grid.

    See Also
    ========
    xr.Dataset.rio.reproject_match
    """
    # - - - - - - - - - -
    if dem is None:
        return None

    dem = Path(dem)
    if not dem.exists():
        raise ValueError("DEM file not found: {}".format(dem))

    if (match_da is not None) and (match_da.rio.crs is None):
        raise ValueError("Target DataArray is missing CRS.")
    # - - - - - - - - - -

    LOGGER = get_logger(__name__)

    dem_ds = xr.open_dataset( dem )

    # deduce which is the DEM variable in the dataset:
    if dem_var is not None:
        if dem_var not in dem_ds:
            raise ValueError("'{}' variable not found in the input dataset. Available: {}".format(dem_var, list(dem_ds)))
    else:
        if len(dem_ds) == 1:
            dem_var = list(dem_ds)[0]
        elif DEM_VAR in dem_ds:
            dem_var = DEM_VAR
        else:
            raise ValueError("'{}' variable not found in DEM file: {}".format(DEM_VAR, dem))

    # align spatial dims (otherwise rio.reproject_match fails)
    dem_ds = dem_ds.rename({
                 dem_ds.rio.x_dim: match_da.rio.x_dim,
                 dem_ds.rio.y_dim: match_da.rio.y_dim  })
    # deduce CRS
    if dem_ds.rio.crs is None:
        dem_crs = get_crs( dem )
        if dem_crs is None:
            if match_da is not None:
                LOGGER.warn("Could not extract CRS from DEM file ('%s'): assuming target DataArray's projection.", dem)
                dem_crs = CRS( match_da.rio.crs )
            else:
                raise ValueError("Could not extract CRS from DEM file ('{}').".format(dem))
        #
        dem_ds = dem_ds.rio.write_crs( dem_crs )
    # reprojection?
    if match_da is not None:
        same_crs = dem_crs.is_exact_same( match_da.rio.crs )
        same_res = dem_ds.rio.resolution() == match_da.rio.resolution() # TODO False also on -Yres/+Yres
        same_bnd = dem_ds.rio.bounds() == match_da.rio.bounds()
        if (not same_crs) or (not same_res) or (not same_bnd):
            # sample 2D XY grid of input datacube
            dem_ds = dem_ds.rio.reproject_match( match_da, resampling=DEFAULT_RESAMPLING )
            # TODO CLIP BEFORE reshaping?
            #dem_ds = dem_ds.rio.reproject(
            #        dst_crs = match_da.rio.crs,
            #        shape   = match_da.shape,
            #        resampling = Resampling.bilinear, nodata=np.nan)
            LOGGER.debug("DEM reprojected to match input spatial grid.")
    # clipping?
    if xyclip is not None:
        xyclip = to_gpd_series(  xyclip, crs_if_none=dem_ds.rio.crs, target_crs=dem_ds.rio.crs )
        dem_ds = dem_ds.rio.clip(xyclip, crs=xyclip.crs, drop=True, invert=False)
        LOGGER.debug("DEM XY clip set.")

    return dem_ds


# ------------------------------------------------------------------------------
# input spatial clipping harmonizazion
#
def to_gpd_series(xyclip, crs_if_none=None, target_crs:CRS=None) -> gpd.GeoSeries:
    """
    Imports a spatial clipping, reprojecting it to a target CRS.

    Parameters
    ==========
    xyclip : shapely.Geometry or gpd.GeoSeries or gpd.GeoDataFrame
        The definition of the spatial 1+ geometries.
        In case of a geometry, or a GeoSeries with no CRS attached,
        the `xycrs` is assumed.

    crs_if_none : CRS
        The CRS of the input xyclip when not specified: in case of a GeoSeries,
        the attached CRS, if found, has priority.

    target_crs : CRS
        The target CRS to which the geometries will be optionally reprojected to.

    Returns
    =======
    The input clipping as a GeoSeries or GeoDataFrame, optionally reprojected to the `target_crs`.
    """
    # - - - - - - - - - -
    if xyclip is None:
        return None
    # - - - - - - - - - -
    LOGGER = get_logger(__name__)

    if isinstance(xyclip, BaseGeometry):
        xyclip = gpd.GeoSeries(xygeom, crs=crs_if_none)
    elif isinstance(xyclip, gpd.GeoDataFrame):
        xyclip = gpd.GeoSeries(xyclip.geometry)
    elif not isinstance(xyclip, gpd.base.GeoPandasBase):
        raise ValueError("Input clip shall be either Shapely Geometry or GeoPandas GeoSeries/GeoDataFrame: {}".format(type(xyclip)))

    if (xyclip.crs is None) and (crs_if_none is not None):
        xyclip = xyclip.set_crs( crs_if_none )

    if xyclip.crs is None:
        raise ValueError("No CRS found in input, please provide a valid crs_if_none projection to assign.")

    if target_crs is not None:
        #LOGGER.debug("xyclip.crs: %s (%s)", xyclip.crs, type(xyclip.crs))
        if not xyclip.crs.is_exact_same(target_crs):
            xyclip = xyclip.to_crs( crs=target_crs )
            LOGGER.debug("XY clip geometry reprojected to target CRS: %.30s", xyclip.geometry.iloc[0])

    return xyclip


# ------------------------------------------------------------------------------
# format analysis output file names
#
def craft_file_name(an_type:AnalysisType, index:str, scenario:str,
        tint=None, baseline=None, baseline_op:OpType=None,
        taggr:str=None, eaggr:str=None, xyaggr:str=None, hfilter=None,
        ofmt:FmtType=None) -> str:
    """
    Crafts the name of the output file for a given analysis.

    Parameters
    ==========
    an_type : AnalysisType
        The type of the analysis that was requested.

    index : str
        The climate index that was analysed.

    scenario : str
        The climate emissions scenario under which the analysis took place.

    tint : str or array_like (optional)
        The [tmin[,tmax]] input time subset.

    baseline : array_like (optional)
        [tmin,tmax] array of time steps the define the baseline of the analysis;
        use the `baseline_op` to define the type of comparison to be applied.

    baseline_op : str or OpType (optional)
        The type of operation to be applied with respect to the `baseline`:
        `TARGET baseline_op BASELINE`.

    baseline_op : OpType (optional)
        The comparison operator with respect to the baseline.

    taggr : str (optional)
        The temporal aggregator used to slice out the time dimension.
        
    eaggr : str (optional)
        The aggregator used to represent the climate models ensemble..

    xyaggr : str (optional)
        The spatial aggregator used to slice out the horizontal spatial dimensions.

    hfilter : 2D array_like (optional)
        The [hmin,hmax] altitude filters, maximuem one 'None' value is allowed.

    ofmt : FmtType (optional)
        The output format of the file (no file extension is appended if None)

    Returns
    =======
    The crafted name of the analysis output.

    Examples
    ========
    >>> craft_file_name(AnalysisType.map2d, 'su', 'rcp85', 
            tint=[2041,2050], baseline=[1980,2010], baseline_op=OpType.diff,
            taggr='avg', eaggr='q3', ofmt=FmtType.json)
    'map_su_rcp85_2041-2050_bl1980-2010-diff_eq3_tavg.json'
    """
    # - - - - - - - - - -
    LOGGER = get_logger(__name__)

    if an_type is None:
        raise ValueError("Provide an analysis type.")

    if index is None:
        raise ValueError("Provide the analysed index.")

    if scenario is None:
        raise ValueError("Provide the analyis scenario.")

    if tint is not None:
        if any(isinstance(x, list) for x in tint):
            if (len(tint) > 1):
                tint = None # add tint in file name only if there is one interval, otherwise too much cluttering
            else:
                tint = tint[0]
        if tint is not None and len(tint) == 1:
            tint.append(None)
        if tint is not None and len(tint) != 2:
            raise ValueError("Provide a valid [tmin[,tmax]] time interval.")

    if baseline is not None:
        if len(baseline) != 2:
            raise ValueError("Provide a valid [tmin,tmax] baseline interval.")

    if bool(baseline) and not bool(baseline_op):
        raise ValueError("Provide the baseline operation.")

    if not bool(baseline) and bool(baseline_op):
        LOGGER.warn("Ignoring baseline operation '%s' as baseline interval was not provided.", bl_op)

    if hfilter is not None:
        if len(hfilter) != 2:
            raise ValueError("Provide a valid [hmin,hmax] altitude filter specification.")
        if all(h is None for h in hfilter):
            LOGGER.debug("Ignoring double-None hfilter input.")
            hfilter = None
    # - - - - - - - - - -

    # constants
    SEP = '_'
    TS  = '-'
    BASELINE_PREFIX = 'b'
    ENSEMBLE_PREFIX = 'e'
    TIME_PREFIX     = 't'
    ALTITUDE_PREFIX = 'h'
    GREATER_THAN    = 'gt'
    LOWER_THAN      = 'lt'
    XY_PREFIX       = 'xy'

    # if multiple aggrs, they are stored as dataset dimensions: discard from filename
    eaggr  = eaggr  if (type(eaggr)  is str) else eaggr[0]  if isinstance(eaggr,  list) and len(eaggr)  == 1 else None
    taggr  = taggr  if (type(taggr)  is str) else taggr[0]  if isinstance(taggr,  list) and len(taggr)  == 1 else None
    xyaggr = xyaggr if (type(xyaggr) is str) else xyaggr[0] if isinstance(xyaggr, list) and len(xyaggr) == 1 else None

    # build the file name:

    ofilename = an_type.value + SEP + index + SEP + scenario

    if tint is not None:
        ofilename += (SEP + str(tint[0])) if tint[0] is not None else ''
        ofilename += (TS  + str(tint[1])) if tint[1] is not None else ''

    ofilename += (SEP + BASELINE_PREFIX + str(baseline[0])) if baseline is not None else ''
    ofilename +=                    (TS + str(baseline[1])) if baseline is not None else ''
    ofilename += (TS + baseline_op.value) if baseline_op is not None else ''

    if hfilter is not None:
        if hfilter[0] is None:
            ofilename += (SEP + ALTITUDE_PREFIX + TS + LOWER_THAN   + str(hfilter[1]))
        elif hfilter[1] is None:
            ofilename += (SEP + ALTITUDE_PREFIX + TS + GREATER_THAN + str(hfilter[0]))
        else:
            ofilename += (SEP + ALTITUDE_PREFIX + str(hfilter[0]) + TS + str(hfilter[1]))

    ofilename += (SEP + ENSEMBLE_PREFIX + eaggr)  if eaggr  is not None else ''
    ofilename += (SEP + TIME_PREFIX     + taggr)  if taggr  is not None else ''
    ofilename += (SEP + XY_PREFIX       + xyaggr) if xyaggr is not None else ''

    ofilename += ('.' + ofmt.value) if ofmt is not None else ''

    return ofilename


# ------------------------------------------------------------------------------
# format analysis output file names
##... def fetch_files(an_type:AnalysisType, index:str, scenario:str,

