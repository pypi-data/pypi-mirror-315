#!/usr/bin/env python

__package__ = 'tests.analyse'

"""
Tests for the generation of maps from NetCDF inputs.
"""

import unittest

import logging
import importlib_resources
from ddt import ddt, data

import pandas as pd
import numpy as np
import xarray as xr
import geopandas as gpd
from shapely.geometry import MultiPoint

from .context import cmodels
from .context import utils
from .context import trends_nc as trends
from .context import xarrays
from .context import enums
from .context import an_utils
from climdex.constants import *
from climdex.nc import *

# constants
RCP85_N_MODELS = { 'amt':4, 'spi12':5 } # valid non-empty ones in testdata/
TIME_MON_RES = { 'amt':12, 'spi12':1 } # TODO fetch automatically
TEST_INDICES = [ i for i in TIME_MON_RES.keys() ]
INPUT_CRS = 'epsg:3035'
Q_INTERP_METHOD = an_utils.DEFAULT_QUANTILE_INTERP
PROJ_RESAMPLING = an_utils.DEFAULT_RESAMPLING

def setUpModule():
    # enable DEBUG lines
    utils.setup_logging( level=logging.DEBUG, path=None, env_key=None )

    global IDIR
    global DEM

    IDIR = importlib_resources.files(__package__) / '..' / 'testdata' / 'INDICES'
    DEM  = IDIR / '..' / 'DEM_1km_LAEA.nc'

    assert IDIR.exists()
    assert DEM.exists()

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

def suite():
    suite = unittest.TestSuite()
    #
    suite.addTest(TestMapSingleTstep())
    suite.addTest(TestMapTaggr())
    suite.addTest(TestMapXYClipping())
    suite.addTest(TestMapHFilter())
    suite.addTest(TestMapModelsSubselection())
    suite.addTest(TestMapWithBaseline())
    #
    suite.addTest(TestMapDegenerateCases())
    suite.addTest(TestMapBadInput())
    # ...
    return suite

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

