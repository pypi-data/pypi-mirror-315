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


class GetMe:
    def __init__(self, **kwargs):
        self.id: int = kwargs.get("id", 0)
        self.name: str = kwargs.get("name", "")
        self.email: str = kwargs.get("email", "")
        self.avatar: str = kwargs.get("avatar", "")
        self.saldo: int = kwargs.get("saldo", 0)
        self.earnings: int = kwargs.get("penghasilan", 0)
        self.role: str = kwargs.get("role", "")
        self.createdAt: str = kwargs.get("createdAt", "")
        self.updatedAt: str = kwargs.get("updatedAt", "")

    def parser(self):
        return {
            "_": "GetMe",
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "avatar": self.avatar,
            "saldo": self.saldo,
            "earnings": self.earnings,
            "role": self.role,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
