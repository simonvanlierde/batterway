from pathlib import Path

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
