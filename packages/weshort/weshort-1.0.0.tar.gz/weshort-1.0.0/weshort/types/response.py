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


class Response:
    def __init__(self, **kwargs):
        self.responseCode: int = kwargs.get("responseCode", 0)
        self.responseSuccess: bool = kwargs.get("responseSuccess", False)
        self.responseMessage: str = kwargs.get("responseMessage", "")
        self.responseData: dict = kwargs.get("responseData", None)

    def parser(self):
        return {
            "_": "Response",
            "responseCode": self.responseCode,
            "responseSuccess": self.responseSuccess,
            "responseMessage": self.responseMessage,
            "responseData": self.responseData
        }
