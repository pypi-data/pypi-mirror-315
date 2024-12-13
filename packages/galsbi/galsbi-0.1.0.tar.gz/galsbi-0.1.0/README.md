# The (Great) GalSBI

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/galsbi.svg)](https://pypi.python.org/pypi/galsbi/)
[![PyPI version](https://badge.fury.io/py/galsbi.svg)](https://badge.fury.io/py/galsbi)
[![pipeline](https://gitlab.com/cosmology-ethz/galsbi/badges/main/pipeline.svg)](https://gitlab.com/cosmology-ethz/galsbi/-/pipelines)
[![coverage](https://gitlab.com/cosmology-ethz/galsbi/badges/main/coverage.svg)](https://gitlab.com/cosmology-ethz/galsbi)
<a href="https://cosmo-docs.phys.ethz.ch/galsbi/htmlcov/index.html">
  <img src="https://img.shields.io/badge/coverage_report-green"
    alt="coverage report"/>
</a>

[![image](https://img.shields.io/badge/arXiv-2412.08701-B31B1B.svg?logo=arxiv&style=flat)](https://arxiv.org/abs/2412.08701)
[![image](https://img.shields.io/badge/arXiv-2412.08722-B31B1B.svg?logo=arxiv&style=flat)](https://arxiv.org/abs/2412.08722)
[![Docs](https://badgen.net/badge/icon/Documentation?icon=https://cdn.jsdelivr.net/npm/simple-icons@v13/icons/gitbook.svg&label)](https://cosmo-docs.phys.ethz.ch/galsbi/)
[![Source Code](https://badgen.net/badge/icon/Source%20Code?icon=github&label)](https://gitlab.com/cosmology-ethz/galsbi)

Create realistic galaxy catalogs and astronomical images based on the GalSBI model.
The GalSBI model is described in [Fischbacher et al. (2024)](https://arxiv.org/abs/2412.08701) and the
package is described in [Fischbacher et al. (2024)](https://arxiv.org/abs/2412.08722).

## Installation

The package can be installed via pip:

```bash
pip install galsbi
```

## Usage

To generate a catalog of galaxies with their intrinsic properties, you can use the following code snippet:

```python
from galsbi import GalSBI

model = GalSBI("Fischbacher+24")
model()
cats = model.load_catalogs()
```

More examples and detailed documentation can be found in the [documentation](https://cosmo-docs.phys.ethz.ch/galsbi/).

## Citation

If you use GalSBI in your work, please cite the science paper [Fischbacher et al. (2024)](https://arxiv.org/abs/2412.08701)
for using the GalSBI model and the code release paper [Fischbacher et al. (2024)](https://arxiv.org/abs/2412.08722) for using the package.
If you are using specific models or parametrizations, please also cite the corresponding papers.
If you are not sure which papers to cite, use the following with your model instance:

```python
model.cite()
```

## Credits

This package was developed by the Cosmology group at ETH Zurich and is currently maintained by
[Silvan Fischbacher](silvanf@phys.ethz.ch).

## Contributions

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.
