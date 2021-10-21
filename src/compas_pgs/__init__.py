"""
********************************************************************************
compas_pgs
********************************************************************************

.. currentmodule:: compas_pgs


.. toctree::
    :maxdepth: 1


"""

from __future__ import print_function

import os


__author__ = ["Juney Lee"]
__copyright__ = "Block Research Group"
__license__ = "MIT License"
__email__ = "juney.lee@arch.ethz.ch"
__version__ = "0.1.3"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]
