# Copyright (C) 2019 ETH Zurich, Institute for Particle Physics and Astrophysics

"""
Created on Aug 2021
author: Tomasz Kacprzak
"""

import os

import numpy as np
from cosmic_toolbox import arraytools as at
from cosmic_toolbox import logger
from ivy.plugin.base_plugin import BasePlugin

LOGGER = logger.get_logger(__file__)


def get_ucat_catalog_filename(catalog_name):
    return catalog_name.replace("ufig", "ucat")


def catalog_to_rec(catalog):
    # get dtype first
    dtype_list = []
    for col_name in catalog.columns:
        col = getattr(catalog, col_name)
        n_obj = len(col)
        if len(col.shape) == 1:
            dtype_list += [(col_name, col.dtype)]
        else:
            dtype_list += [(col_name, col.dtype, col.shape[1])]

    # create empty array
    rec = np.empty(n_obj, dtype=np.dtype(dtype_list))

    # copy columns to array
    for col_name in catalog.columns:
        col = getattr(catalog, col_name)
        if len(col.shape) == 1:
            rec[col_name] = col
        elif col.shape[1] == 1:
            rec[col_name] = col.ravel()
        else:
            rec[col_name] = col

    return rec


class Plugin(BasePlugin):
    def __call__(self):
        par = self.ctx.parameters
        # make output dirs if needed
        if not os.path.isdir(par.filepath_tile):
            os.makedirs(par.filepath_tile)

        # write catalogs
        if "galaxies" in self.ctx:
            filepath_out = os.path.join(
                par.filepath_tile,
                get_ucat_catalog_filename(par.galaxy_catalog_name),
            )

            cat = catalog_to_rec(self.ctx.galaxies)
            at.write_to_hdf(filepath_out, cat)

        if "stars" in self.ctx:
            filepath_out = os.path.join(
                par.filepath_tile, get_ucat_catalog_filename(par.star_catalog_name)
            )
            cat = catalog_to_rec(self.ctx.stars)
            at.write_to_hdf(filepath_out, cat)

    def __str__(self):
        return "write ucat catalog to file"
