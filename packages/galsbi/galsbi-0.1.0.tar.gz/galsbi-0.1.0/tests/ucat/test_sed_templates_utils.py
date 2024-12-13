# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Thu Aug 01 2024


import os

import h5py
import numpy as np
from cosmic_toolbox import file_utils

from galsbi.ucat import sed_templates_util


def test_get_template_integrals():
    filter = "DECam_i"

    filters = {}
    with h5py.File(
        os.path.join(
            os.path.dirname(__file__), "./../../resources/filters_collection.h5"
        ),
        "r",
    ) as f:
        filters[filter] = {}
        filters[filter]["lam"] = np.array(f[filter]["lam"])
        filters[filter]["amp"] = np.array(f[filter]["amp"])

    filters[filter]["integ"] = np.trapz(filters[filter]["amp"], filters[filter]["lam"])

    sed_templates = {}
    sed_templates["n_templates"] = 3
    sed_templates["lam"] = filters[filter]["lam"]
    sed_templates["amp"] = np.random.rand(
        sed_templates["n_templates"], len(sed_templates["lam"])
    )
    integrals, excess_grid, z_grid = sed_templates_util.get_template_integrals(
        sed_templates, filters, filter_names=[filter], test=True
    )
    assert integrals[filter][0].shape[1] == len(excess_grid)
    assert integrals[filter][0].shape[0] == len(z_grid)

    sed_templates_util.store_sed_integrals("test.h5", integrals, excess_grid, z_grid)
    sed_templates_util.store_sed_integrals(
        "test_dir/test.h5", integrals, excess_grid, z_grid
    )
    os.remove("test.h5")
    file_utils.robust_remove("test_dir/")
