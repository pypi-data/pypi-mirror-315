from dataclasses import dataclass

from src.properties.property import Property


@dataclass
class Email(Property):
    """Email class

    ex.
    {'id': 'Io%7C%3A', 'type': 'email', 'email': 'sample@example.com'}
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
    def of(key: str, param: dict) -> "Email":
        return Email(
            id=param["id"],
            name=key,
            value=param.get("email"),
        )

    @staticmethod
    def from_email(name: str, email: str) -> "Email":
        return Email(name=name, value=email)

    @property
    def type(self) -> str:
        return "email"

    def __dict__(self) -> dict:
        result = {
            "type": self.type,
            "email": self.value,
        }
        if self.id is not None:
            result["id"] = self.id
        return {
            self.name: result,
        }

    def value_for_filter(self) -> str:
        raise NotImplementedError
