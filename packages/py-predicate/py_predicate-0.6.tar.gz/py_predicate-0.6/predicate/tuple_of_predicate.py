from dataclasses import dataclass
from typing import override

from more_itertools import first, ilen

from predicate.predicate import Predicate


@dataclass
class TupleOfPredicate[T](Predicate[T]):
    """A predicate class that models the tuple_of predicate."""

    predicates: list[Predicate]

    def __call__(self, x: tuple) -> bool:
        return ilen(x) == len(self.predicates) and all(p(v) for p, v in zip(self.predicates, x, strict=False))

    def __repr__(self) -> str:
        predicates_repr = ", ".join(repr(predicate) for predicate in self.predicates)
        return f"is_tuple_of_p({predicates_repr})"

    @override
    def explain_failure(self, x: tuple) -> dict:
        if (actual_length := ilen(x)) != (expected_length := len(self.predicates)):
            return {
                "result": False,
                "reason": f"Incorrect tuple size, expected: {expected_length}, actual: {actual_length}",
            }

        fail_p, fail_v = first((p, v) for p, v in zip(self.predicates, x, strict=False) if not p(v))

        return {"result": False, "reason": f"Predicate {fail_p} failed for value {fail_v}"}
