
import pytest
from typing import Callable, Tuple
from time import sleep

from eci.utils import leaf_classes
from tests.primitives import Command
from tests.enums import CommandString
from tests.interfaces import CovviInterface
from tests.messages import (
    ControlMsg, RealtimeMsg,
    DigitStatusAllMsg, DigitPosnAllMsg,    CurrentGripMsg,   ElectrodeValueMsg,
    InputStatusMsg,    MotorCurrentAllMsg, DigitTouchAllMsg, DigitErrorMsg,
    EnvironmentalMsg,  OrientationMsg,     MotorLimitsMsg
)
from tests.util import REALTIME_TEST_TIME
from tests.fixtures import realtime_eci, eci


def test_eci(eci: CovviInterface):
    assert eci

################################################################################################################################
# Real-time messages
################################################################################################################################

def test_setRealtimeCfg_no_packets(realtime_eci: CovviInterface):
    start_n_realtime_packets = realtime_eci.n_realtime_packets
    sleep(REALTIME_TEST_TIME)
    assert realtime_eci.n_realtime_packets == start_n_realtime_packets

def test_setRealtimeCfg_any_packets(realtime_eci: CovviInterface):
    start_n_realtime_packets = realtime_eci.n_realtime_packets
    realtime_eci.setRealtimeCfg(
        digit_status    = True,
        digit_posn      = True,
        current_grip    = True,
        electrode_value = True,
        input_status    = True,
        motor_current   = True,
        digit_touch     = True,
        digit_error     = True,
        environmental   = True,
        orientation     = True,
        motor_limits    = True,
    )
    sleep(REALTIME_TEST_TIME)
    end_n_realtime_packets = realtime_eci.n_realtime_packets
    assert end_n_realtime_packets > start_n_realtime_packets

################################

ALL_REALTIME_MSG_CLASSES = set(leaf_classes(RealtimeMsg))

def _test_setRealtimeCfg_common(callback: Callable, realtime_eci: CovviInterface):
    counter = 0
    def common_callback(b: ControlMsg):
        nonlocal counter
        counter = counter + 1
        b.uid, b.dev_id
        assert b.cmd_type == Command(value=CommandString.RTD)
        assert type(b) in ALL_REALTIME_MSG_CLASSES
        assert b.data_len > 0
        callback(b)
    realtime_eci.resetRealtimeCfg()
    start_n_realtime_packets = realtime_eci.n_realtime_packets
    yield common_callback
    sleep(REALTIME_TEST_TIME)
    realtime_eci.setRealtimeCfg()
    # assert realtime_eci.n_realtime_packets > start_n_realtime_packets
    # assert counter > 0
    # assert realtime_eci.n_realtime_packets == counter

################################

# @pytest.mark.parametrize('cls, kwargs', [
#     [DigitStatusAllMsg,  dict(digit_status    = True)],
#     [DigitPosnAllMsg,    dict(digit_posn      = True)],
#     [CurrentGripMsg,     dict(current_grip    = True)],
#     [ElectrodeValueMsg,  dict(electrode_value = True)],
#     [InputStatusMsg,     dict(input_status    = True)],
#     [MotorCurrentAllMsg, dict(motor_current   = True)],
#     [DigitTouchAllMsg,   dict(digit_touch     = True)],
#     [DigitErrorMsg,      dict(digit_error     = True)],
#     [EnvironmentalMsg,   dict(environmental   = True)],
#     [OrientationMsg,     dict(orientation     = True)],
#     [MotorLimitsMsg,     dict(motor_limits    = True)],
# ])
# def test_setRealtimeCfg(cls: type, kwargs: Dict[str, bool], realtime_eci: CovviInterface):
#     def callback(m: ControlMsg):
#         assert m
#         assert issubclass(type(m), cls)
        
#     for realtime_eci._callback_Dict[caDigitStatus_all] in _test_setRealtimeCfg_common(callback, realtime_eci):
#     # for realtime_eci.callbackDigitStatus in _test_setRealtimeCfg_common(callback, realtime_eci):
#         realtime_eci.setRealtimeCfg(**kwargs)

