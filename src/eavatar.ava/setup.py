# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from ava import __version__

setup(
    name="ava",
    version=__version__,
    description="EAvatar Ava - A versatile agent.",
    # package_dir={'': ''},
    packages=find_packages(exclude=['tests']),
    include_package_data=True,

    install_requires=['base58',
                      'bottle',
                      'click',
                      'gevent',
                      'libnacl',
                      'lmdb',
                      'msgpack-python',
                      'pycrypto',
                      'PyDispatcher',
                      'PyYAML',
                      'pyscrypt',
                      'requests',
                      'ws4py'],
    test_suite='nose.collector',
    zip_safe=False,

    entry_points={
        'console_scripts': [
            'ava = ava.launcher:main',
        ],
    },

    author="Sam Kuo",
    author_email="sam@eavatar.com",
    url="http://www.eavatar.com",

)