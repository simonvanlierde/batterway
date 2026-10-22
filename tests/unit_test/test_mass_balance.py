"""Mass-balance checks for the recycling routes built from data/dataframes."""

from pathlib import Path

import pytest

from batterway.datamodel.parser.Inventory import Inventory

DATA = Path(__file__).parents[2] / "data" / "dataframes"
MASS_IN_KG = 578.0
TOLERANCE = 0.05
# Electricity is stored as "kg" in the data but is energy, so it is not part of the mass balance.
NOT_MASS = {"Electricity"}


def run_route(name):
    process = Inventory.create_from_file(DATA).get_process(name)
    process.update_fixed_input_lci({"Battery_NMC442": MASS_IN_KG})
    return process.computed_input_bom, process.computed_output_bom


@pytest.mark.xfail(
    strict=True,
    reason="known gap: the model does not conserve mass (578 kg in, 6.6 kg out on route 1, 3.2 kg on route 2)",
)
@pytest.mark.parametrize("route", ["recycling_process_1", "recycling_process_2"])
def test_mass_balance_closes(route):
    _, out_bom = run_route(route)
    mass_out = sum(
        i.qty.value
        for i in out_bom.product_quantities.values()
        if i.product.name not in NOT_MASS
    )
    assert mass_out == pytest.approx(MASS_IN_KG, rel=TOLERANCE)


@pytest.mark.xfail(
    strict=True,
    reason="known gap: regression ratios in lci_relative.csv give negative inputs on route 1 (hydrogen peroxide, kerosene)",
)
def test_no_negative_flows():
    negative = {
        i.product.name: i.qty.value
        for bom in run_route("recycling_process_1")
        for i in bom.product_quantities.values()
        if i.qty.value < 0
    }
    assert not negative
