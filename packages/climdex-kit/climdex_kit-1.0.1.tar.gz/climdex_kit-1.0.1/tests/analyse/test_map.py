#!/usr/bin/env python

__package__ = 'tests.analyse'

"""
Tests for the generation of maps of climate indices.
"""

import unittest

import logging
import importlib_resources
from ddt import ddt, data

from .context import an
from .context import maps
from .context import enums
from .context import utils
from climdex.constants import *

# constants
NOTIMPL_SRC_TYPES = [ enums.SrcType.openeo, enums.SrcType.wcps ]
IMPL_SRC_TYPES    = [ enums.SrcType.local ]

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
    suite.addTest(TestMapNotImplemented())
    suite.addTest(TestMapDegenerateCases())
    suite.addTest(TestMapBadInput())
    # ...
    return suite

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.worker = an.AnalysisWorker()
        self.worker.setup()

@ddt
class TestMapNotImplemented(BaseTestCase):
    """
    Tests unimplemented map features are properly notified to the client.
    """
    @data( *NOTIMPL_SRC_TYPES )
    def test_not_implemented_src_type(self, srcType):
        with self.assertRaisesRegex(NotImplementedError, 'source type') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'amt', srcType, src=IDIR, scenario='rcp45', eaggr='med')

    def test_xyclip(self):
        with self.assertRaisesRegex(ValueError, 'clipping') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'amt', enums.SrcType.local, src=IDIR, scenario='rcp45',
                    eaggr='med', taggr='avg',
                    xyclip='POINT(30 10)')

    def test_not_implemented_multiple_tint(self):
        with self.assertRaisesRegex(NotImplementedError, 'time') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'amt', enums.SrcType.local, src=IDIR, scenario='rcp85',
                    tint=[['1990'],['2037','2053']], taggr='p05', eaggr='avg')

@ddt
class TestMapDegenerateCases(BaseTestCase):
    """
    Tests degenerate inputs for the `an.do_extract_information()` method.
    """
    @data( *IMPL_SRC_TYPES )
    def test_no_index(self, srcType):
        dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, None, srcType, src=IDIR, scenario='rcp45',
                      eaggr='med', taggr='avg', lenient=True)
        self.assertIsNone( dataset )

    @data( *IMPL_SRC_TYPES )
    def test_no_models_filter(self, srcType):
        dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'amt', srcType, src=IDIR, scenario='rcp45',
                      models=(14, 15, 16), eaggr='med', taggr='max',
                      lenient=True)
        self.assertIsNone( dataset )

    @data( *IMPL_SRC_TYPES )
    def test_empty_time_selection(self, srcType):
        dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'spi12', srcType, src=IDIR, scenario='rcp45',
                      tint=['1737','1853'], taggr='p05', eaggr='avg',
                      lenient=True)
        self.assertIsNone( dataset )

    @data( *IMPL_SRC_TYPES )
    def test_single_model(self, srcType):
        dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'amt', srcType, src=IDIR, scenario='rcp45', models=[13,], taggr='avg')
        self.assertIsNotNone( dataset )

