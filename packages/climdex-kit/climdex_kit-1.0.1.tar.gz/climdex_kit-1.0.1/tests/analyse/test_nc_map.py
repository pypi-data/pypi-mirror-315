#!/usr/bin/env python

__package__ = 'tests.analyse'

"""
Tests for the generation of maps from NetCDF inputs.
"""

import unittest

import logging
import importlib_resources
from ddt import ddt, data

import numpy as np
import xarray as xr
import geopandas as gpd
from shapely.geometry import MultiPoint

from .context import cmodels
from .context import utils
from .context import maps_nc as maps
from .context import xarrays
from .context import enums
from .context import an_utils
from climdex.constants import *
from climdex.nc import *

# constants
TIME_MON_RES = { 'amt':12, 'spi12':1 } # TODO fetch automatically
TEST_INDICES = [ i for i in TIME_MON_RES.keys() ]
INPUT_XY_SHAPE = (2,2) # TODO fetch automatically from input
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
    suite.addTest(TestMapWithStatSignificanceFilter())
    #
    suite.addTest(TestMapDegenerateCases())
    suite.addTest(TestMapBadInput())
    # ...
    return suite

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

@ddt
class TestMapSingleTstep(unittest.TestCase):
    """
    Test the generation of a 2D map representing a single time-step
    (only emsemble aggregation involved).
    """

    @classmethod
    def setUpClass(cls):
        cls.tstep = { 'amt':'2050', 'spi12':'2050-12' } # they have different t-res
        cls.rcp   = 'rcp85'
        cls.datasets = { index:
            maps._extract_map(index, idir=IDIR,
                scenario=cls.rcp,
                tint=[cls.tstep[index], cls.tstep[index]],
                eaggr='med') for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg="Returned data is not an xarray Dataset")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == INPUT_XY_SHAPE,
                msg=f"Unexpected spatial grid of generated map: {dataset[index].shape}")

    @data( *TEST_INDICES )
    def test_values(self, index):
        tstep   = self.tstep[ index ]
        dataset = self.datasets[ index ]

        # load datasets and select 2050
        scenario_dir = IDIR / index / self.rcp
        ensemble_files = list(scenario_dir.glob( NETCDF_RGX ))
        ensemble_ds = xr.open_mfdataset(
                     ensemble_files, parallel=False, engine='netcdf4',
                     concat_dim=MODELS_DIM, combine='nested',
                     decode_times=True)

        # manually select the timestep
        ensemble_da = ensemble_ds[ index ].loc[{TIME_DIM:tstep}]
        self.assertTrue( len(ensemble_da[TIME_DIM]) == 1 )

        # compute median manually 
        oracle_values = ensemble_da.median(dim=MODELS_DIM, skipna=True).values
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Ensemble median of the test index does not match the expected values.")


@ddt
class TestMapTaggr(unittest.TestCase):
    """
    Tests the generation of a 2D map representing an aggregation
    over a given time interval.
    """
    @classmethod
    def setUpClass(cls):
        cls.years = ['2071', '2076']
        cls.nyears= int(cls.years[1])-int(cls.years[0])+1
        cls.rcp   = 'rcp45'
        cls.datasets = { index:
            maps._extract_map(index, idir=IDIR,
                scenario=cls.rcp,
                tint=cls.years,
                eaggr='min',
                taggr='avg') for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg="Returned data is not an xarray Dataset")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == INPUT_XY_SHAPE,
                msg=f"Unexpected spatial grid of generated map: {dataset[index].shape}")

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

        # manually select the timestep
        ensemble_da = ensemble_ds[ index ].loc[{TIME_DIM:slice(*self.years)}]
        self.assertTrue( len(ensemble_da[TIME_DIM]) == ((self.nyears/tres)*12))

        # compute aggregation manually
        # TODO changing aggregation order changes the results: min/max not linear operators!!
        ensemble_da   = ensemble_da.mean(dim=TIME_DIM,  skipna=True)
        oracle_values = ensemble_da.min(dim=MODELS_DIM, skipna=True).values
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Time-averaged ensemble min. of the test index does not match the expected values.")

