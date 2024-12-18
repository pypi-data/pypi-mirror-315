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

from typing import Literal

import weshort
from weshort.exception import WeShortError
from weshort.types import Withdraw, Response


class RequestWithdraw:
    async def requestWithdraws(
        self: "weshort.WeShort",
        nameRek: str,
        noRek: str,
        amount: str,
        method: Literal[
            "Dana",
            "Bank BCA",
            "Bank BRI",
            "Bank BNI",
            "Bank Mandiri",
            "Bank SeaBank",
            "Bank Syariah"
        ]
    ) -> Withdraw:
        """Request Withdraw, the main means for interacting with API WeShort.
        
        Parameters:
            nameRek (``str``):
                Name of Recipient, e.g.: "AyiinDevs".
            noRek (``str``):
                Number of Recipient, e.g.: "123456789".
            amount (``str``):
                Amount of Withdraw, e.g.: "1000".
            method (``str``):
                Method of Withdraw, e.g.: "Bank SeaBank".

        Returns:
            ``Withdraw``: Withdraw Object

        Example:
            >>> from weshort import WeShort
            >>> 
            >>> weShort = WeShort(apiToken="YOUR_API_TOKEN")
            >>> try:
            >>>     requested = await weShort.requestWithdraws(
            >>>         nameRek="AyiinDevs",
            >>>         noRek="123456789",
            >>>         amount="1000",
            >>>         method="Bank SeaBank"
            >>>     )
            >>>     print(requested) # Output: Withdraw
            >>> except WeShortError as e:
            >>>     print(e)
        """
        res = await self.post(
            f"/wd",
            {
                "nama": nameRek,
                "noRek": noRek,
                "amount": amount,
                "method": method
            }
        )
        if not isinstance(res, Response):
            raise WeShortError(res)
        return Withdraw(**res.responseData)
