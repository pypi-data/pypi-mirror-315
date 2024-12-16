
from eci.utils import leaf_classes
from tests.util import random_value_dict
from tests.messages import control_msg_kwargs


def random_message(cls: type):
    return cls(
        **{
            key: random_value_dict.get(type, getattr(type, 'random', (lambda: 0)))()
            for key, type in cls.field_names_types()
            if key not in control_msg_kwargs
        }
    )


def n_random_messages_per_cls(base_cls: type, n: int) -> list:
    return [
        random_message(cls)
        for cls in leaf_classes(base_cls)
        for _ in range(n)
    ]
