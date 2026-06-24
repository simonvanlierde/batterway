# batterway

[![Python Version](https://img.shields.io/badge/python-%3E%3D3.11-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue)](LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

**batterway** is a small Python package for modelling the life-cycle inventory (LCI) of
lithium-ion battery recycling. It loads battery bills-of-materials and recycling-route flow
ratios from CSV data, then computes the material in- and out-flows of a recycling process for a
given quantity of end-of-life battery. The current model covers NMC battery chemistries
(NMC111, NMC442, NMC622), their elemental composition, and the relative LCI flows of a recycling
route — propagating a fixed battery input through those ratios to the recovered materials and
process reagents. It is a focused mass-flow / inventory model, not a full impact-assessment or
characterisation engine.

It was built at the **2024 Départ de Sentier autumn school** on open life-cycle assessment.

## Why

batterway is an exercise in open, reproducible LCA on top of the
[Départ de Sentier](https://www.d-d-s.ch/) / [Sentier](https://vocab.sentier.dev/) ecosystem.
Units, products and flows carry [Sentier vocabulary](https://vocab.sentier.dev/) IRIs, and the
package builds on [`sentier_data_tools`](https://pypi.org/project/sentier-data-tools/) so that
battery and recycling data can be expressed against shared, openly governed vocabularies rather
than ad-hoc spreadsheets.

## Installation

The package is not published on PyPI; install it from source. It uses
[uv](https://docs.astral.sh/uv/) for environment and dependency management:

```bash
git clone https://github.com/simonvanlierde/batterway.git
cd batterway
uv sync
```

(Or, with a plain virtualenv: `pip install -e .`.)

## Usage

The runnable entry point is [`main.py`](main.py), which loads the bundled CSV inventory under
[`data/dataframes/`](data/dataframes/) and runs a recycling process:

```bash
uv run python main.py
```

The same flow in a few lines:

```python
from pathlib import Path
from batterway.datamodel.parser.Inventory import Inventory

# Load units, products, bills-of-materials and recycling-route LCI ratios from CSV
inventory = Inventory.create_from_file(Path("data/dataframes/"))

# Pick a recycling process defined in recycling_process.csv
process = inventory.get_process("recycling_process_1")

# Feed it 578 kg of end-of-life NMC442 battery; in-/out-flows are recomputed
process.update_fixed_input_lci({"Battery_NMC442": 578.0})

# Computed flows are printed and also stored on the process
process.computed_input_bom    # reagents / inputs required
process.computed_output_bom   # recovered materials / outputs
```

The model inputs live in [`data/dataframes/`](data/dataframes/) as CSV files: `units.csv`,
`products.csv`, `chemical_compounds.csv`, `BoM.csv` (battery bills-of-materials),
`lci_relative.csv` (per-route flow ratios), `fixedlci.csv` and `recycling_process.csv`.

## Repository layout

- [`batterway/`](batterway/) — the package. The core data model lives in
  [`datamodel/generic/product.py`](batterway/datamodel/generic/product.py) (`Unit`, `Quantity`,
  `Product`, `BoM`, `ChemicalCompound`) and
  [`datamodel/generic/process.py`](batterway/datamodel/generic/process.py) (`Process`,
  `RecyclingProcess`, `RecyclingRoute`); CSV loading and validation is in
  [`datamodel/parser/`](batterway/datamodel/parser/).
- [`data/dataframes/`](data/dataframes/) — the CSV inventory used by `main.py`.
- `data/archive/regression.ipynb` — **archived scratch work, not a tutorial.** This notebook was
  used once to derive the relative-LCI factors in `lci_relative.csv` from regression on external
  spreadsheet data; it does not import `batterway` and is not part of the analysis API. Start from
  `main.py` and the `batterway/` package, not this notebook.

## Authorship

This was a collaborative project at the 2024 Départ de Sentier autumn school. Simon van Lierde
created and maintains the repository and authored the core object-oriented data model and CSV
parser (`product.py`, `process.py`, `Inventory.py`, `parsers.py`). The recycling-route LCI data,
chemical-compound and material definitions, and additional parser/process work were contributed by
fellow participants (Leon Ferrari, Johanna Holsten, Samaneh Fayyaz, Kira Fischer). See the git
history for the full breakdown.

## License

Distributed under the terms of the [GPL-3.0 license](LICENSE); batterway is free and open source
software.

## Issues

If you encounter a problem, please [file an issue](https://github.com/simonvanlierde/batterway/issues)
with a description.
