#!/usr/bin/env python
"""
EST Client
==========
"""
import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "est",
    version = "0.2.1",
    author = "Laurent Luce",
    author_email = "laurentluce49@yahoo.com",
    description = ('Client to interact with an EST server - RFC 7030.'),
    license = "MIT",
    keywords = "Enrollment secure transport",
    packages=['est'],
    install_requires=[
        'pyOpenSSL',
        'asn1crypto',
        'requests'
    ],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
