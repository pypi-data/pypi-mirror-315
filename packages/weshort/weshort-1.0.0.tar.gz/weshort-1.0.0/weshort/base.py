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

import aiohttp
from typing import Optional

from .exception import ResponseError
from .types import Response
from .version import __version__


class Base:
    version = __version__
    apiToken: str
    baseUrl: str = "https://api.weshort.pro/api"
    def __init__(self, apiToken: str):
        self.apiToken = apiToken
        self.headers = {
            "Content-Type": "application/json",
            "Xd-Token": self.apiToken
        }

    async def post(self, path: str, data: Optional[dict] = None, headers: Optional[dict] = None) -> Response:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            res = await session.post(
                url=f"{self.baseUrl}{path}",
                json=data,
                headers=headers
            )
            json = await res.json()
            response: Response = Response(**json)
            if response.responseSuccess:
                return response
            else:
                raise ResponseError(response.responseMessage)

    async def get(
        self,
        path: str,
        data: Optional[dict] = None,
        headers: Optional[dict] = None
    ):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            req = await session.get(url=f"{self.baseUrl}{path}", json=data, headers=headers)
            json = await req.json()
            response: Response = Response(**json)
            if response.responseSuccess:
                return response
            else:
                raise ResponseError(response.responseMessage)

    async def delete(
        self,
        path: str,
        data: Optional[dict] = None,
        headers: Optional[dict] = None
    ):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            req = await session.delete(url=f"{self.baseUrl}{path}", json=data, headers=headers)
            json = await req.json()
            response: Response = Response(**json)
            if response.responseSuccess:
                return response
            else:
                raise ResponseError(response.responseMessage)
