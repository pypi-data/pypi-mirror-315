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

import weshort
from weshort.exception import WeShortError
from weshort.types import Response


class CreateShortUrl:
    async def createShortUrl(self: "weshort.WeShort", url: str, price: int) -> str:
        """Create Short URL, the main means for interacting with API WeShort.

        Parameters:
            url (``str``):
                URL for shortening, e.g.: "https://youtu.be/YcQFi-1lAOo?si=pZO1WopFBjU2B6XJ".
            price (``int``):
                Price for shortening, e.g.: 1000.

        Returns:
            ``str``: Short URL.

        Example:
            >>> from weshort import WeShort
            >>> 
            >>> weShort = WeShort(apiToken="YOUR_API_TOKEN")
            >>> try:
            >>>     url = await weShort.createShortUrl("https://youtu.be/YcQFi-1lAOo?si=pZO1WopFBjU2B6XJ", 1000)
            >>>     print(url) # output: https://weshort.pro/keyword
            >>> except WeShortError as e:
            >>>     print(e)
        """
        res = await self.post(
            "/short",
            {
                "url": url,
                "price": str(price)
            }
        )
        if not isinstance(res, Response):
            raise WeShortError(res)
        return res.responseData['shortUrl']
