
import pytest
from enum import Enum

from tests.interfaces import CovviInterface
from tests.util import digits, digits5
from tests.fixtures import eci


def test_eci(eci: CovviInterface):
    assert eci


@pytest.mark.parametrize('single_func_name, all_func_name, enum_values', [
    [single_func_name, all_func_name, enum_values]
    for single_func_name, all_func_name, enum_values in [
        ['getDigitStatus',  'getDigitStatus_all',  digits],
        ['getDigitPosn',    'getDigitPosn_all',    digits],
        ['getMotorCurrent', 'getMotorCurrent_all', digits5],
    ]
])
def test_both(single_func_name: str, all_func_name: str, enum_values: Enum, eci: CovviInterface):
    single_func = getattr(eci, single_func_name)
    all_func    = getattr(eci, all_func_name)
    # assert tuple(
    #     arg
    #     for e in enum_values
    #     for arg in single_func(e).args
    # ) == all_func().args
