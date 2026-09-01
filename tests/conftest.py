"""Fixtures for testing."""
import pytest

from custom_components.som_energia.price import prices


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield


@pytest.fixture(autouse=True)
def reset_price_table():
    """The parsed CSV is cached for the life of the process; keep tests independent."""
    prices._price_table = None
    yield
    prices._price_table = None
