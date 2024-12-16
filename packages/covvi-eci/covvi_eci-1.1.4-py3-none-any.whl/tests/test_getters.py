
import pytest
import inspect

from tests.messages import ControlMsg
from tests.interfaces import CovviInterface
from tests.fixtures import eci


parameterless_getters = [
    func_name
    for func in CovviInterface.publics()
    for func_name in [func.__name__]
    if inspect.isfunction(func)
    if func_name.startswith('get')
    for args in [inspect.signature(func)]
    if len(args.parameters) == 1
]


def test_eci(eci: CovviInterface):
    assert eci


@pytest.mark.parametrize('func_name', parameterless_getters)
def test_parameterless_getters(func_name: str, eci: CovviInterface):
    return_msg = getattr(eci, func_name)()
    if issubclass(type(return_msg), ControlMsg):
        return_msg: ControlMsg
        assert return_msg == type(return_msg).unpack(return_msg.pack())
