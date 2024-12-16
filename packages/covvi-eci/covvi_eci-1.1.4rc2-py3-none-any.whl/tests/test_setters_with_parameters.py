
import pytest
from typing import Tuple, Any
from time import sleep

from tests.messages   import ControlMsg
from tests.interfaces import CovviInterface
from tests.primitives import Percentage
from tests.util       import digits
from tests.fixtures   import eci


def test_eci(eci: CovviInterface):
    assert eci


@pytest.mark.parametrize('func_name, kwargs', [
    [func_name, kwargs]
    for func_name, kwargs in [
        *[
            ['setDigitMove', dict(digit=digit, position=40, speed=Percentage(value=100), power=Percentage(value=100), limit=Percentage(value=0))]
            for digit in digits
        ],
        ['setDigitPosn', dict(speed=Percentage(value=100), thumb=40, index=40, middle=40, ring=40, little=40, rotate=40)],
        ['setDirectControlClose', dict(speed=Percentage(value=0))],
        ['setDirectControlOpen', dict(speed=Percentage(value=0))],
        ['setRealtimeCfg', dict(
            digit_status    = False,
            digit_posn      = False,
            current_grip    = False,
            electrode_value = False,
            input_status    = False,
            motor_current   = False,
            digit_touch     = False,
            environmental   = False,
            orientation     = False,
            motor_limits    = False,
        )],
        ['setDigitPosnStop', dict()],
        ['setDirectControlStop', dict()],
    ]
])
def test_parameter_setters(func_name: str, kwargs: Tuple[Any, ...], eci: CovviInterface):
    func = getattr(eci, func_name)
    return_msg = func(**kwargs)
    sleep(1)
    if not type(return_msg) == tuple:
        return_msg = [return_msg]
    for msg in return_msg:
        if issubclass(type(msg), ControlMsg):
            msg: ControlMsg
            assert msg == type(msg).unpack(msg.pack())
