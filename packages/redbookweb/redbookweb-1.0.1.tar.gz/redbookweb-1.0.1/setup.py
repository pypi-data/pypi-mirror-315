'''
Author: liusuxian 382185882@qq.com
Date: 2024-10-22 21:43:34
LastEditors: liusuxian 382185882@qq.com
LastEditTime: 2024-10-23 12:05:12
Description: 

Copyright (c) 2024 by liusuxian email: 382185882@qq.com, All Rights Reserved.
'''
import os
from setuptools import setup

about = {}
here = os.path.abspath(os.path.dirname(__file__))
version_path = os.path.join(here, "redbookweb", "__version__.py")
with open(version_path, "r", encoding="utf-8") as f:
    exec(f.read(), about)
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license=about["__license__"],
    packages=["redbookweb"],
    install_requires=["requests", "lxml"],
    keywords="redbookweb crawl",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
