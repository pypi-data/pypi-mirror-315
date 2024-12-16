from lotion import Lotion
from lotion.base_page import BasePage
from lotion.properties.property import Property
from lotion.page import PageId


def create_empty_page(database_id: str):
    lotion = Lotion.get_instance()
    return lotion.create_page_in_database(database_id=database_id)


def update_page(page: BasePage, property: Property):
    # When
    lotion = Lotion.get_instance()
    properties = page.properties.append_property(property)
    lotion.update_page(page_id=page.page_id.value, properties=properties.values)

    # Then
    return lotion.retrieve_page(page_id=page.page_id.value)


def remove_page(page_id: PageId):
    lotion = Lotion.get_instance()
    lotion.remove_page(page_id.value)
