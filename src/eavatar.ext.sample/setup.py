# -*- coding: utf-8 -*-

"""
This is a setup.py script for packaging Windows executable.

Usage:
    python setup.py build
"""


from setuptools import setup, find_packages

setup(
    name="eavatar.ext.sample",
    version="0.1.0",
    description = "EAvatar Sample Package.",
    include_package_data=True,
    zip_safe=True,
    packages=find_packages(),
    namespace_packages=['eavatar', 'eavatar.ext'],

    entry_points={
        'ava.extension': [
            'sample1 = eavatar.ext.sample:Sample',
        ]
    }
)