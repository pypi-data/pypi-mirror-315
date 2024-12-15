from dataclasses import dataclass
from typing import Any, override

from more_itertools import first

from predicate.predicate import Predicate, resolve_predicate


@dataclass
class ListOfPredicate[T](Predicate[T]):
    """A predicate class that models the list_of predicate."""

    predicate: Predicate[T]

    def __init__(self, predicate: Predicate[T]):
        self.predicate = resolve_predicate(predicate)

    def __call__(self, x: Any) -> bool:
        match x:
            case list() as l:
                return all(self.predicate(item) for item in l)
            case _:
                return False

    def __repr__(self) -> str:
        return f"is_list_of_p({repr(self.predicate)})"

    @override
    def explain_failure(self, x: Any) -> dict:
        match x:
            case list() as l:
                fail = first(item for item in l if not self.predicate(item))
                return {"result": False, "reason": f"Item '{fail}' didn't match predicate {repr(self.predicate)}"}
            case _:
                return {"result": False, "reason": f"{x} is not an instance of a list"}