@ddt
class TestMapXYClipping(unittest.TestCase):
    """
    Tests the generation of a 2D map where an XY spatial clip is set.
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
            maps._extract_map(index, idir=IDIR,
                scenario=cls.rcp,
                tint=cls.years,
                eaggr='med', taggr='q1',
                xyclip=cls.pnts) for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg="Returned data is not an xarray Dataset")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == (1,2), # h-line
                msg=f"Unexpected spatial grid of generated map: {dataset[index].shape}")

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

        # spatial clipping
        _ = ensemble_ds.rio.write_crs( input_crs=INPUT_CRS, inplace=True )
        clipped_ds = ensemble_ds.rio.clip(geometries=self.pnts, drop=True)

        # manually select the timestep
        ensemble_da = clipped_ds[ index ].loc[{TIME_DIM:slice(*self.years)}]
        self.assertTrue( len(ensemble_da[TIME_DIM]) == ((self.nyears/tres)*12) )

        # compute aggregation manually
        ensemble_da   = ensemble_da.quantile(q=.25, interpolation=Q_INTERP_METHOD, dim=TIME_DIM,  skipna=True)
        oracle_values = ensemble_da.median(dim=MODELS_DIM, skipna=True).values
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Clipped ensemble map of the test index does not match the expected values.")

@ddt
class TestMapHFilter(unittest.TestCase):
    """
    Tests the generation of a 2D map where data are filtered based
    on altitude constraints.
    """
    @classmethod
    def setUpClass(cls):
        cls.years = ['1980', '1985']
        cls.nyears= int(cls.years[1])-int(cls.years[0])+1
        cls.rcp   = 'rcp45'
        cls.hfilter = [1000, None] # > 1000 m pixels only
        cls.datasets = { index:
            maps._extract_map(index, idir=IDIR,
                scenario=cls.rcp,
                tint=cls.years,
                eaggr='avg', taggr='p99',
                hfilter=cls.hfilter,
                dem=DEM) for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg="Returned data is not an xarray Dataset")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == INPUT_XY_SHAPE,
                msg=f"Unexpected spatial grid of generated map: {dataset[index].shape}")

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

        # manually select the timestep
        ensemble_da = filtered_ds[ index ].loc[{TIME_DIM:slice(*self.years)}]
        self.assertTrue( len(ensemble_da[TIME_DIM]) == ((self.nyears/tres)*12) )

        # compute aggregation manually
        ensemble_da   = ensemble_da.quantile(q=.99, interpolation=Q_INTERP_METHOD, dim=TIME_DIM,  skipna=True)
        oracle_values = ensemble_da.mean(dim=MODELS_DIM, skipna=True).values
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="H-filtered ensemble map of the test index does not match the expected values.")


@ddt
class TestMapModelsSubselection(unittest.TestCase):
    """
    Tests the generation of a 2D map where a subselection of the
    ensemble models is involved.
    """
    @classmethod
    def setUpClass(cls):
        cls.models = [7, 19] # shared by both input indices to harmonize tests
        cls.rcp   = 'rcp45'
        cls.datasets = { index:
            maps._extract_map(index, idir=IDIR,
                scenario=cls.rcp,
                models=cls.models,
                eaggr='avg', taggr='med') for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg="Returned data is not an xarray Dataset")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == INPUT_XY_SHAPE,
                msg=f"Unexpected spatial grid of generated map: {dataset[index].shape}")

    @data( *TEST_INDICES )
    def test_values(self, index):
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

        # check models cardinality
        self.assertTrue( len(ensemble_ds[MODELS_DIM]) == len(self.models) )

        # compute aggregation manually
        ensemble_da   = ensemble_ds[index].median(dim=TIME_DIM, skipna=True)
        oracle_values = ensemble_da.mean(dim=MODELS_DIM, skipna=True).values
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Sub-ensemble map of the test index does not match the expected values.")

@ddt
class TestMapWithBaseline(unittest.TestCase):
    """
    Tests the generation of a 2D map where the values are relative
    to a baseline period.
    """
    @classmethod
    def setUpClass(cls):
        cls.years = ['2075', '2079']
        cls.bline = ['1975', '1979']
        cls.nyears= int(cls.years[1])-int(cls.years[0])+1
        cls.byears= int(cls.bline[1])-int(cls.bline[0])+1
        cls.rcp   = 'rcp85'
        cls.datasets = { index:
            maps._extract_map(index, idir=IDIR,
                scenario=cls.rcp,
                tint=cls.years,
                baseline=cls.bline,
                baseline_op=enums.OpType.ratio,
                eaggr='max',
                taggr='max') for index in TEST_INDICES }

    @data( *TEST_INDICES )
    def test_type_and_shape(self, index):
        dataset = self.datasets[ index ]

        self.assertTrue(
                isinstance(dataset, xr.core.dataset.Dataset),
                msg="Returned data is not an xarray Dataset")
        self.assertTrue(
                index in dataset,
                msg="Index variable not found in Dataset")
        self.assertTrue(
                dataset[ index ].shape == INPUT_XY_SHAPE,
                msg=f"Unexpected spatial grid of generated map: {dataset[index].shape}")

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

        # manually select the timestep for both data and baseline
        baseline_da = ensemble_ds[ index ].loc[{TIME_DIM:slice(*self.bline)}]
        ensemble_da = ensemble_ds[ index ].loc[{TIME_DIM:slice(*self.years)}]
        self.assertTrue( len(baseline_da[TIME_DIM]) == ((self.byears/tres)*12))
        self.assertTrue( len(ensemble_da[TIME_DIM]) == ((self.nyears/tres)*12))

        # time aggregation
        ensemble_da   = ensemble_da.max(dim=TIME_DIM,   skipna=True)
        baseline_da   = baseline_da.max(dim=TIME_DIM,   skipna=True)

        # baseline comparison
        ensemble_da.values = ensemble_da.values / baseline_da.values

        # compute aggregation manually
        ensemble_da   = ensemble_da.max(dim=MODELS_DIM, skipna=True)

        #oracle_values = ensemble_da.values / baseline_da.values
        oracle_values = ensemble_da.values
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Baseline-relative ensemble aggregation of the test index does not match the expected values.")


@ddt
class TestMapWithStatSignificanceFilter(unittest.TestCase):
    """
    Tests the generation of a map where the only the models in the ensemble
    that are significantly different from the baseline are filtered.
    """
    @classmethod
    def setUpClass(cls):
        cls.years = ['2006', '2010']
        cls.bline = ['1996', '2000']
        cls.nyears= int(cls.years[1])-int(cls.years[0])+1
        cls.byears= int(cls.bline[1])-int(cls.bline[0])+1
        cls.rcp   = 'rcp45'
        cls.sign_test = [ TIME_DIM ] # I want to drop weak areas, by model, from spatial averaging
        cls.sign_conf = 90
        cls.datasets = { index:
            maps._extract_map(index, idir=IDIR,
                scenario=cls.rcp,
                tint=cls.years,
                baseline=cls.bline,
                baseline_op=enums.OpType.diff,
                sign_test = cls.sign_test, 
                sign_conf = cls.sign_conf,
                eaggr='med', taggr='perc_pos') for index in TEST_INDICES }

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
                dataset[ index ].shape == INPUT_XY_SHAPE,
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
                        conf_level = self.sign_conf)
        # assign new values back to original dataset: back to original dataset:
        ensemble_da = robust_da

        # time aggregations
        das = [ ensemble_da, baseline_da ]
        for i,da in enumerate(das):
            N = len(ensemble_da.coords[TIME_DIM])
            nan_mask_da = da.notnull().any( dim=TIME_DIM ) # preserve all-nan sections
            das[i] = da.where(lambda x: x > 0).count(dim=TIME_DIM) * 100. / N
            das[i] = das[i].where(nan_mask_da)
        ensemble_da = das[0]
        baseline_da = das[1]

        # baseline comparison
        ensemble_da.values -= baseline_da.values

        # compute aggregations manually
        ensemble_da = ensemble_da.median(dim=MODELS_DIM, skipna=True)

        oracle_values = ensemble_da.values 
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Baseline-relative ensemble aggregation of the test index does not match the expected values.")


@ddt
class TestMapWithEnsembleDirectionFilter(unittest.TestCase):
    """
    Tests the generation of a map where the only the pixels with at least
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
        cls.min_pos = 60 # %
        cls.datasets = { index:
            maps._extract_map(index, idir=IDIR,
                scenario=cls.rcp,
                tint=cls.years,
                baseline=cls.bline,
                baseline_op=enums.OpType.diff,
                eaggr='avg', taggr='max',
                perc_pos=cls.min_pos) for index in TEST_INDICES }

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
                dataset[ index ].shape == INPUT_XY_SHAPE,
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

        # time aggregation
        ensemble_da = ensemble_da.max( dim=TIME_DIM, skipna=True)
        baseline_da = baseline_da.max( dim=TIME_DIM, skipna=True)

        # baseline comparison
        ensemble_da.values -= baseline_da.values

        # percentage positive mask:
        N = len(ensemble_da.coords[MODELS_DIM])
        nan_mask_da = ensemble_da.notnull().any( dim=MODELS_DIM )
        perc_da     = ensemble_da.where(lambda x: x > 0).count(dim=MODELS_DIM) * 100. / N
        perc_da     = perc_da.where(nan_mask_da) # restore nans

        # compute aggregations and filtering manually
        ensemble_da = ensemble_da.mean(dim=MODELS_DIM, skipna=True)
        ensemble_da = ensemble_da.where(perc_da >= self.min_pos)

        oracle_values = ensemble_da.values 
        output_values = dataset[ index ].values

        # test (approx) equality
        self.assertTrue(
                np.allclose(output_values, oracle_values, equal_nan=True),
                msg="Baseline-relative ensemble aggregation of the test index does not match the expected values.")


