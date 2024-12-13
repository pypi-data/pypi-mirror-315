import pytest
from rich.table import Table
from myproject import Duck, create_duck_table

def test_duck_creation():
    """Test creating a valid Duck instance."""
    duck = Duck(name="Test Duck", color="white", age=3)
    assert duck.name == "Test Duck"
    assert duck.color == "white"
    assert duck.age == 3

def test_duck_default_color():
    """Test that Duck uses default color when not specified."""
    duck = Duck(name="Test Duck")
    assert duck.color == "white"
    assert duck.age is None

def test_duck_invalid_empty_name():
    """Test that Duck raises error with empty name."""
    with pytest.raises(ValueError):
        Duck(name="")

def test_create_duck_table():
    """Test creation of rich table with duck data."""
    ducks = [
        Duck(name="Donald", color="white", age=5),
        Duck(name="Daisy", color="white"),
    ]
    
    table = create_duck_table(ducks)
    
    assert isinstance(table, Table)
    assert table.title == "Duck Collection"
    assert len(table.columns) == 3  # Name, Color, Age columns
