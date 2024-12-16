
from typing import Callable
from random import randint, choices
from string import ascii_letters
import pytest

from eci import CurrentGripID as ECI_CurrentGripID
from tests.enums import Digit, Digit5, GripNameIndex, BuiltinGripID, CurrentGripID, UserGripID


REALTIME_TEST_TIME = 4


digits = [
    Digit(value=digit)
    for digit in [Digit.THUMB, Digit.INDEX, Digit.MIDDLE, Digit.RING, Digit.LITTLE, Digit.THUMB_ROTATION]
]


digits5 = [
    Digit5(value=digit5)
    for digit5 in [Digit5.THUMB, Digit5.INDEX, Digit5.MIDDLE, Digit5.RING, Digit5.LITTLE]
]


grip_name_indexes = [
    GripNameIndex(value=grip_name_index)
    for grip_name_index in [GripNameIndex.GN0, GripNameIndex.GN1, GripNameIndex.GN2, GripNameIndex.GN3, GripNameIndex.GN4, GripNameIndex.GN5]
]


builtin_grip_ids = [
    BuiltinGripID(value=builtin_grip_id)
    for builtin_grip_id in [
        BuiltinGripID.TRIPOD, BuiltinGripID.POWER, BuiltinGripID.TRIGGER, BuiltinGripID.PREC_OPEN, BuiltinGripID.PREC_CLOSED, BuiltinGripID.KEY, BuiltinGripID.FINGER,
        BuiltinGripID.CYLINDER, BuiltinGripID.COLUMN, BuiltinGripID.RELAXED, BuiltinGripID.GLOVE, BuiltinGripID.TAP, BuiltinGripID.GRAB, BuiltinGripID.TRIPOD_OPEN,
    ]
]


current_grip_ids = [
    CurrentGripID(value=current_grip_id)
    for current_grip_id in [
        CurrentGripID.TRIPOD, CurrentGripID.POWER, CurrentGripID.TRIGGER, CurrentGripID.PREC_OPEN, CurrentGripID.PREC_CLOSED, CurrentGripID.KEY, CurrentGripID.FINGER,
        CurrentGripID.CYLINDER, CurrentGripID.COLUMN, CurrentGripID.RELAXED, CurrentGripID.GLOVE, CurrentGripID.TAP, CurrentGripID.GRAB, CurrentGripID.TRIPOD_OPEN,
        CurrentGripID.GN0, CurrentGripID.GN1, CurrentGripID.GN2, CurrentGripID.GN3, CurrentGripID.GN4, CurrentGripID.GN5,
    ]
]


current_grip_ids_map = {
    ECI_CurrentGripID(value=current_grip_id).name: CurrentGripID(value=current_grip_id)
    for current_grip_id in [
        CurrentGripID.TRIPOD, CurrentGripID.POWER, CurrentGripID.TRIGGER, CurrentGripID.PREC_OPEN, CurrentGripID.PREC_CLOSED, CurrentGripID.KEY, CurrentGripID.FINGER,
        CurrentGripID.CYLINDER, CurrentGripID.COLUMN, CurrentGripID.RELAXED, CurrentGripID.GLOVE, CurrentGripID.TAP, CurrentGripID.GRAB, CurrentGripID.TRIPOD_OPEN,
        CurrentGripID.GN0, CurrentGripID.GN1, CurrentGripID.GN2, CurrentGripID.GN3, CurrentGripID.GN4, CurrentGripID.GN5,
    ]
}


current_user_grip_ids = [
    CurrentGripID(value=current_grip_id)
    for current_grip_id in [CurrentGripID.GN0, CurrentGripID.GN1, CurrentGripID.GN2, CurrentGripID.GN3, CurrentGripID.GN4, CurrentGripID.GN5]
]


user_grip_ids = [
    UserGripID(value=user_grip_id)
    for user_grip_id in [
        UserGripID.FIST, UserGripID.HOOK, UserGripID.PRECISION_HALF, UserGripID.RIPPLE, UserGripID.STICK_IT, UserGripID.THUMBS_UP,
        UserGripID.TRIPOD_CLOSED, UserGripID.TRIPOD_OPEN, UserGripID.TWO_FINGERS, UserGripID.WAVE,
    ]
]


user_grip_names = 'FIST HOOK PRECISION_HALF RIPPLE STICK_IT THUMBS_UP TRIPOD_CLOSED TRIPOD_OPEN TWO_FINGERS WAVE'.strip().split()


random_value_dict = {
    str:  (lambda: ''.join(choices(ascii_letters, k=8))),
    # int:  (lambda: randint(0, 255)),
    int:  (lambda: randint(0, 1)),
    bool: (lambda: bool(randint(0, 1))),
}


def repeat_test(num: int = 1):
    return pytest.mark.parametrize('', [[]] * num)


def setget_action(setter: Callable, getter: Callable, *args):
    setter(*args)
    assert args == getter().args
