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


class DeleteShortUrl:
    async def deleteShortUrl(self: "weshort.WeShort", keyword: str) -> str:
        """Delete Short URL, the main means for interacting with API WeShort.

        Parameters:
            keyword (``str``):
                Keyword for Delete Short URL, e.g.: "pZO1WopFBjU2B6XJ".

        Returns:
            ``str``: String of Response.

        Example:
            >>> from weshort import WeShort
            >>> 
            >>> weShort = WeShort(apiToken="YOUR_API_TOKEN")
            >>> try:
            >>>     url = await weShort.deleteShortUrl("pZO1WopFBjU2B6XJ")
            >>>     print(url)
            >>> except WeShortError as e:
            >>>     print(e)
        """
        res = await self.delete(
            f"/short?keyword={keyword}",
        )
        if not isinstance(res, Response):
            raise WeShortError(res)
        return res.responseMessage
