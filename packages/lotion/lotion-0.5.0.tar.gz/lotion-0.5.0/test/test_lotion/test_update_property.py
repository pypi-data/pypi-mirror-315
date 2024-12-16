from unittest import TestCase

import pytest

from test.test_lotion.lotion_utils import create_empty_page, remove_page, update_page


@pytest.mark.api()
class TestUpdateProperty(TestCase):
    DATABASE_ID = "1596567a3bbf80d58251f1159e5c40fa"

    def setUp(self) -> None:
        self.page = create_empty_page(database_id=self.DATABASE_ID)
        return super().setUp()

    def tearDown(self) -> None:
        remove_page(page_id=self.page.page_id)
        return super().setUp()

    def test_ファイルを変更する(self):
        self.skipTest("ファイルプロパティを作成するところから")
