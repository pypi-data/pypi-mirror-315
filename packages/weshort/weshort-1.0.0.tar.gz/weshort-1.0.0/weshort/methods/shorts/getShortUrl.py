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

from typing import List

import weshort
from weshort.exception import WeShortError
from weshort.types import ShortUrl, Response


class GetShortUrl:
    async def getShortsUrl(self: "weshort.WeShort") -> List[ShortUrl]:
        """Get All Short URL, the main means for interacting with API WeShort.

        Returns:
            ``List[ShortUrl]``: List of ShortUrl.

        Example:
            >>> from weshort import WeShort
            >>> 
            >>> weShort = WeShort(apiToken="YOUR_API_TOKEN")
            >>> try:
            >>>     url = await weShort.getShortUrl("pZO1WopFBjU2B6XJ")
            >>>     print(url) # output: List[ShortUrl]
            >>> except WeShortError as e:
            >>>     print(e)
        """
        res = await self.get(
            f"/short",
        )
        if not isinstance(res, Response):
            raise WeShortError(res)
        shortsUrl: List[ShortUrl] = [
            ShortUrl(
                **x,
                shortUrl=f"https://weshort.pro/{x['keyword']}"
            ) for x in res.responseData
        ]
        return shortsUrl

    async def getShortUrl(self: "weshort.WeShort", keyword: str) -> ShortUrl:
        """Get Short URL, the main means for interacting with API WeShort.

        Parameters:
            keyword (``str``):
                Keyword for Get Short URL, e.g.: "pZO1WopFBjU2B6XJ".

        Returns:
            ``ShortUrl``: ShortUrl class.

        Example:
            >>> from weshort import WeShort
            >>> 
            >>> weShort = WeShort(apiToken="YOUR_API_TOKEN")
            >>> try:
            >>>     url = await weShort.getShortUrl("pZO1WopFBjU2B6XJ")
            >>>     print(url) # output: ShortUrl
            >>> except WeShortError as e:
                    print(e)
        """
        res = await self.get(
            f"/short?keyword={keyword}",
        )
        if not isinstance(res, Response):
            raise WeShortError(res)
        return ShortUrl(**res.responseData)
