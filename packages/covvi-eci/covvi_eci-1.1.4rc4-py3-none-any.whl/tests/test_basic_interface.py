
from tests.interfaces import CovviInterface
from tests.fixtures import ECI_HOST


def test_interface_init():
    CovviInterface(ECI_HOST)


def test_interface_open_close():
    with CovviInterface(ECI_HOST):
        ...


def test_interface_enter_exit():
    eci = CovviInterface(ECI_HOST).__enter__()
    ...
    eci.__exit__()


def test_interface_start_stop():
    eci = CovviInterface(ECI_HOST).start()
    ...
    eci.stop()
