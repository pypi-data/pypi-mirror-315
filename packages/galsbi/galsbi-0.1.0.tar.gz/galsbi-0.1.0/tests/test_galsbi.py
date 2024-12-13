# Copyright (C) 2024 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher
# created: Thu Aug 08 2024


if True:
    # avoids reordering the imports, it is important that patching the
    # local cache folder happens before the galsbi import

    import os

    import cosmo_torrent.cosmo_torrent
    import numpy as np
    import pytest
    from cosmic_toolbox import arraytools as at

    def local_cache_folder(identifier):
        print("LOCAL FOLDER")
        here = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(here, "data", identifier)

    # we need to patch here before we import galsbi
    cosmo_torrent.cosmo_torrent.local_cache_folder = local_cache_folder

    import galsbi
    from galsbi import GalSBI
    from galsbi.citations import CITE_MOSER24


@pytest.fixture
def small_healpix_map():
    healpix_map = np.zeros(12 * 1024**2)
    healpix_map[0] = 1
    return healpix_map


@pytest.fixture
def cwd(tmp_path):
    previous_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        yield tmp_path
    finally:
        os.chdir(previous_cwd)


def test_intrinsic_model(small_healpix_map, cwd):
    model = GalSBI("Moser+24")
    assert model.name == "Moser+24"

    model(healpix_map=small_healpix_map)
    cats = model.load_catalogs()

    # test if all catalogs are written by checking if you can delete them
    for f in ["g", "r", "i", "z", "y"]:
        os.remove(f"GalSBI_sim_0_{f}_ucat.gal.cat")

    model = GalSBI("Moser+24")
    model(model_index=42, healpix_map=small_healpix_map)
    cats2 = model.load_catalogs(model_index=42)

    assert len(cats["ucat galaxies g"]["mag"]) != len(cats2["ucat galaxies g"]["mag"])

    for f in ["g", "r", "i", "z", "y"]:
        os.remove(f"GalSBI_sim_42_{f}_ucat.gal.cat")

    model = GalSBI("Moser+24")
    model(model_index=[0, 42], healpix_map=small_healpix_map)

    for f in ["g", "r", "i", "z", "y"]:
        os.remove(f"GalSBI_sim_0_{f}_ucat.gal.cat")
        os.remove(f"GalSBI_sim_42_{f}_ucat.gal.cat")


def test_emu_model(small_healpix_map, cwd):
    model = GalSBI("Moser+24")
    model(file_name="intrinsic", healpix_map=small_healpix_map)

    model = GalSBI("Moser+24")
    model(mode="emulator", file_name="emu", healpix_map=small_healpix_map)

    # test if intrinsic catalogs are the same
    for f in ["g", "r", "i", "z", "y"]:
        cat1 = at.load_hdf(f"intrinsic_0_{f}_ucat.gal.cat")
        cat2 = at.load_hdf(f"emu_0_{f}_ucat.gal.cat")
        shared_params = set(cat1.dtype.names) & set(cat2.dtype.names)
        assert len(shared_params) > 0
        for par in shared_params:
            assert np.all(cat1[par] == cat2[par])

        os.remove(f"intrinsic_0_{f}_ucat.gal.cat")
        os.remove(f"emu_0_{f}_ucat.gal.cat")
        os.remove(f"emu_0_{f}_ucat.star.cat")

    # test if there are output catalogs
    for f in ["g", "r", "i", "z", "y"]:
        cat = at.load_hdf(f"emu_0_{f}_se.cat")
        assert "MAG_AUTO" in cat.dtype.names
        os.remove(f"emu_0_{f}_se.cat")


def test_image(cwd):
    model = GalSBI("Moser+24")
    model(mode="image", size_x=100, size_y=100)

    # creates intrinsic catalogs and images
    for f in ["g", "r", "i", "z", "y"]:
        os.remove(f"GalSBI_sim_0_{f}_ucat.gal.cat")
        os.remove(f"GalSBI_sim_0_{f}_image.fits")


