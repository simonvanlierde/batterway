# Usage

Clone the repository and install it with `uv sync`. The model reads the CSV files in
`data/dataframes/` and computes the flows of one recycling process for a given battery input:

```python
from pathlib import Path

from batterway.datamodel.parser.Inventory import Inventory

inventory = Inventory.create_from_file(Path("data/dataframes/"))
process = inventory.get_process("recycling_process_1")
process.update_fixed_input_lci({"Battery_NMC442": 578.0})
```

`update_fixed_input_lci` prints the computed in- and out-flows and stores them on the process
(`computed_input_bom` and `computed_output_bom`). `uv run python main.py` runs the same steps.

The mass balance of the bundled data does not close: see the README before using the numbers.
