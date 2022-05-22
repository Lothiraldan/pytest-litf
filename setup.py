#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-litf",
    version="0.1.6",
    author="Boris Feld",
    author_email="lothiraldan@gmail.com",
    maintainer="Boris Feld",
    maintainer_email="lothiraldan@gmail.com",
    license="MIT",
    url="https://github.com/lothiraldan/pytest-litf",
    description="A pytest plugin that stream output in LITF format",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    py_modules=["pytest_litf"],
    install_requires=["pytest>=3.1.1"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["litf = pytest_litf"]},
    scripts=["bin/pytest-litf"],
)
