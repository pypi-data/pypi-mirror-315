from unittest import TestCase

import pytest
from src.block.block import Block
from src.block.bookmark import Bookmark
from src.block.bulleted_list_item import BulletedlistItem
from src.block.callout import Callout
from src.block.code import Code
from src.block.divider import Divider
from src.block.embed import Embed
from src.block.heading import Heading
from src.block.image import Image
from src.block.numbered_list_item import NumberedListItem
from src.block.paragraph import Paragraph
from src.block.quote import Quote
from src.block.to_do import ToDo
from src.block.video import Video
from src.lotion import Lotion


@pytest.mark.api()
class TestAppendBlock(TestCase):
    PAGE_ID = "1596567a3bbf8049803de1ffe3616d9e"

    def setUp(self):
        self.suite = Lotion.get_instance()
        self.suite.clear_page(self.PAGE_ID)

    def test_パラグラフを追加する(self):
        text_block = Paragraph.from_plain_text(text="テスト")
        self._append_block_test(block=text_block)

    def test_ブックマークを追加する(self):
        bookmark = Bookmark.from_url(url="https://www.google.com/")
        self._append_block_test(block=bookmark)

    def test_リストを追加する(self):
        list_block = BulletedlistItem.from_plain_text(text="テスト1")
        self._append_block_test(block=list_block)
        list_block = BulletedlistItem.from_plain_text(text="テスト2")
        self._append_block_test(block=list_block)

    def test_区切り線を追加する(self):
        divider = Divider()
        self._append_block_test(block=divider)

    def test_埋め込みを追加する(self):
        embed = Embed.from_url(url="https://www.google.com/")
        self._append_block_test(block=embed)

    def test_見出しを追加する(self):
        header = Heading.from_plain_text(heading_size=1, text="テスト")
        self._append_block_test(block=header)

    def test_画像を追加する(self):
        url = "https://d3swar8tu7yuby.cloudfront.net/IMG_6286_thumb.jpg"
        image = Image.from_external_url(url=url)
        self._append_block_test(block=image)

    def test_番号付きリストを追加する(self):
        numberd_list_block = NumberedListItem.from_plain_text(text="テスト1")
        self._append_block_test(block=numberd_list_block)

        numberd_list_block = NumberedListItem.from_plain_text(text="テスト2")
        self._append_block_test(block=numberd_list_block)

    def test_引用を追加する(self):
        quote = Quote.from_plain_text(text="テスト")
        self._append_block_test(block=quote)

    def test_TODOリストを追加する(self):
        todo = ToDo.from_plain_text(text="テスト1")
        self._append_block_test(block=todo)
        todo = ToDo.from_plain_text(text="テスト2", checked=True)
        self._append_block_test(block=todo)

    def test_動画を追加する(self):
        url = "https://www.youtube.com/watch?v=L5mF2uBKhS8"
        video = Video.from_external_url(url=url)
        self._append_block_test(block=video)

    def test_コールアウトを追加する(self):
        callout = Callout.from_plain_text(text="テスト")
        self._append_block_test(block=callout)

    def test_コードを追加する(self):
        code = Code.from_plain_text(text="print('hello')", language="python")
        self._append_block_test(block=code)

    def _append_block_test(self, block):
        # When, Then
        actual = self.suite.append_block(block_id=self.PAGE_ID, block=block)
        self.assertTrue("results" in actual)
        block_by_get = self._get_first_block()
        self.assertIsInstance(block_by_get, block.__class__)

    def _get_first_block(self) -> Block:
        page = self.suite.retrieve_page(self.PAGE_ID)
        return page.block_children[0]
