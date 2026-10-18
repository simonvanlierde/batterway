from pathlib import Path

import pytest

from batterway.datamodel.generic.process import RecyclingRoute
from batterway.datamodel.generic.product import ChemicalCompound
from batterway.datamodel.parser.Inventory import Inventory


def test_parser() -> None:
    """Testing the inventory parser."""
    new_inventory = Inventory.create_from_file(Path(__file__).parent.parent.parent / "data/dataframes/")
    r_process = new_inventory.get_process("recycling_process_1")
    r_process.update_fixed_input_lci({"Battery_NMC442": 578.0})


def test_parser_builds_chemical_compounds() -> None:
    """Rows of chemical_compounds.csv become ChemicalCompound objects with their formula."""
    new_inventory = Inventory.create_from_file(Path(__file__).parent.parent.parent / "data/dataframes/")
    assert isinstance(new_inventory.products["Ca(OH)2"], ChemicalCompound)
    assert new_inventory.products["Ca(OH)2"].molar_mass > 0


def test_parse_possible_input() -> None:
    """fixedlci.csv lists, per fixed LCI, the products a process can take as input."""
    possible = Inventory.parse_possible_input(Path(__file__).parent.parent.parent / "data/dataframes/")
    assert set(possible) == {"lci-route-1", "lci-route-2", "lci-route-3"}
    assert possible["lci-route-1"] == [
        "Battery_NMC442", "Battery_NMC111", "Battery_NMC622", "Nickel", "Cobalt", "Manganese"
    ]


def test_parsed_process_outputs_follow_the_output_lci() -> None:
    """A parsed process lists as outputs the products its output relative LCI produces."""
    new_inventory = Inventory.create_from_file(Path(__file__).parent.parent.parent / "data/dataframes/")
    r_process = new_inventory.get_process("recycling_process_1")
    expected = {influenced for _, influenced in r_process.ref_input_to_output_relation}
    assert expected
    assert set(r_process.outputs.products) == expected


def test_alternative_routes_do_not_chain() -> None:
    """recycling_process_1 and _2 both take batteries in, so one does not feed the other."""
    new_inventory = Inventory.create_from_file(Path(__file__).parent.parent.parent / "data/dataframes/")
    steps = [new_inventory.get_process("recycling_process_1"), new_inventory.get_process("recycling_process_2")]
    with pytest.raises(ValueError, match="No product produced by"):
        RecyclingRoute("route", steps).ensure_consistency()
