from dataclasses import dataclass

from lotion.properties.property import Property


@dataclass
class PhoneNumber(Property):
    """PhoneNumber class

    ex.
    {'id': 'FCsG', 'type': 'phone_number', 'phone_number': '03-1234-5678'}
    """

    value: str | None

    def __init__(
        self,
        name: str,
        id: str | None = None,  # noqa: A002
        value: str | None = None,
    ) -> None:
        self.name = name
        self.id = id
        self.value = value

    @staticmethod
    def of(key: str, param: dict) -> "PhoneNumber":
        return PhoneNumber(
            id=param["id"],
            name=key,
            value=param.get("phone_number"),
        )

    @staticmethod
    def create(name: str, phone_number: str) -> "PhoneNumber":
        return PhoneNumber(name=name, value=phone_number)

    @property
    def type(self) -> str:
        return "phone_number"

    def __dict__(self) -> dict:
        result = {
            "type": self.type,
            "phone_number": self.value,
        }
        if self.id is not None:
            result["id"] = self.id
        return {
            self.name: result,
        }

    def value_for_filter(self) -> str:
        raise NotImplementedError
