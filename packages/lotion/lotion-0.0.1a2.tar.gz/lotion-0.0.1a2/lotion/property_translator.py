from typing import Any

from lotion.properties.phone_number import PhoneNumber
from lotion.properties.created_by import CreatedBy
from lotion.properties.email import Email
from lotion.properties.last_edited_by import LastEditedBy
from lotion.properties.button import Button
from lotion.properties.checkbox import Checkbox
from lotion.properties.created_time import CreatedTime
from lotion.properties.date import Date
from lotion.properties.last_edited_time import LastEditedTime
from lotion.properties.multi_select import MultiSelect
from lotion.properties.number import Number
from lotion.properties.properties import Properties
from lotion.properties.property import Property
from lotion.properties.relation import Relation
from lotion.properties.rollup import Rollup
from lotion.properties.select import Select
from lotion.properties.status import Status
from lotion.properties.text import Text
from lotion.properties.title import Title
from lotion.properties.url import Url
from lotion.properties.person import People


class PropertyTranslator:
    @staticmethod
    def from_dict(properties: dict[str, dict]) -> Properties:
        values = []
        for key, value in properties.items():
            values.append(PropertyTranslator.from_property_dict(key, value))
        return Properties(values=[value for value in values if value is not None])

    @staticmethod
    def from_property_dict(key: str, property_: dict[str, Any]) -> "Property":  # noqa: PLR0911
        type_ = property_["type"]
        match type_:
            case "title":
                return Title.from_property(key, property_)
            case "rich_text":
                return Text.from_dict(key, property_)
            case "multi_select":
                return MultiSelect.of(key, property_)
            case "select":
                return Select.of(key, property_)
            case "number":
                return Number.of(key, property_)
            case "checkbox":
                return Checkbox.of(key, property_)
            case "date":
                return Date.of(key, property_)
            case "status":
                return Status.of(key, property_)
            case "url":
                return Url.of(key, property_)
            case "relation":
                return Relation.of(key, property_)
            case "last_edited_time":
                return LastEditedTime.create(key, property_["last_edited_time"])
            case "created_time":
                return CreatedTime.create(key, property_["created_time"])
            case "rollup":
                return Rollup.of(key, property_)
            case "button":
                return Button.of(key, property_)
            case "people":
                return People.of(key, property_)
            case "email":
                return Email.of(key, property_)
            case "phone_number":
                return PhoneNumber.of(key, property_)
            case "created_by":
                return CreatedBy.of(key, property_)
            case "last_edited_by":
                return LastEditedBy.of(key, property_)
            case _:
                msg = f"Unsupported property type: {type_} {property_}"
                raise Exception(msg)
