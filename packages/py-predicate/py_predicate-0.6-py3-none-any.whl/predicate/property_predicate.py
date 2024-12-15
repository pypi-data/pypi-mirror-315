from dataclasses import dataclass
from typing import Callable, override

from predicate import Predicate


@dataclass
class PropertyPredicate[T](Predicate[T]):
    """A predicate class that wraps a boolean property."""

    getter: property

    def __init__(self, getter: Callable):
        self.getter = getter

    def __call__(self, obj: T) -> bool:
        return self.getter.fget(obj)  # type: ignore

    def __repr__(self) -> str:
        return "property_p"

    @override
    def explain_failure(self, obj: T) -> dict:
        return {"result": False, "reason": "tbd"}


def property_p(getter: Callable):
    return PropertyPredicate(getter=getter)
