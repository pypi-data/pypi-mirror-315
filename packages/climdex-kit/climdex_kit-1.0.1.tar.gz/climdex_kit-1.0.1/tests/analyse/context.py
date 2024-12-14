import os
import sys

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"src"
)
sys.path.append(SOURCE_PATH)
##print(f'PATH: {sys.path}')

from climdex import utils
from climdex import nc
from climdex import cmodels
from climdex import constants
from climdex.actions import analyse as an
from climdex.analyse import maps
from climdex.analyse import maps_nc
from climdex.analyse import trends
from climdex.analyse import trends_nc
from climdex.analyse import xarrays
from climdex.analyse import enums
from climdex.analyse import utils as an_utils
