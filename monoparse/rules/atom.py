import re
from operator import rshift
from dataclasses import dataclass, field
from typing import Callable, TypeVar, List, Union, Dict, Tuple, Any

__all__ = ("Atom",)


@dataclass
class Atom:
    body: Union["Atom", str]
    optional: bool = field(default=False)
    frozen: bool = field(default=False)
    capturable: bool = field(default=True)
    attempt_coerce: bool = field(default=True)

    alternatives: List["Atom"] = field(default_factory=list, repr=False)
    followed_by: List["Atom"] = field(default_factory=list, repr=False)

    # Helpers

    def _process(self, other: Union[Any, "Atom"]) -> Tuple["Atom", "Atom"]:
        if not isinstance(other, Atom):
            if self.attempt_coerce:
                other = Atom(other)
            else:
                raise TypeError(f"Unable to coerce object to Atom form ({other=!r})")

        if self.frozen:
            atom = type(self)(self.body, self.optional, self.frozen)
        else:
            atom = self

        return (atom, other)

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
            total = ((fmt and [fmt]) or []) + parts
            fmt = f'({"|".join(total)})'

        for atom in self.followed_by:
            assert isinstance(atom, Atom), repr(atom)
            fmt += atom.compile()

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
        atom, other, = self._process(other)
        atom.alternatives.append(other)
        return atom

    def __rshift__(self, other):
        atom, other, = self._process(other)
        atom.followed_by.append(other)
        return atom