@ddt
class TestEnsembleTrend(unittest.TestCase):
    """
    Test the generation of a 1D (absolute) time-trend representing one aggregated
    value over the whole ensemble.
    """

    @classmethod
    def setUpClass(cls):
        cls.years = ['2081', '2086']
        cls.nyears= int(cls.years[1])-int(cls.years[0])+1
        cls.rcp   = 'rcp85'
        cls.datasets = { index:
            trends._extract_trend(index, idir=IDIR,
                scenario=cls.rcp,
                tint=cls.years,
                xyaggr='avg', eaggr='med') for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg="Returned data is not an xarray Dataset")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == ((self.nyears/tres)*12,),
                msg=f"Unexpected shape of generated trend: {dataset[index].shape}")

    @data( *TEST_INDICES )
    def test_values(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        # load datasets 
        scenario_dir = IDIR / index / self.rcp
        ensemble_files = list(scenario_dir.glob( NETCDF_RGX ))
        ensemble_ds = xr.open_mfdataset(
                     ensemble_files, parallel=False, engine='netcdf4',
                     concat_dim=MODELS_DIM, combine='nested',
                     decode_times=True)

        x_dim = ensemble_ds.rio.x_dim
        y_dim = ensemble_ds.rio.y_dim

        # manually select the timesteps
        ensemble_da = ensemble_ds[ index ].loc[{TIME_DIM:slice(*self.years)}]
        self.assertTrue( len(ensemble_da[TIME_DIM]) == ((self.nyears/tres)*12) )

        # compute spatial aggregation manually 
        ensemble_da = ensemble_da.mean(dim=[x_dim,y_dim], skipna=True)

        # compute ensemble median manually 
        oracle_values = ensemble_da.median(dim=MODELS_DIM, skipna=True).values
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Ensemble median of the test index does not match the expected values.")

@ddt
class TestMultipleEnsembleTrends(unittest.TestCase):
    """
    Test the generation of an array of 1D (absolute) time-trends representing
    multiple different aggregations of the ensemble for a given scenario.
    """

    @classmethod
    def setUpClass(cls):
        cls.years = ['2031', '2036']
        cls.nyears= int(cls.years[1])-int(cls.years[0])+1
        cls.rcp   = 'rcp85'
        cls.eaggr = ['min', 'max']
        cls.datasets = { index:
            trends._extract_trend(index, idir=IDIR,
                scenario=cls.rcp, tint=cls.years,
                xyaggr='avg', eaggr=cls.eaggr) for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg="Returned data is not an xarray Dataset")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == (len(self.eaggr), (self.nyears/tres)*12),
                msg=f"Unexpected shape of generated trend: {dataset[index].shape}")

    @data( *TEST_INDICES )
    def test_values(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        # load datasets 
        scenario_dir = IDIR / index / self.rcp
        ensemble_files = list(scenario_dir.glob( NETCDF_RGX ))
        ensemble_ds = xr.open_mfdataset(
                     ensemble_files, parallel=False, engine='netcdf4',
                     concat_dim=MODELS_DIM, combine='nested',
                     decode_times=True)

        x_dim = ensemble_ds.rio.x_dim
        y_dim = ensemble_ds.rio.y_dim

        # manually select the timesteps
        ensemble_da = ensemble_ds[ index ].loc[{TIME_DIM:slice(*self.years)}]
        self.assertTrue( len(ensemble_da[TIME_DIM]) == ((self.nyears/tres)*12) )

        # compute spatial aggregation manually 
        ensemble_da = ensemble_da.mean(dim=[x_dim,y_dim], skipna=True)

        # compute ensemble aggregations manually 
        ensemble_min_da = ensemble_da.min(dim=MODELS_DIM, skipna=True)
        ensemble_max_da = ensemble_da.max(dim=MODELS_DIM, skipna=True)

        # collect values
        oracle_values = np.vstack([ ensemble_min_da, ensemble_max_da ])
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Ensemble aggregations of the test index does not match the expected values.")


@ddt
class TestEnsembleTrendsMultipleTints(unittest.TestCase):
    """
    Tests the generation of a multiple ensemble trends representing an aggregation
    over multiple given time intervals.
    """

    @classmethod
    def setUpClass(cls):
        cls.years = [['2071', '2076'],['2091','2093']]
        cls.nyears= ((int(cls.years[0][1])-int(cls.years[0][0])+1) +
                     (int(cls.years[1][1])-int(cls.years[1][0])+1))
        cls.rcp   = 'rcp45'
        cls.eaggr = ['min', 'q1']
        cls.datasets = { index:
            trends._extract_trend(index, idir=IDIR,
                scenario=cls.rcp, tint=cls.years,
                xyaggr='max', taggr='avg', eaggr=cls.eaggr) for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg="Returned data is not an xarray Dataset")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == (len(self.eaggr), len(self.years)),
                msg=f"Unexpected shape of generated trend: {dataset[index].shape}")

    @data( *TEST_INDICES )
    def test_values(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        # load dataset
        scenario_dir = IDIR / index / self.rcp
        ensemble_files = list(scenario_dir.glob( NETCDF_RGX ))
        ensemble_ds = xr.open_mfdataset(
                     ensemble_files, parallel=False, engine='netcdf4',
                     concat_dim=MODELS_DIM, combine='nested',
                     decode_times=True)

        x_dim = ensemble_ds.rio.x_dim
        y_dim = ensemble_ds.rio.y_dim

        # compute spatial aggregation manually 
        ensemble_da = ensemble_ds[index].max(dim=[x_dim,y_dim], skipna=True)

        # manually select the timesteps
        ensemble_da_0 = ensemble_da.loc[{TIME_DIM:slice(*self.years[0])}]
        ensemble_da_1 = ensemble_da.loc[{TIME_DIM:slice(*self.years[1])}]
        ensemble_da = xr.concat([
                          ensemble_da_0.mean(dim=TIME_DIM, skipna=True),
                          ensemble_da_1.mean(dim=TIME_DIM, skipna=True)],
                      dim=pd.Index(np.arange(0,len(self.years)), name=TIME_DIM))
        self.assertTrue( len(ensemble_da[TIME_DIM]) == len(self.years) )

        # compute ensemble aggregations manually 
        ensemble_min_da = ensemble_da.min(dim=MODELS_DIM, skipna=True)
        ensemble_q1_da  = ensemble_da.chunk({MODELS_DIM:-1})\
                                     .quantile(q=.25, dim=MODELS_DIM, interpolation=Q_INTERP_METHOD, skipna=True)
        #del ensemble_q1_da.coords['quantile']

        # collect values
        oracle_values = np.vstack([ ensemble_min_da, ensemble_q1_da ])
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Ensemble aggregations of the test index does not match the expected values.")

@ddt
class TestMultipleSpatialAggregations(unittest.TestCase):
    """
    Test the generation of an array of 1D (absolute) time-trends representing
    multiple different aggregations within the area of interest for a given scenario.
    """

    @classmethod
    def setUpClass(cls):
        cls.years = ['2031', '2036']
        cls.nyears= int(cls.years[1])-int(cls.years[0])+1
        cls.rcp   = 'rcp45'
        cls.eaggr  = ['avg']
        cls.xyaggr = ['min', 'max']
        cls.datasets = { index:
            trends._extract_trend(index, idir=IDIR,
                scenario=cls.rcp, tint=cls.years,
                xyaggr=cls.xyaggr, eaggr=cls.eaggr) for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg="Returned data is not an xarray Dataset")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == (len(self.xyaggr), (self.nyears/tres)*12),
                msg=f"Unexpected shape of generated trend: {dataset[index].shape}")

    @data( *TEST_INDICES )
    def test_values(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        # load datasets 
        scenario_dir = IDIR / index / self.rcp
        ensemble_files = list(scenario_dir.glob( NETCDF_RGX ))
        ensemble_ds = xr.open_mfdataset(
                     ensemble_files, parallel=False, engine='netcdf4',
                     concat_dim=MODELS_DIM, combine='nested',
                     decode_times=True)

        x_dim = ensemble_ds.rio.x_dim
        y_dim = ensemble_ds.rio.y_dim

        # manually select the timesteps
        ensemble_da = ensemble_ds[ index ].loc[{TIME_DIM:slice(*self.years)}]
        self.assertTrue( len(ensemble_da[TIME_DIM]) == ((self.nyears/tres)*12) )

        # compute spatial aggregations manually 
        ensemble_min_da = ensemble_da.min(dim=[x_dim,y_dim], skipna=True)
        ensemble_max_da = ensemble_da.max(dim=[x_dim,y_dim], skipna=True)

        # compute ensemble aggregation manually 
        ensemble_min_da = ensemble_min_da.mean(dim=MODELS_DIM, skipna=True)
        ensemble_max_da = ensemble_max_da.mean(dim=MODELS_DIM, skipna=True)

        # collect values
        oracle_values = np.vstack([ ensemble_min_da, ensemble_max_da ])
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Ensemble aggregations of the test index does not match the expected values.")


@ddt
class TestModelsTrend(unittest.TestCase):
    """
    Tests the generation of an array of 1D (absolute) time-trends,
    one for each of the ensemble's models.
    """
    @classmethod
    def setUpClass(cls):
        cls.years = ['2001', '2006']
        cls.nyears= int(cls.years[1])-int(cls.years[0])+1
        cls.rcp   = 'rcp85' # [!]  shall be, see RCP85_N_MODELS
        cls.datasets = { index:
            trends._extract_trend(index, idir=IDIR,
                scenario=cls.rcp,
                tint=cls.years,
                xyaggr='max', eaggr=None) for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg="Returned data is not an xarray Dataset")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == (RCP85_N_MODELS[index], (self.nyears/tres)*12),
                msg=f"Unexpected shape of generated trend: {dataset[index].shape}")

    @data( *TEST_INDICES )
    def test_values(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        # load datasets and select time interval
        scenario_dir = IDIR / index / self.rcp
        ensemble_files = list(scenario_dir.glob( NETCDF_RGX ))
        ensemble_ds = xr.open_mfdataset(
                     ensemble_files, parallel=False, engine='netcdf4',
                     concat_dim=MODELS_DIM, combine='nested',
                     decode_times=True)

        x_dim = ensemble_ds.rio.x_dim
        y_dim = ensemble_ds.rio.y_dim

        # manually select the timesteps
        ensemble_da = ensemble_ds[ index ].loc[{TIME_DIM:slice(*self.years)}]
        self.assertTrue( len(ensemble_da[TIME_DIM]) == ((self.nyears/tres)*12))

        # compute spatial aggregation manually 
        ensemble_da = ensemble_da.max(dim=[x_dim,y_dim], skipna=True)

        # drop na layer
        ensemble_da = ensemble_da.dropna( dim=MODELS_DIM, how='all' )

        oracle_values = ensemble_da.values
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Ensemble models trends do not match the expected values.")

@ddt
class TestTrendXYClipping(unittest.TestCase):
    """
    Tests the generation of a trend where an XY spatial clip is set.
    """
    @classmethod
    def setUpClass(cls):
        cls.years = ['2099', '2100']
        cls.nyears= int(cls.years[1])-int(cls.years[0])+1
        cls.rcp   = 'rcp85'
        cls.pnts   = gpd.GeoSeries([
            MultiPoint([[4345000.0, 2670000.0],
                        [4500000.0, 2670000.0]])], crs='epsg:3035')
        cls.datasets = { index:
            trends._extract_trend(index, idir=IDIR,
                scenario=cls.rcp,
                tint=cls.years,
                eaggr='avg',
                xyaggr='min',
                xyclip=cls.pnts) for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg=f"Returned data is not an xarray Dataset: {type(dataset)}")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == ((self.nyears/tres)*12,),
                msg=f"Unexpected shape of generated trend: {dataset[index].shape}")

    @data( *TEST_INDICES )
    def test_values(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        # load datasets and select time interval
        scenario_dir = IDIR / index / self.rcp
        ensemble_files = list(scenario_dir.glob( NETCDF_RGX ))
        ensemble_ds = xr.open_mfdataset(
                     ensemble_files, parallel=False, engine='netcdf4',
                     concat_dim=MODELS_DIM, combine='nested',
                     decode_times=True)

        x_dim = ensemble_ds.rio.x_dim
        y_dim = ensemble_ds.rio.y_dim

        # spatial clipping
        _ = ensemble_ds.rio.write_crs( input_crs=INPUT_CRS, inplace=True )
        clipped_ds = ensemble_ds.rio.clip(geometries=self.pnts, drop=True)

        # manually select the timesteps
        clipped_da = clipped_ds[ index ].loc[{TIME_DIM:slice(*self.years)}]
        self.assertTrue( len(clipped_da[TIME_DIM]) == ((self.nyears/tres)*12) )

        # compute spatial aggregation manually 
        clipped_da = clipped_da.min(dim=[x_dim,y_dim], skipna=True)

        # drop na layer
        clipped_da = clipped_da.dropna( dim=MODELS_DIM, how='all' )

        # compute ensemble aggregation manually
        clipped_da = clipped_da.mean(dim=MODELS_DIM, skipna=True)

        oracle_values = clipped_da.values
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Clipped ensemble map of the test index does not match the expected values.")

@ddt
class TestTrendHFilter(unittest.TestCase):
    """
    Tests the generation of a trend where data are filtered based
    on altitude constraints.
    """
    @classmethod
    def setUpClass(cls):
        cls.years = ['1980', '1985']
        cls.nyears= int(cls.years[1])-int(cls.years[0])+1
        cls.rcp   = 'rcp45'
        cls.hfilter = [1000, None] # > 1000 m pixels only
        cls.datasets = { index:
            trends._extract_trend(index, idir=IDIR,
                scenario=cls.rcp,
                tint=cls.years,
                xyaggr='p99', eaggr='avg',
                hfilter=cls.hfilter,
                dem=DEM) for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg="Returned data is not an xarray Dataset")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == ((self.nyears/tres)*12,),
                msg=f"Unexpected shape of generated trend: {dataset[index].shape}")

    @data( *TEST_INDICES )
    def test_values(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        # load datasets and select time interval
        scenario_dir = IDIR / index / self.rcp
        ensemble_files = list(scenario_dir.glob( NETCDF_RGX ))
        ensemble_ds = xr.open_mfdataset(
                     ensemble_files, parallel=False, engine='netcdf4',
                     concat_dim=MODELS_DIM, combine='nested',
                     decode_times=True)

        x_dim = ensemble_ds.rio.x_dim
        y_dim = ensemble_ds.rio.y_dim

        # dem
        dem_ds  = xr.open_dataset( DEM )
        dem_var = list(dem_ds)[0] # 'dem'

        # crs
        _ = ensemble_ds.rio.write_crs( input_crs=INPUT_CRS, inplace=True )
        _ =      dem_ds.rio.write_crs( input_crs=INPUT_CRS, inplace=True )

        # dem reproject
        dem_ds = dem_ds.rename({
                 dem_ds.rio.x_dim: ensemble_ds.rio.x_dim,
                 dem_ds.rio.y_dim: ensemble_ds.rio.y_dim  })
        dem_ds = dem_ds.rio.reproject_match( ensemble_ds, resampling=PROJ_RESAMPLING )

        # altitude filter
        filtered_ds = ensemble_ds.where(dem_ds[dem_var] >= self.hfilter[0])

        # manually select the timesteps
        filtered_da = filtered_ds[ index ].loc[{TIME_DIM:slice(*self.years)}]
        self.assertTrue( len(filtered_da[TIME_DIM]) == ((self.nyears/tres)*12) )

        # compute spatial aggregation manually 
        filtered_da = filtered_da.quantile(q=.99, dim=[x_dim,y_dim], interpolation=Q_INTERP_METHOD, skipna=True)

        # drop na layer
        filtered_da = filtered_da.dropna( dim=MODELS_DIM, how='all' )

        # compute ensemble aggregation manually
        filtered_da = filtered_da.mean(dim=MODELS_DIM, skipna=True)

        oracle_values = filtered_da.values
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="H-filtered ensemble map of the test index does not match the expected values.")


