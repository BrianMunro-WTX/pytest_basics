"""Shared pytest fixtures for the Car test suite.

Fixtures defined here are automatically available to every test file
in this directory — no import needed.
"""
import pytest

from car import Car


@pytest.fixture
def default_car():
    """A default Car (Ford Mustang, 2020, 25,000 miles)."""
    return Car()


@pytest.fixture
def tesla():
    """A Tesla Model 3 with low mileage."""
    return Car("Tesla", "Model 3", 2021, 5000)


@pytest.fixture(
    params=[
        Car("Ford", "F-150", 2019, 80000),
        Car("Toyota", "Corolla", 2020, 15000),
        Car("Honda", "Civic", 2018, 30000),
    ],
    ids=["Ford", "Toyota", "Honda"],
)
def standard_car(request):
    """Parametrized fixture: runs a test once per car make."""
    return request.param
