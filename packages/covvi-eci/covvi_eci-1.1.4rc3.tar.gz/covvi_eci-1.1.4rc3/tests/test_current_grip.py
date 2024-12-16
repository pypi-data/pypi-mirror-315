
from time import sleep
import pytest
import os

from tests.enums import CurrentGripID, GripNameIndex
from tests.primitives import CurrentGrip, GripName, Percentage
from tests.interfaces import CovviInterface
from tests.util import current_grip_ids, current_user_grip_ids, current_grip_ids_map, builtin_grip_ids
from tests.fixtures import eci


CURRENT_GRIP_IDS = os.environ.get('CURRENT_GRIP_IDS', current_grip_ids)
CURRENT_GRIP_IDS = CURRENT_GRIP_IDS if not type(CURRENT_GRIP_IDS) is type('') else [
    current_grip_ids_map[current_grip.upper()]
    for current_grip in CURRENT_GRIP_IDS.split(' ')
]


def test_eci(eci: CovviInterface):
    assert eci


@pytest.mark.parametrize('grip_id', CURRENT_GRIP_IDS)
def test_CurrentGrip(grip_id: CurrentGripID, eci: CovviInterface):
    if grip_id in current_user_grip_ids:
        grip_name: GripName = eci.getGripName(GripNameIndex(value=grip_id.value - len(builtin_grip_ids) - 1))
        if str(grip_name.value) == '':
            return

    eci.setCurrentGrip(grip_id=grip_id)
    current_grip = eci.getCurrentGrip()
    assert type(current_grip) is CurrentGrip
    assert current_grip.value == grip_id
    sleep(2**-4)
    eci.setDirectControlClose(speed=Percentage(value=100))
    sleep(1.5)
    eci.setDirectControlStop()
    sleep(2**-4)
    eci.setDirectControlOpen(speed=Percentage(value=100))
    sleep(1.5)
    eci.setDirectControlStop()
