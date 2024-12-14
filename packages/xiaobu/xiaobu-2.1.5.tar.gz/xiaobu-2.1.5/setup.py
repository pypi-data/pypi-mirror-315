# coding: utf-8
# Project：xiaobu
# File：setup.py
# Author：IanHau


from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name="xiaobu",
    version="2.1.5",
    description="erp接口封装",
    author="IanHau",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="xiaobu",
    packages=["xiaobu", "xiaobu/api"],
    install_requires=["requests", "sqlalchemy"]
)

# python .\setup.py sdist bdist_wheel
# twine upload .\dist\xiaobu-2.0.3-py3-none-any.whl