class TestMapDegenerateCases(unittest.TestCase):
    """
    Tests degenerate inputs for the `map_nc._extract_map()` method.
    """
    def test_no_index(self):
        dataset = maps._extract_map(None, idir=IDIR, scenario='rcp45')
        self.assertIsNone( dataset )

    def test_no_models_filter(self):
        dataset = maps._extract_map('amt', idir=IDIR, scenario='rcp45',
                models=(14, 15, 16),
                lenient=True)
        self.assertIsNone( dataset )

    def test_empty_time_selection(self):
        dataset = maps._extract_map('spi12', idir=IDIR, scenario='rcp45',
                tint=['1737','1853'], # beware Pandas timestamp limits
                lenient=True)
        self.assertIsNone( dataset )

    def test_single_model(self):
        dataset = maps._extract_map('amt', idir=IDIR, scenario='rcp45',
                models=[3], taggr='avg')
        self.assertIsNotNone( dataset ) # TODO check dims etc ?

class TestMapBadInput(unittest.TestCase):
    """
    Tests wrong inputs for the `map_nc._extract_map()` method.
    """

    def test_missing_input_dir(self):
        with self.assertRaisesRegex(ValueError, 'directory') as verr:
            dataset = maps._extract_map('amt', idir=None, scenario='rcp45')

    def test_missing_scenario(self):
        with self.assertRaisesRegex(ValueError, 'scenario') as verr:
            dataset = maps._extract_map('amt', idir=IDIR, scenario=None)

    def test_invalid_scenario(self):
        with self.assertRaisesRegex(ValueError, 'Scenario') as verr:
            dataset = maps._extract_map('amt', idir=IDIR, scenario='rcp99999')

    def test_no_models_filter(self):
        with self.assertRaisesRegex(ValueError, 'model') as verr:
            dataset = maps._extract_map('spi12', idir=IDIR, scenario='rcp85',
                    models=(14, 16),
                    lenient=False)

    def test_invalid_xyclip(self):
        with self.assertRaisesRegex(ValueError, 'spatial clipping') as verr:
            dataset = maps._extract_map('amt', idir=IDIR, scenario='rcp45',
                    xyclip=[12.0,13.0,45.5,46.5])

    def test_missing_dem(self):
        with self.assertRaisesRegex(ValueError, 'DEM') as verr:
            dataset = maps._extract_map('spi12', idir=IDIR, scenario='rcp45',
                    hfilter=[None,2000])

    def test_invalid_idir(self):
        with self.assertRaisesRegex(ValueError, 'directory') as verr:
            dataset = maps._extract_map('amt', idir='Sehenswurdigkeiten/', scenario='rcp85')

    def test_invalid_time_selection_order(self):
        with self.assertRaisesRegex(ValueError, 'time') as verr:
            dataset = maps._extract_map('amt', idir=IDIR, scenario='rcp85',
                    tint=['2000','1999'])

    def test_invalid_time_selection_a(self):
        with self.assertRaisesRegex(ValueError, 'time') as verr:
            dataset = maps._extract_map('amt', idir=IDIR, scenario='rcp85',
                    tint=['2000'])

    def test_invalid_time_selection_b(self):
        with self.assertRaisesRegex(ValueError, 'time') as verr:
            dataset = maps._extract_map('amt', idir=IDIR, scenario='rcp85',
                    tint=['1990','2000','2010'])

    def test_empty_time_selection(self):
        with self.assertRaisesRegex(ValueError, 'time') as verr:
            dataset = maps._extract_map('amt', idir=IDIR, scenario='rcp85',
                    tint=['1900','1950'],
                    lenient=False)

    def test_missing_baseline_operator(self):
        with self.assertRaisesRegex(ValueError, 'baseline comparison operator') as verr:
            dataset = maps._extract_map('spi12', idir=IDIR, scenario='rcp45',
                    baseline=['1995','1998'],
                    tint=['2050','2080'])

    def test_invalid_baseline_operator(self):
        with self.assertRaisesRegex(ValueError, 'baseline comparison operator') as verr:
            dataset = maps._extract_map('spi12', idir=IDIR, scenario='rcp45',
                    baseline=['1985','1998'],
                    baseline_op='square_root',
                    tint=['2050','2080'])

    def test_partial_baseline_selection(self):
        with self.assertRaisesRegex(ValueError, 'baseline') as verr:
            dataset = maps._extract_map('amt', idir=IDIR, scenario='rcp85',
                    baseline=['1965','1985'],
                    tint=['2050','2080'])

    def test_invalid_time_aggregation(self):
        with self.assertRaisesRegex(ValueError, 'aggregation') as verr:
            dataset = maps._extract_map('spi12', idir=IDIR, scenario='rcp45',
                    taggr='p00000009')

    def test_invalid_ensemble_aggregation(self):
        with self.assertRaisesRegex(ValueError, 'aggregation') as verr:
            dataset = maps._extract_map('amt', idir=IDIR, scenario='rcp85',
                    eaggr='minmax')

# - - - - - - - - - - - - - - - - - - - - - - - - 

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
