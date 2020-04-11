from dataclasses import dataclass

from .atom import Atom


@dataclass
class Immutable(Atom):
    def __post_init__(self):
        self.frozen = True
