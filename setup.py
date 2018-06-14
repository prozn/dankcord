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
 
    install_requires=[
        'discord.py',
        'EsiPy>=0.1.8',
        'pony>=0.7.3',
        'diskcache>=3.0.6'
    ],
 
    dependency_links=[
        'git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py-1'
    ],
    )
