from dataclasses import dataclass
from lotion.filter.condition import Condition, StringCondition, NumberCondition, NumberConditionType
from lotion.properties import Property, Title


@dataclass
class FilterBuilder:
    conditions: list[Condition]

    def __init__(self, conditions: list[Condition] | None = None) -> None:
        self.conditions = conditions or []

    @staticmethod
    def create(condition: Condition) -> "FilterBuilder":
        return FilterBuilder(conditions=[condition])

    def add_condition(self, condition: Condition) -> "FilterBuilder":
        return FilterBuilder(conditions=[*self.conditions, condition])

    def add(self, condition: Condition) -> "FilterBuilder":
        return FilterBuilder(conditions=[*self.conditions, condition])

    @staticmethod
    def build_simple_equal_condition(property: Property) -> dict:  # noqa: A002
        """指定されたプロパティが指定された値と一致する条件を作成する"""
        result = FilterBuilder().add_condition(StringCondition.equal(property=property)).build()
        if result is None:
            msg = "Filter is empty"
            raise ValueError(msg)
        return result

    @staticmethod
    def build_simple_equal_unique_id_condition(name: str, number: int) -> dict:
        """unique_idが指定された値と一致する条件を作成する"""
        number_condition = NumberCondition(
            property_name=name,
            property_type="unique_id",
            condition_type=NumberConditionType.EQUALS,
            value=number,
        )
        result = FilterBuilder.create(number_condition).build()
        if result is None:
            msg = "Filter is empty"
            raise ValueError(msg)
        return result

    @staticmethod
    def build_title_equal_condition(title: str, name: str = "名前") -> dict:
        """名前が指定された値と一致する条件を作成する"""
        title_prop = Title.from_plain_text(name=name, text=title)
        return FilterBuilder.build_simple_equal_condition(property=title_prop)

    def build(self) -> dict | None:
        if len(self.conditions) == 0:
            return None
        if len(self.conditions) == 1:
            return self.conditions[0].__dict__()
        return {
            "and": [condition.__dict__() for condition in self.conditions],
        }
