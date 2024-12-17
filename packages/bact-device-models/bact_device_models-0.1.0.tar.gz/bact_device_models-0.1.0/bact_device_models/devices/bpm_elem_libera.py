import functools
from dataclasses import dataclass

from typing import Sequence, Union


@dataclass
class BPMElementPosition:
    #: in nanometer
    x: int
    #: in nanometer
    y: int


@dataclass
class BPMElementSignalFromButtons:
    """Beam position monitor readings from the buttons

    Todo:
        find out what the units of these signals are in reality
    """
    a: int
    b: int
    c: int
    d: int


@dataclass
class BPMElement:
    name: str
    pos: BPMElementPosition
    sig: Union[BPMElementSignalFromButtons, None]


@dataclass
class BPMElementList:
    bpms: Sequence[BPMElement]

    def get_eleement(self, name: str) -> BPMElement:
        @functools.lru_cache(maxsize=1)
        def get_dict():
            return {elem.name: elem for elem in self.bpms}

        return get_dict()[name]
