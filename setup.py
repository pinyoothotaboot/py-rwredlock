import re
import pathlib

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent
txt = (here / 'rwredlock' / '__version__.py').read_text()
version = re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name = "rwredlock",
    version = version,
    python_requires=">=3.10",
    author = "Mr.Pinyoo Thotaboot",
    author_email = "pinyoo.too@gmail.com",
    description = "Distribute RWLocking",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/pinyoothotaboot/py-rwlock/",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=['rwredlock']
)