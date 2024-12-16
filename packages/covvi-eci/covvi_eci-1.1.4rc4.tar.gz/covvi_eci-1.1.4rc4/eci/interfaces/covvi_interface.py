
from time import sleep
from logging import debug
from typing import Union

from eci.interfaces.utils      import public
from eci.interfaces.control    import ControlInterface
from eci.interfaces.realtime   import RealtimeInterface
from eci.interfaces.messages   import HandPowerMsg, DeviceInfoMsg, OrientationMsg
from eci.interfaces.primitives import FourOctetAddress
from eci.interfaces.enums      import CommandCode, NetDevice


class CovviInterface(RealtimeInterface, ControlInterface):
    '''An interface to combine all functionality from all the interfaces into a single one, except 'DiscoveryInterface'.'''

    HAND_POWERED_ON_TIMEOUT = 2**-4

    def __init__(self, host: Union[FourOctetAddress, str]):
        debug('Initializing the Covvi Interface')
        super(ControlInterface, self).__init__(host)
        RealtimeInterface.__init__(self, None, None)
        self.hand_powered_on: bool = False
        self._message_dict[DeviceInfoMsg] = self._process_DeviceInfoMsg
        debug('Initialized the Covvi Interface')

    def __enter__(self):
        debug('Starting the Covvi Interface')
        super(ControlInterface, self).__enter__()
        self.local_host, self.local_port = self._ctl_socket.getsockname()
        RealtimeInterface.__enter__(self)
        debug('Started the Covvi Interface')
        return self

    def __exit__(self, *args):
        debug('Closing the Covvi Interface')
        RealtimeInterface.__exit__(self)
        super(ControlInterface, self).__exit__()
        debug('Closed the Covvi Interface')

    ################################################################

    def _process_DeviceInfoMsg(self, msg: DeviceInfoMsg) -> None:
        self.hand_powered_on = msg.connected if msg.device_id == NetDevice.D1 else self.hand_powered_on

    def _setHandPower(self, enable: bool) -> HandPowerMsg:
        return self._send(HandPowerMsg(cmd_type=CommandCode.CMD, enable=enable))

    @public
    def setHandPowerOn(self) -> HandPowerMsg:
        '''Power on the hand'''
        debug('Powering on the hand')
        r = self._setHandPower(True)
        debug('Waiting for the hand to power on')
        while not self.hand_powered_on:
            sleep(CovviInterface.HAND_POWERED_ON_TIMEOUT)
        self.setRealtimeCfg(orientation = True)
        return r

    @public
    def setHandPowerOff(self) -> HandPowerMsg:
        '''Power off the hand'''
        debug('Powering off the hand')
        r = self._setHandPower(False)
        self.hand_powered_on = False
        return r

    ################################################################

    @public
    def resetRealtimeCfg(self):
        self.setRealtimeCfg()
        RealtimeInterface.resetRealtimeCfg(self)

    @public
    def getOrientation(self) -> OrientationMsg:
        '''Get hand orientation

        X Position
        Y Position
        Z Position
        '''
        if type(self.orientation_msg) == type(None):
            self.orientation_msg = ControlInterface.getOrientation(self)
        return self.orientation_msg
