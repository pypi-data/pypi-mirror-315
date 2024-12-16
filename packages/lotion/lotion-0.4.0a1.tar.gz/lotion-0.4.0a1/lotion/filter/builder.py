from dataclasses import dataclass
from typing import Any

from lotion.filter.condition_ruleset import ConditionRuleset
from lotion.filter.condition import Prop, Cond


@dataclass(frozen=True)
class Builder:
    conditions: list[dict]

    @staticmethod
    def create() -> "Builder":
        return Builder(conditions=[])

    def add(self, prop_type: Prop, prop_name: str, cond_type: Cond, value: Any = None) -> "Builder":
        ConditionRuleset(prop_type, cond_type, value).validate()
        param = {
            "property": prop_name,
            prop_type.value: {
                cond_type.value: value if value is not None else {},
            },
        }
        return Builder(conditions=[*self.conditions, param])

    def is_empty(self) -> bool:
        return len(self.conditions) == 0

    def build(self) -> dict:
        if len(self.conditions) == 0:
            raise ValueError("Filter is empty")
        if len(self.conditions) == 1:
            return self.conditions[0]
        return {
            "and": self.conditions,
        }
