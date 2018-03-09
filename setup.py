#!/usr/bin/env python3

import sys
import setuptools

from asynciojobs.version import version as version

# check python version
from sys import version_info
major, minor = version_info[0:2]
if not (major == 3 and minor >= 5):
    print("python 3.5 or higher is required")
    exit(1)

long_description = \
                   "See notebook at https://github.com/parmentelat/" \
                   "asynciojobs/blob/master/README.ipynb"

required_modules = []

setuptools.setup(
    name="asynciojobs",
    version=version,
    author="Thierry Parmentelat",
    author_email="thierry.parmentelat@inria.fr",
    description="A simplistic orchestration engine for asyncio-based jobs",
    long_description=long_description,
    license="CC BY-SA 4.0",
    url="http://asynciojobs.readthedocs.io/",
    packages=['asynciojobs'],
    install_requires=required_modules,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3.5",
    ],
)
