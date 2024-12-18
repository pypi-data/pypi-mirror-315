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

import os
import re
import shutil
import sys
from setuptools import setup, find_packages

def clearFolder(folder):
    try:
        # Remove Directory
        if os.path.exists(folder):
            shutil.rmtree(folder)
    except Exception as e:
        print(e)

with open("weshort/version.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

if sys.argv[-1] == "publish":
    clearFolder("build")
    clearFolder("dist")
    clearFolder("weshort.egg-info")
    os.system("pip install twine setuptools")
    os.system("python3 setup.py sdist")
    os.system("twine upload dist/*")
    sys.exit()


setup(
    name="weshort",
    version=version,
    description="WeShort is Shortener URL and Asynchronous API in Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/AyiinXd/pyweshort",
    download_url="https://github.com/AyiinXd/pyweshort/releases/latest",
    author="AyiinXd",
    author_email="ayiin@gotgel.org",
    license="LGPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="api scrapper library python shortener shortlink shorturl url",
    project_urls={
        "Tracker": "https://github.com/AyiinXd/pyweshort/issues",
        "Community": "https://t.me/AyiinProjects",
        "Source": "https://github.com/AyiinXd/pyweshort"
    },
    python_requires="~=3.7",
    package_data={
        "weshort": ["py.typed"],
    },
    packages=find_packages(exclude=["tests*"]),
    zip_safe=False,
    install_requires=["aiohttp"],
)