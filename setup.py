from setuptools import setup, find_packages
from alchemy import alchemy

setup(
    name = "Alchemy",
    version = alchemy.__version__,
    packages = find_packages(),
    install_requires = ['docutils>=0.3'],

    package_data = {
    # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst']
    },
    #metadata
    author = "Zeph Chai",
    author_email = "chaiqianhao@gmail.com",
    url = "https://github.com/zephchai/alchemy",

)
