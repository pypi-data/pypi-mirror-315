import re
from dataclasses import dataclass


@dataclass(frozen=True)
class PageId:
    value_: str

    def __post_init__(self) -> None:
        # 型チェック
        if not isinstance(self.value_, str):
            msg = f"page_idは文字列である必要があります: {self.value_}"
            raise TypeError(msg)

        # UUID4の形式であることを確認する
        if not re.match(r"[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}", self.value_):
            msg = f"page_idの形式が不正です: {self.value_}"
            raise ValueError(msg)

    @staticmethod
    def dummy() -> "PageId":
        return PageId(value_="5c38fd30-714b-4ce2-bf2d-25407f3cfc16")

    @property
    def value(self) -> str:
        """UUID4の形式の文字列を返す"""
        # まずハイフンを削除してから、ハイフンをつけなおす
        value_ = self.value_.replace("-", "")
        return "-".join([value_[:8], value_[8:12], value_[12:16], value_[16:20], value_[20:]])
