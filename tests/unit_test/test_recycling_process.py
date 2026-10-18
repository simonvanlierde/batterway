import pytest

import tests.unit_test.utils_common as UC
from batterway.datamodel.generic.process import RecyclingProcess, RecyclingRoute
from batterway.datamodel.generic.product import BoM, ProductInstance, Quantity


def test_recycling_process_relative_lci():
    input_products = BoM(
        {
            UC.water: ProductInstance(UC.water, Quantity(1.0, UC.kg)),
            UC.nmc111: ProductInstance(UC.nmc111, Quantity(1.0, UC.kg)),
        }
    )

    relative_input_influenced = {(UC.water, UC.heat): Quantity(1.0, UC.kg)}

    output_products = BoM({})
    relative_output_influences = {(UC.water, UC.vapor): Quantity(3.0, UC.kg)}
    r_p = RecyclingProcess(
        "recycling_test", input_products, output_products, relative_input_influenced, relative_output_influences
    )
    with pytest.raises(ValueError, match="Empty inputs"):
        r_p.update_fixed_input_lci({})




def test_chocolate_recycling_process():
    input_products = BoM(
        {
            UC.cookie: ProductInstance(UC.cookie, Quantity(1.0, UC.kg)),
            UC.schwarze_kuchen: ProductInstance(UC.schwarze_kuchen, Quantity(1.0, UC.kg)),
            UC.brownie: ProductInstance(UC.brownie, Quantity(1.0, UC.kg)),
        }
    )
    output_products = BoM({})
    relative_input_influenced = {
        (UC.chocolate, UC.heat): Quantity(1.0, UC.kg),
        (UC.black_wheat, UC.heat): Quantity(10.0, UC.kg),
    }
    relative_output_influences = {
        (UC.water, UC.vapor): Quantity(1.0, UC.kg),
        (UC.water, UC.vapor): Quantity(1.0, UC.kg),
    }
    r_p = RecyclingProcess(
        "recyclin_test", input_products, output_products, relative_input_influenced, relative_output_influences
    )



def test_missing_output_influencer_is_named(capsys):
    input_products = BoM({UC.water: ProductInstance(UC.water, Quantity(1.0, UC.kg))})
    with pytest.raises(ValueError, match="influencing the output"):
        RecyclingProcess(
            "recycling_test",
            input_products,
            BoM({}),
            {(UC.water, UC.heat): Quantity(1.0, UC.kg)},
            {(UC.steel, UC.vapor): Quantity(1.0, UC.kg)},
        )
    assert "steel" in capsys.readouterr().out


def test_recycling_route_iterates_process_flows():
    def water_step(name):
        water = BoM({UC.water: ProductInstance(UC.water, Quantity(1.0, UC.kg))})
        return RecyclingProcess(
            name, water, water, {(UC.water, UC.heat): Quantity(1.0, UC.kg)}, {(UC.water, UC.vapor): Quantity(1.0, UC.kg)}
        )

    steps = [water_step("step_1"), water_step("step_2")]
    assert "water" in str(steps[0])
    RecyclingRoute("route", steps).ensure_consistency()
