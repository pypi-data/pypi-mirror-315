
import os
import pytest
from typing import Tuple

from eci import FourOctetAddress

from tests.interfaces import DiscoveryInterface
from tests.sockets import DiscoveryReceivingSocket
from tests.messages import DiscoveryRequestMsg, DiscoveryResponseMsg, DiscoveryConfigMsg


THIS_HOST = str(FourOctetAddress(os.environ.get('THIS_HOST', '')))


################################################################################################################################
# DiscoveryInterface fixtures
################################################################################################################################

@pytest.fixture(scope='module')
def interface():
    print('Starting module fixture')
    with DiscoveryInterface(THIS_HOST) as interface:
        yield interface
    print('Closing module fixture')

def test_interface(interface: DiscoveryInterface):
    assert interface

################################################################################################################################
# Tests
################################################################################################################################

def test_DiscoveryRequestMsg():
    assert DiscoveryRequestMsg() == DiscoveryRequestMsg.unpack(DiscoveryRequestMsg().pack())

def test_send_request(interface: DiscoveryInterface):
    assert interface.send_request()

def check_DiscoveryResponseMsg(msg: DiscoveryResponseMsg, addr: Tuple[str, int]):
    assert addr
    host, port = addr
    assert host
    assert port
    assert port == DiscoveryReceivingSocket.PORT
    if msg:
        assert msg
        DiscoveryResponseMsg.unpack(msg.pack())

def test_recvfrom_disco_packet(interface: DiscoveryInterface):
    test_send_request(interface)
    check_DiscoveryResponseMsg(*interface.recvfrom_disco_packet())

def test_get_eci_list(interface: DiscoveryInterface):
    test_send_request(interface)
    for msg, addr in interface.get_eci_list():
        check_DiscoveryResponseMsg(msg, addr)
