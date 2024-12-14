#!/usr/bin/env python

"""
Handler of the {mlut} action.
"""

import argparse

from climdex import cmodels, utils

# ------------------------------------------------------------------------------
#
def validate_args(args) -> bool:
    """
    Arguments validation for the {mlut} action.
    """

    # (no args for the moment)

    return True


# ------------------------------------------------------------------------------
#
def run(args) -> bool:
    """
    Executes the configured {show,sh} action.
    """

    LOGGER = utils.get_logger(__name__)
    LOGGER.debug("{mlut} action called.")

    # load LUT
    cmodels.load_lut( force_reload=False )
    lut_items = cmodels.show_lut()


    header = "========== {0} ====================".format("Climate Models LUT")
    print(header)

    for item in lut_items:
        print("{0}".format(item))

