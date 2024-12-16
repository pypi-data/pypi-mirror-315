from unittest import TestCase

import pytest

from lotion.filter.builder import Builder
from lotion.filter.condition import Prop, Cond
from lotion import Lotion


@pytest.mark.api()
class TestSearch(TestCase):
    DATABASE_ID = "15d6567a3bbf8032ada3e0a42892c357"

    def setUp(self) -> None:
        self.suite = Lotion.get_instance()
        return super().setUp()

    def test_検索_シンプルなテキスト検索(self):
        # Given
        filter_param = {
            "property": "テキスト",
            "rich_text": {
                "contains": "A",
            },
        }
        self._search_and_assert(filter_param, 1)

    def test_検索_複数の条件指定(self):
        # Given
        filter_param = (
            Builder.create()
            .add(Prop.RICH_TEXT, "名前", Cond.STARTS_WITH, "テスト")
            .add(Prop.NUMBER, "数値", Cond.GREATER_THAN, 50)
            .build()
        )
        self._search_and_assert(filter_param, 1)

    def test_検索_日付の検索(self):
        # Given
        filter_param = Builder.create().add(Prop.DATE, "日付", Cond.AFTER, "2021-01-01").build()
        self._search_and_assert(filter_param, 1)

    def test_検索_日付の検索_1年前以内(self):
        # Given
        filter_param = Builder.create().add(Prop.DATE, "日付", Cond.PAST_YEAR).build()
        self._search_and_assert(filter_param, 1)

    def test_or条件(self):
        # Given
        filter_param_a = Builder.create().add(Prop.RICH_TEXT, "名前", Cond.EQUALS, "テストA").build()
        filter_param_b = Builder.create().add(Prop.RICH_TEXT, "テキスト", Cond.EQUALS, "テキストB").build()
        filter_param = {
            "or": [filter_param_a, filter_param_b],
        }
        self._search_and_assert(filter_param, 2)

    def _search_and_assert(self, filter_param: dict, expected: int):
        # When
        actual = self.suite.retrieve_database(
            database_id=self.DATABASE_ID,
            filter_param=filter_param,
        )

        # Then
        self.assertEqual(expected, len(actual))
