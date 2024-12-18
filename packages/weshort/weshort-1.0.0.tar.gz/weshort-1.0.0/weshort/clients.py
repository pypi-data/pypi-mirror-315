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

from aiohttp import ClientSession
from typing import Union

from .base import Base
from .exception import WeShortError
from .methods import Methods
from .types import GetMe, Response


class WeShort(Base, Methods):
    """WeShort Client, the main means for interacting with API AyiinHub.

    Parameters:
        apiToken (``str``):
            API token for Authorization Users, e.g.: "AxD_ABCDEFghIklzyxWvuew".\n
            Get the *API Token* in [WeShortProfile](https://weshort.pro).

    Example:
        >>> from weshort import WeShort
        >>> 
        >>> weShort = WeShort(
        >>>     apiToken="YOUR_API_TOKEN"
        >>> )
    """
    def __init__(
        self,
        apiToken: str
    ):
        super().__init__(apiToken=apiToken)

    async def getMe(self) -> GetMe:
        res = await self.get("/client")
        if not isinstance(res, Response):
            raise WeShortError("Failed to get User Info")
        return GetMe(**res.responseData)

    async def deleteAccount(self):
        res = await self.delete("/client")
        if not isinstance(res, Response):
            raise WeShortError("Failed to delete Account")
        return True
