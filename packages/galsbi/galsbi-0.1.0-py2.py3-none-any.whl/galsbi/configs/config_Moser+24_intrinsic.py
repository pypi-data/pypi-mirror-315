# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Thu Aug 08 2024

import os

import numpy as np
import ufig.config.common
from cosmo_torrent import data_path
from ivy.loop import Loop
from ufig.workflow_util import FiltersStopCriteria

import galsbi.ucat.config.common


# Import all common settings from ucat and ufig as default
def _update_globals(module, globals_):
    globals_.update(
        {k: v for k, v in module.__dict__.items() if not k.startswith("__")}
    )


_update_globals(galsbi.ucat.config.common, globals())
_update_globals(ufig.config.common, globals())

# Default size of the image
sampling_mode = "healpix"
healpix_map = np.zeros(12 * 64**2)
healpix_map[0] = 1

# Define the filters
filters = ["g", "r", "i", "z", "y"]
filters_full_names = {
    "B": "SuprimeCam_B",
    "g": "HSC_g",
    "r": "HSC_r2",
    "i": "HSC_i2",
    "z": "HSC_z",
    "y": "HSC_y",
}
reference_band = "i"

# Define the plugins that should be used
plugins = [
    "ufig.plugins.multi_band_setup",
    "galsbi.ucat.plugins.sample_galaxies",
    Loop(
        [
            "ufig.plugins.single_band_setup_intrinsic_only",
            "ufig.plugins.write_catalog",
        ],
        stop=FiltersStopCriteria(),
    ),
    "ivy.plugin.show_stats",
]

# Luminosity function
lum_fct_z_res = 0.001
lum_fct_m_max = -4
lum_fct_z_max = 6

# Sampling methods ucat
nside_sampling = 4096

# Magnitude limits
stars_mag_max = 26
gals_mag_max = 28
stars_mag_min = 12
gals_mag_min = 14

# Filter throughputs
filters_file_name = os.path.join(
    data_path("HSC_tables"), "HSC_filters_collection_yfix.h5"
)

# Template spectra & integration tables
n_templates = 5
templates_file_name = os.path.join(
    data_path("template_BlantonRoweis07"), "template_spectra_BlantonRoweis07.h5"
)

# Extinction
extinction_map_file_name = os.path.join(
    data_path("lambda_sfd_ebv"), "lambda_sfd_ebv.fits"
)

# magnitude table
magnitude_calculation = "table"
templates_int_tables_file_name = os.path.join(
    data_path("HSC_tables"), "HSC_template_integrals_yfix.h5"
)

# Catalog precision
catalog_precision = np.float32

# Seed
seed = 1996


# Parameters that are specific to the Moser+24 model
# Mainly the different parametrizations of the galaxy population model.
# DO NOT CHANGE THESE VALUES IF YOU WANT TO USE THE GALAXY POPULATION MODEL OF MOSER+24
# CHANGING THESE VALUES WILL LEAD TO A DIFFERENT MEANING OF SOME OF THE PARAMETERS
lum_fct_parametrization = "logpower"
ellipticity_sampling_method = "beta_mode_red_blue"
sersic_sampling_method = "blue_red_betaprime"
logr50_sampling_method = "red_blue"
template_coeff_sampler = "dirichlet_alpha_mode"
template_coeff_weight_blue = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
template_coeff_weight_red = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
template_coeff_z1_blue = 3
template_coeff_z1_red = 3
