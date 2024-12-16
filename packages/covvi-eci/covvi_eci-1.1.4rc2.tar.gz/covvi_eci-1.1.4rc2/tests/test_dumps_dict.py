
import pytest

from tests.messages import BaseMessage
from tests.messages_util import n_random_messages_per_cls


@pytest.mark.parametrize('msg', n_random_messages_per_cls(BaseMessage, 100))
def test_dumps_dict(msg: BaseMessage):
    assert msg.dumps() == type(msg)(**msg.dict).dumps()
