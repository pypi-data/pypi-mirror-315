
import pytest
from typing import List, Dict, Any
from time   import sleep

from tests.interfaces import CovviInterface
from tests.messages   import DigitPosnMsg
from tests.enums      import Digit
from tests.primitives import Percentage
from tests.fixtures   import eci


MIN_DIGIT_POSITION:  int =  44
MAX_DIGIT_POSITION:  int = 210
MIN_LITTLE_POSITION: int =  44
MAX_LITTLE_POSITION: int = 200
MIN_THUMB_ROTATION:  int =  72
MAX_THUMB_ROTATION:  int = 230

N_TEST_POSITIONS: int = 10
ERROR_MARGIN:     int =  7

MAX, LIMIT = Percentage(value=Percentage.MAX), Percentage(value=1)


def make_positions(start: int, stop: int, num: int) -> List[int]:
    assert num >= 2
    sign = 1 if (stop - start) >= 0 else -1
    start, stop = min(start, stop), max(start, stop)
    return [
        int(round((i / (num - 1)) * (stop - start) + start))
        for i in range(num)
    ][::sign]


def open_all_positions(eci: CovviInterface) -> None:
    for digit in [Digit.THUMB, Digit.INDEX, Digit.MIDDLE, Digit.RING]:
        eci.setDigitMove(digit=Digit(value=digit), position=MIN_DIGIT_POSITION, speed=MAX, power=MAX, limit=LIMIT)
    eci.setDigitMove(digit=Digit(value=Digit.LITTLE), position=MIN_LITTLE_POSITION, speed=MAX, power=MAX, limit=LIMIT)
    eci.setDigitMove(digit=Digit(value=Digit.THUMB_ROTATION), position=MIN_THUMB_ROTATION, speed=MAX, power=MAX, limit=LIMIT)


@pytest.fixture(scope='module')
def position_eci(eci: CovviInterface):
    open_all_positions(eci)
    yield eci
    open_all_positions(eci)


def test_eci(position_eci: CovviInterface):
    assert position_eci


@pytest.mark.parametrize('set_func_name, kwargs', [
    [set_func_name, kwargs]
    for set_func_name, kwargs in [
        *[
            ['setDigitMove', dict(digit=Digit(value=digit), position=position, speed=MAX, power=MAX, limit=LIMIT)]
            for digit in [Digit.THUMB, Digit.INDEX, Digit.MIDDLE, Digit.RING]
            for position in make_positions(MIN_DIGIT_POSITION, MAX_DIGIT_POSITION, N_TEST_POSITIONS) + [MIN_DIGIT_POSITION]
        ],
        *[
            ['setDigitMove', dict(digit=Digit(value=digit), position=position, speed=MAX, power=MAX, limit=LIMIT)]
            for digit in [Digit.LITTLE]
            for position in make_positions(MIN_LITTLE_POSITION, MAX_LITTLE_POSITION, N_TEST_POSITIONS) + [MIN_LITTLE_POSITION]
        ],
        *[
            ['setDigitMove', dict(digit=Digit(value=digit), position=position, speed=MAX, power=MAX, limit=LIMIT)]
            for digit in [Digit.THUMB_ROTATION]
            for position in make_positions(MIN_THUMB_ROTATION, MAX_THUMB_ROTATION, N_TEST_POSITIONS) + [MIN_THUMB_ROTATION]
        ],
    ]
])
def test_set_and_stop(set_func_name: str, kwargs: Dict[str, Any], position_eci: CovviInterface):
    set_func  = getattr(position_eci, set_func_name)
    set_func(**kwargs)
    sleep(1.5)
    if 'digit' in kwargs and 'position' in kwargs:
        digit, position = kwargs['digit'], kwargs['position']
        msg: DigitPosnMsg = position_eci.getDigitPosn(digit=digit)
        # assert abs(msg.pos - position) <= ERROR_MARGIN
