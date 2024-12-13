# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Wed Jul 31 2024


import os

import h5py
import ivy
import numpy as np
from cosmic_toolbox import arraytools as at

from galsbi.ucat import galaxy_sampling_util
from galsbi.ucat.plugins import write_catalog, write_catalog_photo


def test_write_catalogs():
    ctx = ivy.context.create_ctx(
        parameters=ivy.load_configs("galsbi.ucat.config.common")
    )
    ctx.parameters.filepath_tile = "test/"
    columns = ["x", "y", "z"]
    ctx.galaxies = galaxy_sampling_util.Catalog()
    ctx.galaxies.columns = columns
    gal = {}
    ctx.stars = galaxy_sampling_util.Catalog()
    ctx.stars.columns = columns
    star = {}

    for c in columns:
        setattr(ctx.galaxies, c, np.zeros(5))
        gal[c] = np.zeros(5)
        setattr(ctx.stars, c, np.ones(5))
        star[c] = np.ones(5)
    gal = at.dict2rec(gal)
    star = at.dict2rec(star)
    write_catalog.Plugin(ctx)()

    par = ctx.parameters
    filepath_gal = os.path.join(
        par.filepath_tile,
        write_catalog.get_ucat_catalog_filename(par.galaxy_catalog_name),
    )
    gal_cat = at.load_hdf(filepath_gal)
    assert np.all(gal_cat == gal)
    filepath_star = os.path.join(
        par.filepath_tile,
        write_catalog.get_ucat_catalog_filename(par.star_catalog_name),
    )
    star_cat = at.load_hdf(filepath_star)
    assert np.all(star_cat == star)

    os.remove(filepath_gal)
    os.remove(filepath_star)


def test_write_catalog_photo():
    ctx = ivy.context.create_ctx(
        parameters=ivy.load_configs("galsbi.ucat.config.common")
    )
    ctx.parameters.filepath_tile = "test/"
    ctx.parameters.filters = ["g", "r"]
    columns = ["z", "z_noisy", "galaxy_type", "template_coeffs", "template_coeffs_abs"]
    ctx.galaxies = galaxy_sampling_util.Catalog()
    ctx.galaxies.columns = columns
    gal = {}
    for c in columns:
        setattr(ctx.galaxies, c, np.zeros(5))
        gal[c] = np.zeros(5)
    ctx.galaxies.int_magnitude_dict = {"g": np.zeros(5), "r": np.zeros(5)}
    ctx.galaxies.abs_magnitude_dict = {"g": np.zeros(5), "r": np.zeros(5)}
    ctx.galaxies.magnitude_dict = {"g": np.zeros(5), "r": np.zeros(5)}
    gal = at.dict2rec(gal)
    write_catalog_photo.Plugin(ctx)()

    par = ctx.parameters
    filepath = os.path.join(
        par.filepath_tile,
        write_catalog_photo.get_ucat_catalog_filename(),
    )
    with h5py.File(filepath, "r") as fh5:
        for col in columns:
            assert np.all(fh5[col][:] == gal[col])
        for b in par.filters:
            assert np.all(fh5[f"int_mag_{b}"][:] == np.zeros(5))
            assert np.all(fh5[f"abs_mag_{b}"][:] == np.zeros(5))
            assert np.all(fh5[f"mag_{b}"][:] == np.zeros(5))

    os.remove(filepath)
