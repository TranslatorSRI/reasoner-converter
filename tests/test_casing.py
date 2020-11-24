"""Test casing."""
import pytest

from reasoner_converter.util import pascal_case, snake_case

def test_snake():
    """Test conversion to snake_case."""
    snake_case("ChemicalSubstance") == "chemical_substance"
    snake_case([
        "ChemicalSubstance",
        "Biological Process"
    ]) == [
        "chemical_substance",
        "biological_process",
    ]
    with pytest.raises(ValueError):
        snake_case({"a": "ChemicalSubstance"})


def test_pascal():
    """Test conversion to PascalCase."""
    pascal_case("chemical_substance") == "ChemicalSubstance"
    pascal_case([
        "chemical_substance",
        "biological process",
    ]) == [
        "ChemicalSubstance",
        "BiologicalProcess"
    ]
    with pytest.raises(ValueError):
        pascal_case({"a": "ChemicalSubstance"})
