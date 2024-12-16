
import os
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST, IPPROTO_UDP
from logging import debug

from eci.primitives import FourOctetAddress
from eci.sockets.messages import DiscoveryRequestMsg, DiscoveryConfigMsg
from eci.sockets.discovery.discovery_socket import DiscoverySocket


DISCOVERY_SENDING_ADDRESS = str(FourOctetAddress(os.environ.get('DISCOVERY_SENDING_ADDRESS', '255.255.255.255')))


class DiscoverySendingSocket(DiscoverySocket):
    '''A UDP socket for sending discovery requests and configuration messages.'''

    def __init__(self, host: str = ''):
        debug(f'''Initializing discovery sending socket host='{host}' port={DiscoverySocket.PORT}''')
        super().__init__(host=host, port=DiscoverySocket.PORT, family=AF_INET, type=SOCK_DGRAM, proto=IPPROTO_UDP)
        self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.settimeout(DiscoverySocket.TIMEOUT)
        debug(f'''Initialized discovery sending socket host='{host}' port={DiscoverySocket.PORT}''')

    def __enter__(self):
        debug('Binding discovery sending socket')
        super().__enter__()
        self.bind((self.host, self.port))
        debug('Bound discovery sending socket')
        return self

    def send_request(self) -> int:
        msg = DiscoveryRequestMsg()
        debug(f'{msg} has been sent to {DISCOVERY_SENDING_ADDRESS} on port {DiscoverySocket.PORT}')
        return self.sendto(msg.pack(), (DISCOVERY_SENDING_ADDRESS, DiscoverySocket.PORT))

    def send_config(self, msg: DiscoveryConfigMsg, addr: str) -> int:
        debug(f'{msg} has been sent to {addr} on port {DiscoverySocket.PORT}')
        return self.sendto(msg.pack(), (addr, DiscoverySocket.PORT))
