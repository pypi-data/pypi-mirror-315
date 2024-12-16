
from dataclasses import dataclass

from eci.primitives.base_primitive import BasePrimitive


@dataclass(unsafe_hash=True)
class Percentage(BasePrimitive):
    '''This is a class to represent a percentage value. I.E. a speed, power, or limit value.'''
    MAX = 100
    MIN = 0
    value: int = 0

    def __init__(self, value: int = MIN):
        if type(value) is Percentage:
            value = value.value
        assert value in range(self.MAX + 1)
        self.value = int(value)

    def __str__(self) -> str:
        return str(self.value)
    def __int__(self) -> int:
        return int(self.value)
