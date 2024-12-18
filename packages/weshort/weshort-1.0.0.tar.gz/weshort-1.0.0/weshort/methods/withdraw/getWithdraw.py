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
from weshort.types import Withdraw, Response


class GetWithdraw:
    async def getWithdraws(self: "weshort.WeShort") -> List[Withdraw]:
        """Get All Withdraw, the main means for interacting with API WeShort.

        Returns:
            ``List[Withdraw]``: List of Withdraw

        Example:
            >>> from weshort import WeShort
            >>> 
            >>> weShort = WeShort(apiToken="YOUR_API_TOKEN")
            >>> try:
            >>>     withdraws = await weShort.getWithdraws()
            >>>     print(withdraws) # Output: List[Withdraw]
            >>> except WeShortError as e:
            >>>     print(e)
        """
        res = await self.get(
            f"/wd",
        )
        if not isinstance(res, Response):
            raise WeShortError(res)
        getWithdraws: List[Withdraw] = [Withdraw(**x) for x in res.responseData]
        return getWithdraws

    async def getWithdraw(self: "weshort.WeShort", withdrawId: str) -> Withdraw:
        """Get Withdraw, the main means for interacting with API WeShort.
        
        Parameters:
            ``withdrawId`` (``str``): Withdraw ID

        Returns:
            ``Withdraw``: Withdraw Object

        Example:
            >>> from weshort import WeShort
            >>> 
            >>> weShort = WeShort(apiToken="YOUR_API_TOKEN")
            >>> try:
            >>>     withdraw = await weShort.getWithdraw("withdrawId")
            >>>     print(withdraw) # Output: Withdraw
            >>> except WeShortError as e:
                    print(e)
        """
        res = await self.get(
            f"/wd?withdrawId={withdrawId}",
        )
        if not isinstance(res, Response):
            raise WeShortError(res)
        return Withdraw(**res.responseData)
