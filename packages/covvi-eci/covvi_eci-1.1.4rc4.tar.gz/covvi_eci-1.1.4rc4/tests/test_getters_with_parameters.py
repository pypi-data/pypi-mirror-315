
import pytest

from tests.primitives import GripName
from tests.messages import ControlMsg, DigitConfigMsg, DigitErrorMsg, DigitPosnMsg, DigitStatusMsg, MotorCurrentMsg
from tests.interfaces import CovviInterface
from tests.util import digits, digits5, grip_name_indexes
from tests.fixtures import eci


def test_eci(eci: CovviInterface):
    assert eci


@pytest.mark.parametrize('func_name, i, return_type', [
    [func_name, i, return_type]
    for func_name, i, return_type in [
        *[['getDigitConfig',  j,  DigitConfigMsg] for j in            digits],
        *[['getDigitError',   j,   DigitErrorMsg] for j in            digits],
        *[['getDigitPosn',    j,    DigitPosnMsg] for j in            digits],
        *[['getDigitStatus',  j,  DigitStatusMsg] for j in            digits],
        *[['getGripName',     j,        GripName] for j in grip_name_indexes],
        *[['getMotorCurrent', j, MotorCurrentMsg] for j in           digits5],
    ]
])
def test_parameter_getters(func_name: str, i: int, return_type: type, eci: CovviInterface):
    func = getattr(eci, func_name)
    return_msg = func(i)
    assert issubclass(type(return_msg), return_type)
    if issubclass(type(return_msg), ControlMsg):
        return_msg: ControlMsg
        assert return_msg == type(return_msg).unpack(return_msg.pack())
