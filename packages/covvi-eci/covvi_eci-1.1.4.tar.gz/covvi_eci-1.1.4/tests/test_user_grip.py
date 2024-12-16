
import pytest

from tests.enums import GripNameIndex, UserGripID
from tests.primitives import GripName
from tests.interfaces import CovviInterface
from tests.fixtures import eci
from tests.util import grip_name_indexes, user_grip_ids, user_grip_names


def test_eci(eci: CovviInterface):
    assert eci


@pytest.mark.parametrize('grip_name_index', grip_name_indexes)
def test_removeUserGrip(grip_name_index: GripNameIndex, eci: CovviInterface):
    assert eci.removeUserGrip(grip_name_index)
    grip_name: GripName = eci.getGripName(grip_name_index)
    assert str(grip_name.value) == ''


@pytest.mark.parametrize('grip_name_index, user_grip_id, user_grip_name', [
    (grip_name_index, user_grip_id, user_grip_name)
    for grip_name_index in grip_name_indexes
    for user_grip_id, user_grip_name in zip(user_grip_ids, user_grip_names)
])
def test_sendUserGrip(grip_name_index: GripNameIndex, user_grip_id: UserGripID, user_grip_name: str, eci: CovviInterface):
    assert eci.sendUserGrip(grip_name_index, user_grip_id)
    grip_name: GripName = eci.getGripName(grip_name_index)
    assert str(grip_name.value).lower() == user_grip_name.lower().replace('_', ' ')


def test_resetUserGrips(eci: CovviInterface):
    eci.resetUserGrips()
    for grip_name_index in grip_name_indexes:
        grip_name: GripName = eci.getGripName(grip_name_index)
        assert str(grip_name.value) != ''
