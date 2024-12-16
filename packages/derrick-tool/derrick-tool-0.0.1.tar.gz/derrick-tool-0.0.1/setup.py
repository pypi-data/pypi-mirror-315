# -*- encoding: utf-8 -*-
"""
@File    :   setup.py    
@Contact :   qiull@tellhow.com
@Author  :   Long-Long-Qiu
@Modify Time      @Version    @Description
------------      --------    -----------
2024/12/16 14:03                None
"""
from __future__ import print_function
from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="derrick-tool",
    version='0.0.1',
    author="DerrickChiu",
    author_email="chiull@foxmail.com",
    description="some usual tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://gitee.com/DerrickChiu/derrick-tool",
    packages=find_packages(),
    install_requires=[

        ],
    classifiers=[
        "Topic :: Scientific/Engineering",
        'Topic :: Scientific/Engineering :: GIS',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
