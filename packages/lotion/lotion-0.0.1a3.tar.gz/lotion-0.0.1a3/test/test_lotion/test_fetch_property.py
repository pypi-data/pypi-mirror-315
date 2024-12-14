from unittest import TestCase

import pytest

from lotion.datetime_utils import jst_now
from lotion import Lotion
from lotion.properties import Title


@pytest.mark.api()
class TestFetchProperty(TestCase):
    DATABASE_ID = "1596567a3bbf80fc9aacdc21f9f5c516"

    def setUp(self) -> None:
        self.suite = Lotion.get_instance()
        created_page = self.suite.create_page_in_database(
            database_id=self.DATABASE_ID, properties=[Title.from_plain_text(text="テスト")]
        )
        self.page = self.suite.retrieve_page(page_id=created_page.page_id.value)
        self.now = jst_now().replace(second=0, microsecond=0)
        return super().setUp()

    def tearDown(self) -> None:
        self.suite.remove_page(self.page.page_id.value)
        return super().setUp()

    def test_作成日時と更新日時を取得する(self):
        self.assertEqual(self.page.created_at, self.now)
        self.assertEqual(self.page.updated_at, self.now)

    def test_作成ユーザと更新ユーザを取得する(self):
        expected_id = "510806db-4772-4f42-b4b6-6f81b6e8b788"
        expected_object = "user"
        self.assertEqual(self.page.created_by.id, expected_id)
        self.assertEqual(self.page.created_by.object, expected_object)
        self.assertEqual(self.page.edited_by.id, expected_id)
        self.assertEqual(self.page.edited_by.object, expected_object)

    def test_セレクトを取得する(self):
        # Given
        page_id = "15a6567a3bbf80ddb22add1abcbec3d6"
        page = self.suite.retrieve_page(page_id=page_id)

        # When
        select = page.get_select(name="セレクト")
        self.assertEqual(select.selected_name, "セレクトA")

    def test_未選択のセレクトを取得する(self):
        # Given
        page_id = "15a6567a3bbf803f9dcbdff9ef33355a"
        page = self.suite.retrieve_page(page_id=page_id)

        # When
        select = page.get_select(name="セレクト")
        self.assertIsNone(select.selected_name)