@ddt
class TestMapBadInput(BaseTestCase):
    """
    Tests wrong inputs for the `an.do_extract_information()` method.
    """
    @data( *IMPL_SRC_TYPES )
    def test_missing_input_dir(self, srcType):
        with self.assertRaisesRegex(ValueError, 'location') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'amt', srcType, src=None, scenario='rcp45', eaggr='med', taggr='avg')

    @data( *IMPL_SRC_TYPES )
    def test_missing_scenario(self, srcType):
        with self.assertRaisesRegex(ValueError, 'scenario') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'amt', srcType, src=IDIR, scenario=None, eaggr='med', taggr='avg')

    @data( *IMPL_SRC_TYPES )
    def test_invalid_scenario(self, srcType):
        with self.assertRaisesRegex(ValueError, 'Scenario') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'amt', srcType, src=IDIR, scenario='rcp99999', eaggr='med', taggr='avg')

    @data( *IMPL_SRC_TYPES )
    def test_no_models_filter(self, srcType):
        with self.assertRaisesRegex(ValueError, 'model') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'spi12', srcType, src=IDIR, scenario='rcp85',
                    models=(14, 16), eaggr='med', taggr='max',
                    lenient=False)

    @data( *IMPL_SRC_TYPES )
    def test_no_models_aggregation(self, srcType):
        with self.assertRaisesRegex(ValueError, 'ensemble aggregation') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'amt', srcType, src=IDIR, scenario='rcp45', taggr='avg')

    @data( *IMPL_SRC_TYPES )
    def test_both_bbox_and_wgs84_bbox(self, srcType):
        with self.assertRaisesRegex(ValueError, 'bbox') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'amt', srcType, src=IDIR, scenario='rcp45',
                    eaggr='med', taggr='avg',
                    bbox=[12500,13000,455000,465000],
                    wgs84_bbox=[12.0,13.0,45.5,46.5])

    @data( *IMPL_SRC_TYPES )
    def test_invalid_bbox(self, srcType):
        with self.assertRaisesRegex(ValueError, 'bbox') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'amt', srcType, src=IDIR, scenario='rcp45',
                    eaggr='med', taggr='avg',
                    bbox=[0,0,0,0,0,0,0,0,0])

    @data( *IMPL_SRC_TYPES )
    def test_invalid_wgs84_bbox(self, srcType):
        with self.assertRaisesRegex(ValueError, 'bbox') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'amt', srcType, src=IDIR, scenario='rcp45',
                    eaggr='med', taggr='avg',
                    wgs84_bbox='Asia')

    @data( *IMPL_SRC_TYPES )
    def test_missing_dem(self, srcType):
        with self.assertRaisesRegex(ValueError, 'DEM') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'spi12', srcType, src=IDIR, scenario='rcp45',
                    eaggr='med', taggr='avg',
                    hfilter=[None,2000])

    @data( *IMPL_SRC_TYPES )
    def test_invalid_idir(self, srcType):
        with self.assertRaisesRegex(ValueError, 'directory') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'spi12', srcType, src='Sehenswurdigkeiten/', scenario='rcp45',
                    eaggr='med', taggr='avg')

    @data( *IMPL_SRC_TYPES )
    def test_invalid_time_selection_order(self, srcType):
        with self.assertRaisesRegex(ValueError, 'time') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'amt', srcType, src=IDIR, scenario='rcp85', eaggr='med',
                    tint=['2000','1999'], taggr='avg')

    @data( *IMPL_SRC_TYPES )
    def test_invalid_time_selection(self, srcType):
        with self.assertRaisesRegex(ValueError, 'time') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'amt', srcType, src=IDIR, scenario='rcp85', eaggr='med',
                    tint=['1990','2000', '2010'], taggr='q1')

    @data( *IMPL_SRC_TYPES )
    def test_empty_time_selection(self, srcType):
        with self.assertRaisesRegex(ValueError, 'time') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'amt', srcType, src=IDIR, scenario='rcp85',
                    tint=['1900','1950'], taggr='p05', eaggr='avg',
                    lenient=False)

    @data( *IMPL_SRC_TYPES )
    def test_missing_baseline_operator(self, srcType):
        with self.assertRaisesRegex(ValueError, 'baseline comparison operator') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'spi12', srcType, src=IDIR, scenario='rcp45', eaggr='avg',
                    baseline=['1995','1998'],
                    tint=['2050','2080'], taggr='min')

    @data( *IMPL_SRC_TYPES )
    def test_invalid_baseline_operator(self, srcType):
        with self.assertRaisesRegex(ValueError, 'baseline comparison operator') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'spi12', srcType, src=IDIR, scenario='rcp45', eaggr='avg',
                    baseline=['1995','1998'],
                    baseline_op='square_root',
                    tint=['2050','2080'], taggr='min')

    @data( *IMPL_SRC_TYPES )
    def test_partial_baseline_selection(self, srcType):
        with self.assertRaisesRegex(ValueError, 'baseline') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'amt', srcType, src=IDIR, scenario='rcp85', eaggr='med',
                    baseline=['1965','1985'],
                    baseline_op='diff',
                    tint=['2050','2080'], taggr='min')

    @data( *IMPL_SRC_TYPES )
    def test_invalid_time_aggregation(self, srcType):
        with self.assertRaisesRegex(ValueError, 'aggregation') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'spi12', srcType, src=IDIR, scenario='rcp45', eaggr='avg',
                    tint=['2050','2080'], taggr='p00000009')

    @data( *IMPL_SRC_TYPES )
    def test_invalid_ensemble_aggregation(self, srcType):
        with self.assertRaisesRegex(ValueError, 'aggregation') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'spi12', srcType, src=IDIR, scenario='rcp45', taggr='p99',
                    eaggr='minmax')

    @data( *IMPL_SRC_TYPES )
    def test_significant_test_missing_baseline(self, srcType):
        with self.assertRaisesRegex(ValueError, 'baseline') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'spi12', srcType, src=IDIR, scenario='rcp45', taggr='p99',
                    eaggr='avg', sign_test=[TIME_DIM], sign_conf=95)

    @data( *IMPL_SRC_TYPES )
    def test_invalid_significant_test_dims(self, srcType):
        with self.assertRaisesRegex(ValueError, 'dimension') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'spi12', srcType, src=IDIR, scenario='rcp45', eaggr='q3',
                    baseline=['1980','2010'],
                    baseline_op='diff',
                    tint=['2050','2080'], taggr='min',
                    sign_test=['beyond_dimension'], sign_conf=99)

    @data( *IMPL_SRC_TYPES )
    def test_invalid_significant_test_confidence_interval(self, srcType):
        with self.assertRaisesRegex(ValueError, 'Confidence') as verr:
            dataset = self.worker.do_extract_information(enums.AnalysisType.map2d, 'spi12', srcType, src=IDIR, scenario='rcp45', eaggr='q3',
                    baseline=['1980','2010'],
                    baseline_op='diff',
                    tint=['2050','2080'], taggr='min',
                    sign_test=[TIME_DIM, MODELS_DIM], sign_conf=100)

# - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
