from dataclasses import dataclass
from lotion.properties.property import Property


@dataclass
class Select(Property):
    selected_name: str | None
    selected_id: str | None
    selected_color: str | None
    type: str = "select"

    def __init__(
        self,
        name: str,
        selected_name: str | None = None,
        selected_id: str | None = None,
        selected_color: str | None = None,
        id: str | None = None,
    ):
        self.name = name
        self.id = id
        self.selected_name = selected_name
        self.selected_id = selected_id if selected_id is not None else "default"
        self.selected_color = selected_color if selected_color is not None else "default"

    @staticmethod
    def of(name: str, param: dict) -> "Select":
        select = param["select"]
        if select is None:
            return Select(name=name)
        return Select(
            name=name,
            selected_id=select["id"],
            selected_name=select["name"],
            selected_color=select["color"],
            id=param["id"],
        )

    def __dict__(self):
        if self.selected_name is None:
            return {
                self.name: {
                    "type": self.type,
                    "select": None,
                }
            }
        result = {
            "type": self.type,
            "select": {
                "id": self.selected_id,
                "name": self.selected_name,
                "color": self.selected_color,
            },
        }
        if self.id is not None:
            result["id"] = self.id
        return {self.name: result}

    def value_for_filter(self) -> str:
        return self.selected_name if self.selected_name is not None else ""
