
from typing import Any
import os
import pytest

from eci import CovviInterface, FourOctetAddress


def tobool(value: Any) -> bool:
    if isinstance(value, str):
        return value.lower() == 'true'
    return bool(int(value))


ECI_HOST       = str(FourOctetAddress(os.environ.get('ECI_HOST', '192.168.1.5')))
POWER_ON_HAND  = tobool(os.environ.get('POWER_ON_HAND', True))
POWER_OFF_HAND = tobool(os.environ.get('POWER_OFF_HAND', True))


@pytest.fixture(scope='module')
def eci():
    print('Starting module fixture')
    with CovviInterface(ECI_HOST) as _eci:
        if POWER_ON_HAND:
            _eci.setHandPowerOn()
        yield _eci
        if POWER_OFF_HAND:
            _eci.setHandPowerOff()
    print('Closing module fixture')


@pytest.fixture()
def realtime_eci(eci: CovviInterface):
    print('Clearing realtime config')
    eci.resetRealtimeCfg()
    yield eci
    eci.resetRealtimeCfg()