def test_custom_config(small_healpix_map, cwd):
    model = GalSBI("Moser+24")
    model(healpix_map=small_healpix_map)
    cats1 = {}
    for f in ["g", "r", "i", "z", "y"]:
        cats1[f] = at.load_hdf(f"GalSBI_sim_0_{f}_ucat.gal.cat")
        os.remove(f"GalSBI_sim_0_{f}_ucat.gal.cat")

    path2config = os.path.join(
        galsbi.__path__[0], "configs/config_Moser+24_intrinsic.py"
    )
    model = GalSBI("Moser+24")
    model(mode="config_file", config_file=path2config, healpix_map=small_healpix_map)
    cats2 = {}
    for f in ["g", "r", "i", "z", "y"]:
        cats2[f] = at.load_hdf(f"GalSBI_sim_0_{f}_ucat.gal.cat")
        os.remove(f"GalSBI_sim_0_{f}_ucat.gal.cat")

    config_module = "galsbi.configs.config_Moser+24_intrinsic"
    model = GalSBI("Moser+24")
    model(mode="config_file", config_file=config_module, healpix_map=small_healpix_map)
    cats3 = {}
    for f in ["g", "r", "i", "z", "y"]:
        cats3[f] = at.load_hdf(f"GalSBI_sim_0_{f}_ucat.gal.cat")
        os.remove(f"GalSBI_sim_0_{f}_ucat.gal.cat")

    for f in ["g", "r", "i", "z", "y"]:
        assert np.all(cats1[f] == cats2[f])
        assert np.all(cats1[f] == cats3[f])


def test_citations(capsys, cwd):
    model = GalSBI("Moser+24")
    model.cite()

    captured = capsys.readouterr()
    assert CITE_MOSER24 in captured.out


def test_invalid_model(cwd):
    with pytest.raises(ValueError):
        model = GalSBI("Moser+25")
        model()

    with pytest.raises(ValueError):
        galsbi.load.load_abc_posterior("Moser+25")

    with pytest.raises(ValueError):
        galsbi.citations.cite_abc_posterior("Moser+25")


def test_load_cats_and_images(cwd):
    model = GalSBI("Moser+24")
    model(mode="image", size_x=100, size_y=100)

    cats_rec = model.load_catalogs()
    cats_df = model.load_catalogs(output_format="df")
    cats_fits = model.load_catalogs(output_format="fits")
    assert np.all(
        list(cats_rec["ucat galaxies g"].dtype.names)
        == list(cats_fits["ucat galaxies g"].columns)
    )
    p = "mag"
    assert np.all(cats_rec["ucat galaxies g"][p] == cats_df["ucat galaxies g"][p])
    assert np.all(cats_rec["ucat galaxies g"][p] == cats_fits["ucat galaxies g"][p])

    with pytest.raises(ValueError):
        model.load_catalogs(output_format="invalid")

    images = model.load_images()
    assert (
        list(images.keys()).sort()
        == ["image g", "image r", "image i", "image z", "image y"].sort()
    )

    for f in model.filters:
        os.remove(f"GalSBI_sim_0_{f}_ucat.gal.cat")
        os.remove(f"GalSBI_sim_0_{f}_image.fits")

    images = model.load_images()
    assert images == {}

    cats = model.load_catalogs()
    assert cats == {}


def test_combine_cats(small_healpix_map, cwd):
    model = GalSBI("Moser+24")
    model(mode="emulator", healpix_map=small_healpix_map)

    cats = model.load_catalogs()
    cats_combined = model.load_catalogs(combine=True)

    assert np.all(
        cats["ucat galaxies g"]["mag"] == cats_combined["ucat galaxies"]["mag g"]
    )
    assert np.all(
        cats["sextractor g"]["MAG_AUTO"] == cats_combined["sextractor"]["MAG_AUTO g"]
    )

    for f in ["g", "r", "i", "z", "y"]:
        os.remove(f"GalSBI_sim_0_{f}_ucat.gal.cat")
        os.remove(f"GalSBI_sim_0_{f}_ucat.star.cat")
        os.remove(f"GalSBI_sim_0_{f}_se.cat")


def test_method_call_order(cwd):
    model = GalSBI("Moser+24")
    with pytest.raises(RuntimeError):
        model.load_catalogs()


@pytest.mark.slow
def test_fischbacher_model_with_emulator(cwd):
    model = GalSBI("Fischbacher+24")
    model(mode="emulator")
