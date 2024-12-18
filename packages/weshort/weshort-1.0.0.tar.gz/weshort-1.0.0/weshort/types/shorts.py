#  Weshort - Telegram MTProto API Client Library for Python
#  Copyright (C) 2024-present AyiinXd <https://github.com/AyiinXd>
#
#  This file is part of Weshort.
#
#  Weshort is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Weshort is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Weshort.  If not, see <http://www.gnu.org/licenses/>.


class ShortUrl:
    def __init__(self, **kwargs):
        self.id: int = kwargs.get("id", 0)
        self.clientName: str = kwargs.get("clientName", "")
        self.url: str = kwargs.get("url", "")
        self.keyword: str = kwargs.get("keyword", "")
        self.price: int = kwargs.get("price", 0)
        self.views: int = kwargs.get("views", 0)
        self.payments: int = kwargs.get("payments", 0)
        self.createdAt: str = kwargs.get("createdAt", "")
        self.updatedAt: str = kwargs.get("updatedAt", "")
        self.shortUrl: str = kwargs.get("shortUrl", "")

    def parser(self):
        return {
            "_": "ShortUrl",
            "id": self.id,
            "clientName": self.clientName,
            "url": self.url,
            "keyword": self.keyword,
            "price": self.price,
            "views": self.views,
            "payments": self.payments,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
            "shortUrl": self.shortUrl
        }
