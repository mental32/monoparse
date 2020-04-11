from dataclasses import dataclass

from .atom import Atom

__all__ = ("Maybe", "OneOf", "OneOrMore", "NoneOrSome")


@dataclass
class Maybe(Atom):
    def __post_init__(self):
        self.optional = True


class OneOrMore(Atom):
    def compile(self):
        return f"{super().compile()}+"


class NoneOrSome(Atom):
    def compile(self):
        return f"{super().compile()}*"


@dataclass
class OneOf(Atom):
    def __post_init__(self):
        self.alternatives = list(map(Atom, map(re.escape, self.body)))
        self.body = ""
