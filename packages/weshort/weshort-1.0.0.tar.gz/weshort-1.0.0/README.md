<p align="center">
    <b>WeShort API for Python</b>
    <br>
    <a href="https://github.com/AyiinXd/pyweshort">
        Homepage
    </a>
    •
    <a href="https://github.com/AyiinXd/pyweshort/releases">
        Releases
    </a>
    •
    <a href="https://t.me/AyiinChats">
        News
    </a>
</p>

<p align="center">
  <img src="https://weshort.pro/images/branch.png">
</p>

## WeShort

> WeShort is Shortener URL and Asynchronous API in Python

``` python
from weshort import WeShort
from weshort.exception import WeShortError

weShort = WeShort(
    apiToken="YOUR_API_TOKEN"
)

try:
    shortUrl = await weShort.createShortUrl("https://youtu.be/YcQFi-1lAOo?si=pZO1WopFBjU2B6XJ", 1000)
except WeShortError as e:
    print(e)
    return
else:
    print(shortUrl)
```

**WeShort** is a modern, elegant and asynchronous [WeShort API](https://weshort.pro/)
shortener URL. It enables you to easily interact with the main means of WeShort using Python.


### Installation

``` bash
pip3 install weshort
```


## Made with ✨ by

[![Ayiin](https://img.shields.io/static/v1?label=Github&message=AyiinXd&color=critical)](https://github.com/AyiinXd)   
[![Ayiin](https://img.shields.io/static/v1?label=Telegram&message=AyiinXd&color=aqua)](https://t.me/AyiinXd)
#
# License
[![License](https://www.gnu.org/graphics/gplv3-with-text-136x68.png)](LICENSE)   
WeShort is licensed under [GNU General Public License](https://www.gnu.org/licenses/agpl-3.0.html) v3 or later.
#
# Credits
*  [AyiinXd](https://github.com/AyiinXd) for [weshort](https://github.com/AyiinXd/pyweshort)
#