@ddt
class TestTrendModelsSubselection(unittest.TestCase):
    """
    Tests the generation of a trend where a subselection of the
    ensemble models is involved.
    """
    @classmethod
    def setUpClass(cls):
        cls.models = [19,] # shared by both input indices to harmonize tests
        cls.years = ['1980', '1985']
        cls.nyears= int(cls.years[1])-int(cls.years[0])+1
        cls.rcp   = 'rcp45'
        cls.datasets = { index:
            trends._extract_trend(index, idir=IDIR,
                scenario=cls.rcp,
                tint=cls.years,
                models=cls.models,
                xyaggr='avg', eaggr='avg') for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg="Returned data is not an xarray Dataset")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == ((self.nyears/tres)*12,),
                msg=f"Unexpected shape of generated trend: {dataset[index].shape}")

    @data( *TEST_INDICES )
    def test_values(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        # models selection files regex
        models_str = [ cmodels.get_model(x) for x in self.models ]
        models_rgx = [ f"*{m}{NETCDF_RGX}"  for m in models_str ]

        # load datasets
        scenario_dir = IDIR / index / self.rcp
        ensemble_files = utils.glob_or(scenario_dir, models_rgx)
        ensemble_ds = xr.open_mfdataset(
                     ensemble_files, parallel=False, engine='netcdf4',
                     concat_dim=MODELS_DIM, combine='nested',
                     decode_times=True)

        x_dim = ensemble_ds.rio.x_dim
        y_dim = ensemble_ds.rio.y_dim

        # check models cardinality
        self.assertTrue( len(ensemble_ds[MODELS_DIM]) == len(self.models) )

        # manually select the timesteps
        ensemble_da = ensemble_ds[ index ].loc[{TIME_DIM:slice(*self.years)}]
        self.assertTrue( len(ensemble_da[TIME_DIM]) == ((self.nyears/tres)*12) )

        # compute spatial aggregation manually 
        ensemble_da = ensemble_da.mean(dim=[x_dim,y_dim], skipna=True)

        # drop na layer
        ensemble_da = ensemble_da.dropna( dim=MODELS_DIM, how='all' )

        # compute aggregation manually
        ensemble_da   = ensemble_da.mean(dim=MODELS_DIM, skipna=True)

        oracle_values = ensemble_da.values
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Sub-ensemble map of the test index does not match the expected values.")

@ddt
class TestTrendWithBaseline(unittest.TestCase):
    """
    Tests the generation of a trend where the values are relative
    to a baseline period.
    """
    @classmethod
    def setUpClass(cls):
        cls.years = ['2075', '2079']
        cls.bline = ['1975', '1999']
        cls.nyears= int(cls.years[1])-int(cls.years[0])+1
        cls.byears= int(cls.bline[1])-int(cls.bline[0])+1
        cls.rcp   = 'rcp85'
        cls.datasets = { index:
            trends._extract_trend(index, idir=IDIR,
                scenario=cls.rcp,
                tint=cls.years,
                baseline=cls.bline,
                baseline_op=enums.OpType.ratio, taggr='max',
                xyaggr='max', eaggr='max') for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg="Returned data is not an xarray Dataset")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == ((self.nyears/tres)*12,),
                msg=f"Unexpected shape of generated trend: {dataset[index].shape}")

    @data( *TEST_INDICES )
    def test_values(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        # load datasets and select time interval
        scenario_dir = IDIR / index / self.rcp
        ensemble_files = list(scenario_dir.glob( NETCDF_RGX ))
        ensemble_ds = xr.open_mfdataset(
                     ensemble_files, parallel=False, engine='netcdf4',
                     concat_dim=MODELS_DIM, combine='nested',
                     decode_times=True)

        x_dim = ensemble_ds.rio.x_dim
        y_dim = ensemble_ds.rio.y_dim

        # drop na layer
        ensemble_ds = ensemble_ds.dropna( dim=MODELS_DIM, how='all', subset=[index] )

        # compute spatial aggregation manually 
        ensemble_ds[index] = ensemble_ds[index].max(dim=[x_dim,y_dim], skipna=True)

        # manually select the timesteps for both data and baseline
        ensemble_da = ensemble_ds[index].loc[{TIME_DIM:slice(*self.years)}]
        baseline_da = ensemble_ds[index].loc[{TIME_DIM:slice(*self.bline)}]
        self.assertTrue( len(baseline_da[TIME_DIM]) == ((self.byears/tres)*12))
        self.assertTrue( len(ensemble_da[TIME_DIM]) == ((self.nyears/tres)*12))

        # baseline comparison
        baseline_da = baseline_da.max(dim=TIME_DIM, skipna=True)
        ensemble_da = ensemble_da / baseline_da

        # compute ensemble aggregation manually
        ensemble_da   = ensemble_da.max(dim=MODELS_DIM, skipna=True)

        oracle_values = ensemble_da.values 
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Baseline-relative ensemble aggregation of the test index does not match the expected values.")


@ddt
class TestTrendWithStatSignificanceFilter(unittest.TestCase):
    """
    Tests the generation of a trend where the only the pixels
    that are significantly different from the baseline are considered
    in the aggregations (across model).
    """
    @classmethod
    def setUpClass(cls):
        cls.years = ['2005', '2009']
        cls.bline = ['2000', '2004']
        cls.nyears= int(cls.years[1])-int(cls.years[0])+1
        cls.byears= int(cls.bline[1])-int(cls.bline[0])+1
        cls.rcp   = 'rcp85'
        cls.sign_test = [TIME_DIM, MODELS_DIM] # I want to drop weak areas from spatial averaging
        cls.sign_conf = 50 # unusual confidence interval, to allow partial filtering
        cls.datasets = { index:
            trends._extract_trend(index, idir=IDIR,
                scenario=cls.rcp,
                tint=cls.years,
                baseline=cls.bline,
                baseline_op=enums.OpType.ratio, taggr='min',
                sign_test = cls.sign_test, 
                sign_conf = cls.sign_conf,
                xyaggr='max', eaggr='perc_neg') for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg="Returned data is not an xarray Dataset")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == ((self.nyears/tres)*12,),
                msg=f"Unexpected shape of generated trend: {dataset[index].shape}")

    @data( *TEST_INDICES )
    def test_values(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        # load datasets and select time interval
        scenario_dir = IDIR / index / self.rcp
        ensemble_files = list(scenario_dir.glob( NETCDF_RGX ))
        ensemble_ds = xr.open_mfdataset(
                     ensemble_files, parallel=False, engine='netcdf4',
                     concat_dim=MODELS_DIM, combine='nested',
                     decode_times=True)

        x_dim = ensemble_ds.rio.x_dim
        y_dim = ensemble_ds.rio.y_dim

        # drop na layer
        ensemble_ds = ensemble_ds.dropna( dim=MODELS_DIM, how='all', subset=[index] )

        # manually select the timesteps for both data and baseline
        ensemble_da = ensemble_ds[index].loc[{TIME_DIM:slice(*self.years)}]
        baseline_da = ensemble_ds[index].loc[{TIME_DIM:slice(*self.bline)}]
        self.assertTrue( len(baseline_da[TIME_DIM]) == ((self.byears/tres)*12) )
        self.assertTrue( len(ensemble_da[TIME_DIM]) == ((self.nyears/tres)*12) )

        # significance filter
        robust_da = xarrays.filter_significant(
                        ensemble_da,
                        baseline_da,
                        core_dim   = self.sign_test,
                        conf_level = self.sign_conf,
                        mode = 'approx')
        # assign new values back to original dataset: back to original dataset:
        ensemble_da = robust_da

        # compute spatial aggregation manually 
        ensemble_da = ensemble_da.max(dim=[x_dim,y_dim], skipna=True)
        baseline_da = baseline_da.max(dim=[x_dim,y_dim], skipna=True)

        # baseline comparison
        baseline_da = baseline_da.min(dim=TIME_DIM, skipna=True)
        ensemble_da = ensemble_da / baseline_da

        # compute ensemble aggregation manually
        N = len(ensemble_da.coords[MODELS_DIM])
        nan_mask_da = ensemble_da.notnull().any( dim=MODELS_DIM ) # preserve all-nan sections
        ensemble_da = ensemble_da.where(lambda x: x < 0).count(dim=MODELS_DIM) * 100. / N
        ensemble_da = ensemble_da.where(nan_mask_da)

        oracle_values = ensemble_da.values 
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Baseline-relative ensemble aggregation of the test index does not match the expected values.")


@ddt
class TestTrendWithEnsembleDirectionFilter(unittest.TestCase):
    """
    Tests the generation of a trend where the only the timesteps where at least
    a minium percentage of e.g. positive (>0) values within the ensemble
    are kept.
    """
    @classmethod
    def setUpClass(cls):
        cls.years = ['2006', '2010']
        cls.bline = ['1996', '2000']
        cls.nyears= int(cls.years[1])-int(cls.years[0])+1
        cls.byears= int(cls.bline[1])-int(cls.bline[0])+1
        cls.rcp   = 'rcp85'
        cls.min_neg = 50 # %
        cls.datasets = { index:
            trends._extract_trend(index, idir=IDIR,
                scenario=cls.rcp,
                tint=cls.years,
                baseline=cls.bline,
                baseline_op=enums.OpType.diff, taggr='max',
                xyaggr='min', eaggr='avg',
                perc_neg=cls.min_neg) for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg="Returned data is not an xarray Dataset")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == ((self.nyears/tres)*12,),
                msg=f"Unexpected shape of generated trend: {dataset[index].shape}")

    @data( *TEST_INDICES )
    def test_values(self, index):
        tres    = TIME_MON_RES[ index ]
        dataset = self.datasets[ index ]

        # load datasets and select time interval
        scenario_dir = IDIR / index / self.rcp
        ensemble_files = list(scenario_dir.glob( NETCDF_RGX ))
        ensemble_ds = xr.open_mfdataset(
                     ensemble_files, parallel=False, engine='netcdf4',
                     concat_dim=MODELS_DIM, combine='nested',
                     decode_times=True)

        x_dim = ensemble_ds.rio.x_dim
        y_dim = ensemble_ds.rio.y_dim

        # drop na layer
        ensemble_ds = ensemble_ds.dropna( dim=MODELS_DIM, how='all', subset=[index] )

        # manually select the timesteps for both data and baseline
        ensemble_da = ensemble_ds[index].loc[{TIME_DIM:slice(*self.years)}]
        baseline_da = ensemble_ds[index].loc[{TIME_DIM:slice(*self.bline)}]
        self.assertTrue( len(baseline_da[TIME_DIM]) == ((self.byears/tres)*12) )
        self.assertTrue( len(ensemble_da[TIME_DIM]) == ((self.nyears/tres)*12) )

        # compute spatial aggregation manually 
        ensemble_da = ensemble_da.min(dim=[x_dim,y_dim], skipna=True)
        baseline_da = baseline_da.min(dim=[x_dim,y_dim], skipna=True)

        # baseline comparison
        baseline_da = baseline_da.max(dim=TIME_DIM, skipna=True)
        ensemble_da = ensemble_da - baseline_da

        # percentage positive mask:
        N = len(ensemble_da.coords[MODELS_DIM])
        nan_mask_da = ensemble_da.notnull().any( dim=MODELS_DIM )
        perc_da     = ensemble_da.where(lambda x: x < 0).count(dim=MODELS_DIM) * 100. / N
        perc_da     = perc_da.where(nan_mask_da) # restore nans

        # compute aggregations and filtering manually
        ensemble_da = ensemble_da.mean(dim=MODELS_DIM, skipna=True)
        ensemble_da = ensemble_da.where(perc_da >= self.min_neg)

        oracle_values = ensemble_da.values 
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Baseline-relative ensemble aggregation of the test index does not match the expected values.")

