from unittest import TestCase

import pytest

from lotion import Lotion
from lotion.properties.number import Number


@pytest.mark.api()
class TestApiFormula(TestCase):
    DATABASE_ID = "15d6567a3bbf80fe8855d0383a7eb7dd"

    def setUp(self) -> None:
        self.suite = Lotion.get_instance()

    def test_数式の入ったページを取得する(self):
        # When
        actual = self.suite.retrieve_page(page_id="15d6567a3bbf803d9c3eeebb80b24d89")

        # Then
        actual_string = actual.get_formula(name="数式_文字列").value
        self.assertEqual(actual_string, "100円です")
        actual_number = actual.get_formula(name="数式_数値").value
        self.assertEqual(actual_number, 50)

    def test_数式の入ったページを更新する(self):
        # When
        properties = [
            Number.from_num(name="数値", value=200),
        ]
        new_page = self.suite.create_page_in_database(
            database_id=self.DATABASE_ID,
            properties=properties,
        )
        properties = new_page.properties.append_property(Number.from_num(name="数値", value=300))
        self.suite.update_page(
            page_id=new_page.page_id.value,
            properties=properties.values,
        )
        actual = self.suite.retrieve_page(page_id=new_page.page_id.value)
