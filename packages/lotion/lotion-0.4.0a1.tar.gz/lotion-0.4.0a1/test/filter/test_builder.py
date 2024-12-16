from unittest import TestCase


from lotion.filter.builder import Builder
from lotion.filter.condition import Prop, Cond

# https://developers.notion.com/reference/post-database-query-filter


class TestBuilder(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_タイトルで絞りこむ(self):
        actual = (
            Builder.create()
            .add(prop_type=Prop.RICH_TEXT, prop_name="名前", cond_type=Cond.EQUALS, value="テストA")
            .build()
        )
        expected = {
            "property": "名前",
            "rich_text": {
                "equals": "テストA",
            },
        }
        self.assertEqual(expected, actual)
