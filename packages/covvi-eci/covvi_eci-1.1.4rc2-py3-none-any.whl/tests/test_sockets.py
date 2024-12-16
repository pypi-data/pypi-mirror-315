
import os

from eci import FourOctetAddress

from tests.sockets import ControlSocket, RealtimeSocket, DiscoveryReceivingSocket, DiscoverySendingSocket


ECI_HOST  = str(FourOctetAddress(os.environ.get('ECI_HOST',  '192.168.1.5')))
THIS_HOST = str(FourOctetAddress(os.environ.get('THIS_HOST', '')))


def test_ControlSocket():
    with ControlSocket(ECI_HOST):
        ...


def test_RealtimeSocket():
    with RealtimeSocket(THIS_HOST, 12345):
        ...


def test_DiscoveryReceivingSocket():
    with DiscoveryReceivingSocket():
        ...


def test_DiscoverySendingSocket():
    with DiscoverySendingSocket():
        ...
