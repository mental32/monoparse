import re
from operator import rshift
from dataclasses import dataclass, field
from typing import Callable, TypeVar, List, Union, Dict

__all__ = ("Atom",)


@dataclass
class Atom:
    body: Union["Atom", str]
    optional: bool = field(default=False)
    frozen: bool = field(default=False)
    capturable: bool = field(default=True)

    alternatives: List["Atom"] = field(default_factory=list, repr=False)
    followed_by: List["Atom"] = field(default_factory=list, repr=False)

    # Public

    def compile(self) -> str:
        if self.body:
            if not isinstance(self.body, str):
                fmt = f"{self.body.compile()}"
            else:
                fmt = self.body

            if fmt and self.optional:
                fmt += "?"
        else:
            fmt = ""

        parts = [alt.compile() for alt in self.alternatives]

        if parts:
            if fmt:
                parts.insert(0, fmt)
            fmt = f'({"|".join(parts)})'

        for Atom in self.followed_by:
            fmt += Atom.compile()

        if self.followed_by:
            if not self.capturable:
                return f"(?:{fmt})"
            else:
                return f"({fmt})"

        if self.capturable:
            return f"({fmt})"

        return fmt

    # Overloaded

    def __or__(self, other):
        if not isinstance(other, Atom):
            other = Atom(other)

        if self.frozen:
            inst = type(self)(self.body, self.optional, self.frozen)
            inst.alternatives.append(other)
            return inst

        self.alternatives.append(other)
        return self

    def __rshift__(self, other):
        if not isinstance(other, Atom):
            other = Atom(other)

        if self.frozen:
            inst = type(self)(self.body, self.optional, self.frozen)
            inst.followed_by.append(other)
            return inst

        self.followed_by.append(other)
        return self
