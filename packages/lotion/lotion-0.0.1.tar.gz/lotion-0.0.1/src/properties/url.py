from dataclasses import dataclass

from src.properties.property import Property


@dataclass
class Url(Property):
    url: str
    type: str = "url"

    def __init__(self, name: str, url: str, id: str | None = None):
        self.name = name
        self.url = url
        self.id = id

    @staticmethod
    def of(name: str, param: dict) -> "Url":
        return Url(
            name=name,
            url=param["url"],
            id=param["id"],
        )

    @staticmethod
    def from_url(url: str, name: str = "URL") -> "Url":
        return Url(
            name=name,
            url=url,
        )

    def value_for_filter(self) -> str:
        return self.url

    def __dict__(self):
        result = {
            "type": self.type,
            "url": self.url,
        }
        if self.id is not None:
            result["id"] = self.id
        return {
            self.name: result,
        }
