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


class Withdraw:
    def __init__(self, **kwargs):
        self.id: int = kwargs.get("id", 0)
        self.clientName: str = kwargs.get("clientName", "")
        self.withdrawId: str = kwargs.get("withdrawId", "")
        self.method: str = kwargs.get("method", "")
        self.noRek: str = kwargs.get("noRek", "")
        self.nameRek: str = kwargs.get("nameRek", "")
        self.amount: int = kwargs.get("amount", 0)
        self.feeAdmin: int = kwargs.get("feeAdmin", 0)
        self.status: str = kwargs.get("status", "")
        self.createdAt: str = kwargs.get("createdAt", "")
        self.updatedAt: str = kwargs.get("updatedAt", "")

    def parser(self):
        return {
            "_": "Withdraw",
            "id": self.id,
            "clientName": self.clientName,
            "withdrawId": self.withdrawId,
            "method": self.method,
            "noRek": self.noRek,
            "nameRek": self.nameRek,
            "amount": self.amount,
            "feeAdmin": self.feeAdmin,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
