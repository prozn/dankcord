import re
from setuptools import setup
 
 
version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('dankcord/dankcord.py').read(),
    re.M
    ).group(1)
 
 
# with open("README.rst", "rb") as f:
#     long_descr = f.read().decode("utf-8")
 
 
setup(
    name = "dankcord",
    packages = ["dankcord"],
    entry_points = {
        "console_scripts": ['dankcord = dankcord.dankcord:main']
        },
    version = version,
    description = "Prozn's discord bot.",
    # long_description = long_descr,
    author = "Prozn Zanjoahir",
    author_email = "prozn@quickmind.co.uk",
    url = "https://github.com/prozn/dankcord",
    )
