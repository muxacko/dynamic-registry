import pytest

from registry import Registry


@pytest.fixture
def registry():
    return Registry()
