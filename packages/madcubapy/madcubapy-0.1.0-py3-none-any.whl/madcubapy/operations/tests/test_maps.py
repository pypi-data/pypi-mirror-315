from astropy.table import Table
import astropy.units as u
from astropy.utils.diff import report_diff_values
import numpy as np
import pytest
from madcubapy.io.madcubamap import MadcubaMap
from madcubapy.operations import stack_emission

@pytest.fixture
def example_madcuba_map():
    # Create and return a Map instance to be used in tests
    return MadcubaMap.read(
        "madcubapy/operations/tests/data/IRAS16293_SO_2-1_moment0_madcuba.fits"
    )

def test_stack_emission(example_madcuba_map):
    sum_map = stack_emission(example_madcuba_map, example_madcuba_map)
    assert np.array_equal(sum_map.data, example_madcuba_map.data*2, equal_nan=True)
    assert (sum_map.hist[-1]["Macro"] ==
        "//PYTHON: Stack emission. Files: 'IRAS16293_SO_2-1_moment0_madcuba.fits', 'IRAS16293_SO_2-1_moment0_madcuba.fits'"
    )