class TestMapDegenerateCases(unittest.TestCase):
    """
    Tests degenerate inputs for the `trends_nc._)` method.
    """
    def test_no_index(self):
        dataset = trends._extract_trend(None, idir=IDIR, scenario='rcp45', xyaggr='max')
        self.assertIsNone( dataset )

    def test_no_models_filter(self):
        dataset = trends._extract_trend('amt', idir=IDIR, scenario='rcp45', xyaggr='min',
                models=(14, 15, 16),
                lenient=True)
        self.assertIsNone( dataset )

    def test_empty_time_selection(self):
        dataset = trends._extract_trend('spi12', idir=IDIR, scenario='rcp45', xyaggr='avg',
                tint=['1737','1853'], # beware Pandas timestamp limits
                lenient=True)
        self.assertIsNone( dataset )

    def test_single_model(self):
        dataset = trends._extract_trend('amt', idir=IDIR, scenario='rcp45', xyaggr='med',
                models=[3,], taggr='avg')
        self.assertIsNotNone( dataset ) # TODO check dims etc ?

class TestMapBadInput(unittest.TestCase):
    """
    Tests wrong inputs for the `map_nc._extract_map()` method.
    """

    def test_missing_input_dir(self):
        with self.assertRaisesRegex(ValueError, 'directory') as verr:
            dataset = trends._extract_trend('amt', idir=None, scenario='rcp45', xyaggr='avg')

    def test_missing_scenario(self):
        with self.assertRaisesRegex(ValueError, 'scenario') as verr:
            dataset = trends._extract_trend('amt', idir=IDIR, scenario=None, xyaggr='avg')

    def test_invalid_scenario(self):
        with self.assertRaisesRegex(ValueError, 'Scenario') as verr:
            dataset = trends._extract_trend('amt', idir=IDIR, scenario='rcp99999', xyaggr='avg')

    def test_no_models_filter(self):
        with self.assertRaisesRegex(ValueError, 'model') as verr:
            dataset = trends._extract_trend('spi12', idir=IDIR, scenario='rcp85',
                    models=(14, 16), xyaggr='avg',
                    lenient=False)

    def test_invalid_xyclip(self):
        with self.assertRaisesRegex(ValueError, 'spatial clipping') as verr:
            dataset = trends._extract_trend('amt', idir=IDIR, scenario='rcp45',
                    xyclip=[12.0,13.0,45.5,46.5], xyaggr='avg')

    def test_missing_dem(self):
        with self.assertRaisesRegex(ValueError, 'DEM') as verr:
            dataset = trends._extract_trend('spi12', idir=IDIR, scenario='rcp45',
                    hfilter=[None,2000], xyaggr='avg')

    def test_invalid_idir(self):
        with self.assertRaisesRegex(ValueError, 'directory') as verr:
            dataset = trends._extract_trend('amt', idir='Sehenswurdigkeiten/', scenario='rcp85', xyaggr='avg')

    def test_invalid_time_selection_order(self):
        with self.assertRaisesRegex(ValueError, 'time') as verr:
            dataset = trends._extract_trend('amt', idir=IDIR, scenario='rcp85', xyaggr='avg',
                    tint=['2000','1999'])

    def test_invalid_time_selection_a(self):
        with self.assertRaisesRegex(ValueError, 'time') as verr:
            dataset = trends._extract_trend('amt', idir=IDIR, scenario='rcp85', xyaggr='avg',
                    tint=['2000'])

    def test_invalid_time_selection_b(self):
        with self.assertRaisesRegex(ValueError, 'time') as verr:
            dataset = trends._extract_trend('amt', idir=IDIR, scenario='rcp85', xyaggr='avg',
                    tint=['1990','2000','2010'])

    def test_empty_time_selection(self):
        with self.assertRaisesRegex(ValueError, 'time') as verr:
            dataset = trends._extract_trend('amt', idir=IDIR, scenario='rcp85', xyaggr='avg',
                    tint=['1900','1950'],
                    lenient=False)

    def test_missing_baseline_operator(self):
        with self.assertRaisesRegex(ValueError, 'baseline comparison operator') as verr:
            dataset = trends._extract_trend('spi12', idir=IDIR, scenario='rcp45', xyaggr='avg',
                    baseline=['1995','1998'], taggr='avg',
                    tint=['2050','2080'])

    def test_invalid_baseline_operator(self):
        with self.assertRaisesRegex(ValueError, 'baseline comparison operator') as verr:
            dataset = trends._extract_trend('spi12', idir=IDIR, scenario='rcp45', xyaggr='avg',
                    baseline=['1985','1998'],
                    baseline_op='square_root', taggr='avg',
                    tint=['2050','2080'])

    def test_partial_baseline_selection(self):
        with self.assertRaisesRegex(ValueError, 'baseline') as verr:
            dataset = trends._extract_trend('amt', idir=IDIR, scenario='rcp85', xyaggr='avg',
                    baseline=['1965','1985'], taggr='avg',
                    tint=['2050','2080'])

    def test_invalid_time_aggregation(self):
        with self.assertRaisesRegex(ValueError, 'aggregation') as verr:
            dataset = trends._extract_trend('spi12', idir=IDIR, scenario='rcp45', xyaggr='avg',
                    tint=['2005','2018'],
                    baseline=['1985','1998'],
                    baseline_op='diff',
                    taggr='p00000009')

    def test_invalid_ensemble_aggregation(self):
        with self.assertRaisesRegex(ValueError, 'aggregation') as verr:
            dataset = trends._extract_trend('amt', idir=IDIR, scenario='rcp85', xyaggr='avg',
                    eaggr='minmax')

# - - - - - - - - - - - - - - - - - - - - - - - - 

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

