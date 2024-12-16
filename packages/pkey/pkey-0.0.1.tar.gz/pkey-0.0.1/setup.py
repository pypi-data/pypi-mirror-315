import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pkey",
    version = "0.0.1",
    author = "JustAnEric",
    author_email = "ericmuzyk@icloud.com",
    description = ("A simple Python implementation to generate private keys for your applications."),
    license = "GPL-3.0",
    keywords = "key authentication",
    url = "https://github.com/JustAnEric/pkey",
    packages=['pkey'],
    long_description=read('README.md'),
    classifiers=[
        "Topic :: Utilities"
    ],
)