def test_setRealtimeCfg_DigitStatusAllMsg(realtime_eci: CovviInterface):
    def callback(m: DigitStatusAllMsg):
        assert issubclass(type(m), DigitStatusAllMsg)
    for realtime_eci.callbackDigitStatus in _test_setRealtimeCfg_common(callback, realtime_eci):
        realtime_eci.setRealtimeCfg(digit_status = True)

def test_setRealtimeCfg_DigitPosnMsg(realtime_eci: CovviInterface):
    def callback(m: DigitPosnAllMsg):
        assert issubclass(type(m), DigitPosnAllMsg)
    for realtime_eci.callbackDigitPosn in _test_setRealtimeCfg_common(callback, realtime_eci):
        realtime_eci.setRealtimeCfg(digit_posn = True)

def test_setRealtimeCfg_CurrentGripMsg(realtime_eci: CovviInterface):
    def callback(m: CurrentGripMsg):
        assert issubclass(type(m), CurrentGripMsg)
    for realtime_eci.callbackCurrentGrip in _test_setRealtimeCfg_common(callback, realtime_eci):
        realtime_eci.setRealtimeCfg(current_grip = True)

def test_setRealtimeCfg_ElectrodeValueMsg(realtime_eci: CovviInterface):
    def callback(m: ElectrodeValueMsg):
        assert issubclass(type(m), ElectrodeValueMsg)
    for realtime_eci.callbackElectrodeValue in _test_setRealtimeCfg_common(callback, realtime_eci):
        realtime_eci.setRealtimeCfg(electrode_value = True)

def test_setRealtimeCfg_InputStatusMsg(realtime_eci: CovviInterface):
    def callback(m: InputStatusMsg):
        assert issubclass(type(m), InputStatusMsg)
    for realtime_eci.callbackInputStatus in _test_setRealtimeCfg_common(callback, realtime_eci):
        realtime_eci.setRealtimeCfg(input_status = True)

def test_setRealtimeCfg_MotorCurrentMsg(realtime_eci: CovviInterface):
    def callback(m: MotorCurrentAllMsg):
        assert issubclass(type(m), MotorCurrentAllMsg)
    for realtime_eci.callbackMotorCurrent in _test_setRealtimeCfg_common(callback, realtime_eci):
        realtime_eci.setRealtimeCfg(motor_current = True)

def test_setRealtimeCfg_DigitTouchMsg(realtime_eci: CovviInterface):
    def callback(m: DigitTouchAllMsg):
        assert issubclass(type(m), DigitTouchAllMsg)
    for realtime_eci.callbackDigitTouch in _test_setRealtimeCfg_common(callback, realtime_eci):
        realtime_eci.setRealtimeCfg(digit_touch = True)

def test_setRealtimeCfg_DigitErrorMsg(realtime_eci: CovviInterface):
    def callback(m: DigitErrorMsg):
        assert issubclass(type(m), DigitErrorMsg)
    for realtime_eci.callbackDigitError in _test_setRealtimeCfg_common(callback, realtime_eci):
        realtime_eci.setRealtimeCfg(digit_error = True)

def test_setRealtimeCfg_EnvironmentalMsg(realtime_eci: CovviInterface):
    def callback(m: EnvironmentalMsg):
        assert issubclass(type(m), EnvironmentalMsg)
    for realtime_eci.callbackEnvironmental in _test_setRealtimeCfg_common(callback, realtime_eci):
        realtime_eci.setRealtimeCfg(environmental = True)

def test_setRealtimeCfg_OrientationMsg(realtime_eci: CovviInterface):
    def callback(m: OrientationMsg):
        assert issubclass(type(m), OrientationMsg)
    for realtime_eci.callbackOrientation in _test_setRealtimeCfg_common(callback, realtime_eci):
        realtime_eci.setRealtimeCfg(orientation = True)

def test_setRealtimeCfg_MotorLimitsMsg(realtime_eci: CovviInterface):
    def callback(m: MotorLimitsMsg):
        assert issubclass(type(m), MotorLimitsMsg)
    for realtime_eci.callbackMotorLimits in _test_setRealtimeCfg_common(callback, realtime_eci):
        realtime_eci.setRealtimeCfg(motor_limits = True)
